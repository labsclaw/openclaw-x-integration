---
name: browser-batch-extraction
description: Extract data from multiple URLs in parallel. Visits N pages, runs extraction script on each, returns structured JSON. For research, monitoring, and multi-page data collection.
---

# Browser Batch Extraction

## Quando Usar

ATIVAR quando:
- Precisa coletar dados de múltiplas páginas
- Pesquisa de mercado, monitoramento de preços, scraping
- Comparação de produtos/conteúdo entre sites
- Qualquer tarefa "visitar N URLs e extrair dados"

NÃO ativar para:
- Uma única URL (usar `web_fetch` direto)
- Interação com a página (formulários, clicks) — usar `playwright__browser_*`
- Download de arquivos — usar `download-file` skill

## Padrão de Execução

### Opção 1: Sub-agent paralelo (recomendado para >5 URLs)

```javascript
// Coletar URLs primeiro
const urls = [
  "https://example.com/page1",
  "https://example.com/page2",
  "https://example.com/page3"
];

// Definir script de extração
const extractScript = `
  return {
    title: document.querySelector('h1')?.textContent?.trim(),
    price: document.querySelector('.price')?.textContent?.trim(),
    description: document.querySelector('.description')?.textContent?.slice(0, 300),
    url: window.location.href
  };
`;

// Executar via sub-agent
sessions_spawn({
  task: \`Extraia dados das seguintes URLs. Para cada URL, navegue e execute o script de extração.
  
URLs: \${JSON.stringify(urls)}

Script de extração:
\${extractScript}

Retorne JSON array com os resultados. Se uma URL falhar, inclua com error: true.\`,
  mode: "run",
  runtime: "subagent"
});
```

### Opção 2: Execução sequencial (para <5 URLs ou quando precisa de browser state)

```javascript
// Para cada URL:
for (const url of urls) {
  playwright__browser_navigate({ url });
  const result = playwright__browser_evaluate({ 
    function: extractScript 
  });
  results.push(result);
}
```

### Opção 3: web_fetch paralelo (para HTML estático, sem JS)

```javascript
// Mais rápido, sem browser
const results = await Promise.all(
  urls.map(url => web_fetch({ url, extractMode: "markdown" }))
);
```

## Script de Extração Padrão

```javascript
// Extração genérica — ajustar seletores por site
function extractPageData() {
  return {
    // Identificação
    url: window.location.href,
    title: document.querySelector('h1')?.textContent?.trim() 
        || document.title,
    
    // Conteúdo principal
    heading: document.querySelector('h1, h2')?.textContent?.trim(),
    description: document.querySelector('meta[name="description"]')?.content
              || document.querySelector('.description, .summary, .excerpt')?.textContent?.slice(0, 500),
    
    // Dados estruturados (ajustar por site)
    price: document.querySelector('.price, [data-price]')?.textContent?.trim(),
    date: document.querySelector('time, .date, .published')?.textContent?.trim(),
    author: document.querySelector('.author, [rel="author"]')?.textContent?.trim(),
    
    // Links relevantes
    links: [...document.querySelectorAll('a[href]')]
      .slice(0, 20)
      .map(a => ({ text: a.textContent.trim().slice(0, 100), href: a.href })),
    
    // Metadata
    extractedAt: new Date().toISOString()
  };
}
```

## Seletores por Tipo de Site

### E-commerce
```javascript
{
  title: 'h1.product-title, .product-name',
  price: '.price, [data-price], .current-price',
  image: '.product-image img, .gallery img',
  rating: '.rating, .stars, [data-rating]',
  reviews: '.review-count, .reviews-count'
}
```

### Noticias/Artigos
```javascript
{
  title: 'h1.article-title, .headline',
  author: '.author, [rel="author"], .byline',
  date: 'time[datetime], .publish-date',
  content: '.article-body, .post-content, article',
  image: '.featured-image img, .hero-image img'
}
```

### Redes Sociais/Perfis
```javascript
{
  name: '.profile-name, .display-name',
  bio: '.bio, .description, .about',
  followers: '.followers-count, .follower-count',
  posts: '.post, .tweet, .status'
}
```

## Tratamento de Erros

| Erro | Ação |
|------|------|
| Timeout (30s) | Marcar URL como failed, continuar com próximas |
| CAPTCHA | Pular URL, logar para investigação manual |
| Login wall | Pular URL, reportar que precisa de autenticação |
| 404 | Marcar como not_found, continuar |
| JS error | Retry uma vez, se falhar marcar como error |

## Formato de Output

```json
{
  "results": [
    {
      "url": "https://example.com/page1",
      "status": "success",
      "data": { "title": "...", "price": "...", "..." },
      "extractedAt": "2026-07-03T15:00:00Z"
    },
    {
      "url": "https://example.com/page2",
      "status": "error",
      "error": "Timeout after 30s",
      "extractedAt": "2026-07-03T15:00:31Z"
    }
  ],
  "summary": {
    "total": 10,
    "success": 8,
    "failed": 2,
    "duration": "45s"
  }
}
```

## Performance

| Método | Velocidade | JS Rendering | Use Case |
|--------|-----------|--------------|----------|
| `web_fetch` | ~2s/URL | ❌ | HTML estático |
| `playwright` sequencial | ~5s/URL | ✅ | Precisa de interação |
| Sub-agent paralelo | ~5s total (10 URLs) | ✅ | Múltiplas URLs, extração complexa |

**Regra:** Para >5 URLs, sempre usar sub-agent paralelo. Para <5, `web_fetch` se estático, `playwright` se dinâmico.
