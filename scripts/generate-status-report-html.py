import base64
import os

with open(r"artifacts\x-testing\assets\image2.png", "rb") as f:
    b64_logo = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Status Report • Projeto QAI X-Testing</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --green-primary: #38761D;
      --green-accent: #509546;
      --green-light: #6AA84F;
      --green-dark: #274E13;
      --orange-alert: #FF5722;
      --dark-text: #1A1A1A;
      --gray-sub: #7F7F7F;
      --border-gray: #E2E8F0;
      --bg-page: #F4F6F4;
      --surface: #FFFFFF;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Raleway', sans-serif;
      background-color: var(--bg-page);
      color: var(--dark-text);
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 30px 20px;
    }}

    .deck-container {{
      width: 100%;
      max-width: 1240px;
      display: flex;
      flex-direction: column;
      gap: 36px;
    }}

    .slide {{
      background: var(--surface);
      border: 1px solid var(--border-gray);
      border-radius: 18px;
      padding: 36px 44px;
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.08);
      position: relative;
      overflow: hidden;
    }}

    .slide::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; height: 5px;
      background: linear-gradient(90deg, var(--green-primary), var(--green-accent), var(--orange-alert));
    }}

    .slide-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 26px;
    }}

    .slide-header-text {{
      max-width: 80%;
    }}

    .slide-tag {{
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: var(--orange-alert);
      margin-bottom: 4px;
    }}

    .slide-title {{
      font-size: 26px;
      font-weight: 800;
      color: var(--dark-text);
      line-height: 1.2;
    }}

    .slide-subtitle {{
      font-size: 13px;
      font-weight: 500;
      color: var(--gray-sub);
      margin-top: 4px;
    }}

    .slide-logo {{
      height: 48px;
      object-fit: contain;
    }}

    /* 3 COLUMNS CARDS (SLIDE 1 & SLIDE 5) */
    .cards-grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }}

    .card-box {{
      background: #FFFFFF;
      border: 1px solid var(--border-gray);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }}

    .card-box.green-dark {{ border-top: 4px solid var(--green-primary); }}
    .card-box.green-mid {{ border-top: 4px solid var(--green-accent); }}
    .card-box.orange {{ border-top: 4px solid var(--orange-alert); }}
    .card-box.blue {{ border-top: 4px solid #156082; }}

    .card-num {{
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }}
    .card-box.green-dark .card-num {{ color: var(--green-primary); }}
    .card-box.green-mid .card-num {{ color: var(--green-accent); }}
    .card-box.orange .card-num {{ color: var(--orange-alert); }}
    .card-box.blue .card-num {{ color: #156082; }}

    .card-title {{
      font-size: 17px;
      font-weight: 800;
      margin-bottom: 4px;
      color: var(--dark-text);
    }}

    .card-badge {{
      display: inline-block;
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: 0.5px;
      margin-bottom: 10px;
    }}

    .card-desc {{
      font-size: 12px;
      color: var(--gray-sub);
      line-height: 1.45;
      margin-bottom: 14px;
    }}

    .card-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 12px;
      color: #333333;
      line-height: 1.4;
    }}

    /* 2x2 GRID (SLIDE 4) */
    .grid-2x2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}

    .grid-card {{
      background: #FFFFFF;
      border: 1px solid var(--border-gray);
      border-radius: 14px;
      padding: 20px 22px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }}

    .grid-card.green-dark {{ border-top: 4px solid var(--green-primary); }}
    .grid-card.green-mid {{ border-top: 4px solid var(--green-accent); }}
    .grid-card.green-deep {{ border-top: 4px solid var(--green-dark); }}
    .grid-card.orange {{ border-top: 4px solid var(--orange-alert); }}

    /* ROADMAP & TABLES (SLIDE 2 & 3) */
    .roadmap-table, .schedule-table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 8px;
    }}

    .th-cat {{
      background: #FFFFFF;
      color: var(--dark-text);
      border: 1px solid var(--border-gray);
      border-radius: 8px;
      padding: 10px;
      font-size: 11.5px;
      font-weight: 800;
      text-align: center;
    }}

    .th-stage {{
      color: #FFFFFF;
      border-radius: 8px;
      padding: 10px;
      font-size: 11.5px;
      font-weight: 800;
      text-align: center;
    }}

    .td-cat {{
      background: #FFFFFF;
      color: var(--dark-text);
      border: 1px solid var(--border-gray);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 11.5px;
      font-weight: 800;
      text-align: center;
      vertical-align: middle;
    }}

    .td-content {{
      background: #FFFFFF;
      border: 1px solid var(--border-gray);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 11px;
      line-height: 1.4;
      vertical-align: top;
    }}

    .td-content.current-month {{
      background: #EDF7ED;
      border: 1.5px solid var(--green-primary);
      color: var(--green-dark);
      font-weight: 600;
    }}

    .sched-th {{
      color: #FFFFFF;
      padding: 10px;
      font-size: 11.5px;
      font-weight: 800;
      text-align: center;
      border-radius: 8px;
    }}

    .sched-wp {{
      background: #FFFFFF;
      border: 1px solid var(--border-gray);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 11px;
      font-weight: 800;
      color: var(--dark-text);
      vertical-align: middle;
    }}

    .sched-cell {{
      background: #FFFFFF;
      border: 1px solid var(--border-gray);
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 10.5px;
      line-height: 1.4;
      vertical-align: top;
    }}

    .cell-done {{
      background: #EDF7ED;
      border: 1.5px solid var(--green-primary);
      color: var(--green-dark);
    }}

    .cell-active {{
      background: #FFF3EE;
      border: 1.5px solid var(--orange-alert);
      color: #9A3412;
    }}

    .cell-target {{
      background: #F0F9F0;
      border: 1px solid var(--green-accent);
      color: var(--dark-text);
    }}

    .cell-blocked {{
      background: #F5F5F5;
      color: #888888;
      border: 1px solid var(--border-gray);
    }}

    .slide-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 24px;
      padding-top: 14px;
      border-top: 1px solid var(--border-gray);
      font-size: 10px;
      font-weight: 700;
      color: #999999;
      letter-spacing: 0.5px;
    }}

    .footer-note {{
      margin-top: 24px;
      font-size: 12px;
      font-weight: 600;
      color: #777777;
      text-align: center;
    }}
  </style>
</head>
<body>

<div class="deck-container">

  <!-- SLIDE 1 -->
  <section class="slide">
    <div class="slide-header">
      <div class="slide-header-text">
        <div class="slide-tag">01 / ESTRATÉGIA OPERACIONAL</div>
        <h1 class="slide-title">Key Objectives & Estratégia de Fases</h1>
        <p class="slide-subtitle">Evolução da operação de testes manuais para esteira autônoma com agentes de IA (OpenClaw + Paperclip)</p>
      </div>
      <img src="data:image/png;base64,{b64_logo}" class="slide-logo" alt="X-Testing Logo">
    </div>

    <div class="cards-grid-3">
      <div class="card-box green-dark">
        <div class="card-num">01 • FASE 01</div>
        <div class="card-title">WEB: Testes Manuais</div>
        <div class="card-badge" style="color: var(--green-primary);">EM ANDAMENTO • BASELINE</div>
        <p class="card-desc">Espelhamento dos papéis operacionais e automação do suporte à execução manual.</p>
        <ul class="card-list">
          <li>• Extração estruturada de requisitos (Tree-RAG / PageIndex)</li>
          <li>• Geração de fluxos e regras em BPMN 2.0 formal</li>
          <li>• Elaboração automatizada de Casos de Teste (TestLink)</li>
          <li>• Triagem e pré-preenchimento de defeitos (Mantis)</li>
        </ul>
      </div>

      <div class="card-box green-mid">
        <div class="card-num">02 • FASE 02</div>
        <div class="card-title">WEB: Integração & Aceitação</div>
        <div class="card-badge" style="color: var(--green-accent);">PLANEJADA • SEQUENCIAL</div>
        <p class="card-desc">Automação E2E com execução autônoma no navegador e evidências rastreáveis.</p>
        <ul class="card-list">
          <li>• Execução agêntica via Playwright / Camoufox</li>
          <li>• Validação de integração de APIs e regras de negócio</li>
          <li>• Geração de evidências com prints e vídeos por passo</li>
          <li>• Pipeline de regressão contínua integrada ao CI/CD</li>
        </ul>
      </div>

      <div class="card-box orange">
        <div class="card-num">03 • FASE 03</div>
        <div class="card-title">MOBILE: Todos os Anteriores</div>
        <div class="card-badge" style="color: var(--orange-alert);">CONDICIONAL • PÓS-WEB</div>
        <p class="card-desc">Transposição do ecossistema agêntico completo para aplicações mobile nativas.</p>
        <ul class="card-list">
          <li>• Início condicionado ao término das Fases 01 e 02</li>
          <li>• Testes funcionais, usabilidade e fluxos de tela nativos</li>
          <li>• Integração e testes de aceitação em Android/iOS</li>
          <li>• Automação agêntica em dispositivos reais e emuladores</li>
        </ul>
      </div>
    </div>

    <div class="slide-footer">
      <span>PROJETO QAI • FÁBRICA DE TESTES X-TESTING</span>
      <span>WWW.XTESTING.COM.BR</span>
    </div>
  </section>

  <!-- SLIDE 2 -->
  <section class="slide">
    <div class="slide-header">
      <div class="slide-header-text">
        <div class="slide-tag">02 / ROADMAP ESTRATÉGICO</div>
        <h1 class="slide-title">Product Stages Roadmap (Setembro - Dezembro 2026)</h1>
        <p class="slide-subtitle">Evolução estruturada em 4 etapas bimestrais com entregas tangíveis e critérios de avanço</p>
      </div>
      <img src="data:image/png;base64,{b64_logo}" class="slide-logo" alt="X-Testing Logo">
    </div>

    <table class="roadmap-table">
      <thead>
        <tr>
          <th class="th-cat" style="width: 18%;">Our Approach</th>
          <th class="th-stage" style="background: var(--green-primary); width: 20.5%;">1. Setembro 2026</th>
          <th class="th-stage" style="background: var(--green-accent); width: 20.5%;">2. Outubro 2026</th>
          <th class="th-stage" style="background: #156082; width: 20.5%;">3. Novembro 2026</th>
          <th class="th-stage" style="background: var(--orange-alert); width: 20.5%;">4. Dezembro 2026</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="td-cat">Strategic<br>Objectives</td>
          <td class="td-content current-month">
            • Instalar Paperclip & estruturar XTE<br>
            • Baseline agêntico com QAI (CEO)<br>
            • Rastreabilidade sem chunking
          </td>
          <td class="td-content">
            • Operar WEB Testes Manuais<br>
            • Automatizar geração de TC / Mantis<br>
            • Integrar conectores ALM
          </td>
          <td class="td-content">
            • Automação WEB Integração/E2E<br>
            • Execução autônoma Playwright<br>
            • Validação contínua de regras
          </td>
          <td class="td-content">
            • Kickoff esteira MOBILE<br>
            • Transpor skills para apps nativos<br>
            • Homologação completa
          </td>
        </tr>
        <tr>
          <td class="td-cat">Key<br>Milestones</td>
          <td class="td-content current-month">
            • Ambiente Paperclip 100% ativo<br>
            • Tree-RAG SANASA indexado<br>
            • Skill de BPMN validada
          </td>
          <td class="td-content">
            • 1º Ciclo de testes gerado por IA<br>
            • Geração de CTs no TestLink<br>
            • Validação com time SANASA
          </td>
          <td class="td-content">
            • Bateria de testes E2E executada<br>
            • Cobertura de regras críticas<br>
            • Evidências visuais auditáveis
          </td>
          <td class="td-content">
            • Matriz de testes Mobile pronta<br>
            • Execução emuladores/reais<br>
            • Handover operacional 2027
          </td>
        </tr>
        <tr>
          <td class="td-cat">Deliverables</td>
          <td class="td-content current-month">
            • Planilha Classificação / Riscos<br>
            • sanasa-requirements-tree.json<br>
            • Segmentos SSC no Memory Viewer
          </td>
          <td class="td-content">
            • Suíte TestLink gerada por IA<br>
            • Relatório de aderência manual<br>
            • Dashboards operacionais QAI
          </td>
          <td class="td-content">
            • Scripts Playwright automatizados<br>
            • Pipeline de testes WEB ativa<br>
            • Relatórios de bugs no Mantis
          </td>
          <td class="td-content">
            • Suíte Mobile completa (Fase 3)<br>
            • Relatório consolidado de KPIs<br>
            • Manual operacional agêntico
          </td>
        </tr>
      </tbody>
    </table>

    <div class="slide-footer">
      <span>PROJETO QAI • FÁBRICA DE TESTES X-TESTING</span>
      <span>WWW.XTESTING.COM.BR</span>
    </div>
  </section>

  <!-- SLIDE 3 -->
  <section class="slide">
    <div class="slide-header">
      <div class="slide-header-text">
        <div class="slide-tag">03 / CRONOGRAMA EXECUTIVO</div>
        <h1 class="slide-title">Schedule Executivo & Marcos de Progresso (Mês a Mês)</h1>
        <p class="slide-subtitle">Acompanhamento sistemático por Work Packages alinhados aos marcos contratuais e técnicos</p>
      </div>
      <img src="data:image/png;base64,{b64_logo}" class="slide-logo" alt="X-Testing Logo">
    </div>

    <table class="schedule-table">
      <thead>
        <tr>
          <th class="sched-th" style="background:#1A1A1A; width: 28%;">Work Package / Trilha de Execução</th>
          <th class="sched-th" style="background:var(--green-primary); width: 18%;">SET/2026 (Atual)</th>
          <th class="sched-th" style="background:var(--green-accent); width: 18%;">OUT/2026</th>
          <th class="sched-th" style="background:#156082; width: 18%;">NOV/2026</th>
          <th class="sched-th" style="background:var(--orange-alert); width: 18%;">DEZ/2026</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="sched-wp">WP1 • Setup Agêntico & Paperclip<br><span style="font-size:9.5px; color:var(--gray-sub);">Ambiente, organograma e governança QAI</span></td>
          <td class="sched-cell cell-done"><strong>100% CONCLUÍDO</strong><br>• Paperclip ativo<br>• Empresa XTE configurada</td>
          <td class="sched-cell">Operação Contínua<br>• Monitoramento</td>
          <td class="sched-cell">Operação Contínua<br>• Manutenção</td>
          <td class="sched-cell">Operação Contínua<br>• Governança</td>
        </tr>
        <tr>
          <td class="sched-wp">WP2 • Extração de Requisitos & BPMN<br><span style="font-size:9.5px; color:var(--gray-sub);">Tree-RAG sem chunking e fluxos de negócio</span></td>
          <td class="sched-cell cell-done"><strong>100% CONCLUÍDO</strong><br>• Árvore de requisitos<br>• Skill BPMN validada</td>
          <td class="sched-cell">Refinamento<br>• Novos fluxos</td>
          <td class="sched-cell">Suporte a E2E<br>• Validação cruzada</td>
          <td class="sched-cell">Migração p/ Mobile<br>• Mapeamento</td>
        </tr>
        <tr>
          <td class="sched-wp">WP3 • FASE 1: WEB Testes Manuais<br><span style="font-size:9.5px; color:var(--gray-sub);">Suporte IA para TestLink e Mantis</span></td>
          <td class="sched-cell cell-active"><strong>EM ANDAMENTO</strong><br>• Matriz prioridades<br>• Riscos SANASA</td>
          <td class="sched-cell cell-target"><strong>EXECUÇÃO PLENA</strong><br>• Suíte TestLink<br>• Triagem Mantis</td>
          <td class="sched-cell">Estabilização<br>• Homologação</td>
          <td class="sched-cell">Fase Concluída<br>• Transição</td>
        </tr>
        <tr>
          <td class="sched-wp">WP4 • FASE 2: WEB Integração & E2E<br><span style="font-size:9.5px; color:var(--gray-sub);">Automação autônoma Playwright / Camoufox</span></td>
          <td class="sched-cell">Planejamento<br>• Spike arquitetura</td>
          <td class="sched-cell">Desenvolvimento<br>• Conectores E2E</td>
          <td class="sched-cell cell-target"><strong>EXECUÇÃO PLENA</strong><br>• Automação E2E<br>• Evidências vídeo</td>
          <td class="sched-cell">Fase Concluída<br>• Regressão ativa</td>
        </tr>
        <tr>
          <td class="sched-wp">WP5 • FASE 3: MOBILE (Todos)<br><span style="font-size:9.5px; color:var(--gray-sub);">Testes manuais e automação em apps nativos</span></td>
          <td class="sched-cell cell-blocked">Bloqueado<br><em>(Aguardando WEB)</em></td>
          <td class="sched-cell cell-blocked">Bloqueado<br><em>(Aguardando WEB)</em></td>
          <td class="sched-cell">Preparação<br>• Setup device farm</td>
          <td class="sched-cell cell-target"><strong>EXECUÇÃO PLENA</strong><br>• Testes Manuais & E2E Mobile</td>
        </tr>
      </tbody>
    </table>

    <div class="slide-footer">
      <span>PROJETO QAI • FÁBRICA DE TESTES X-TESTING</span>
      <span>WWW.XTESTING.COM.BR</span>
    </div>
  </section>

  <!-- SLIDE 4 -->
  <section class="slide">
    <div class="slide-header">
      <div class="slide-header-text">
        <div class="slide-tag">04 / STATUS DA OPERAÇÃO</div>
        <h1 class="slide-title">Tarefas Realizadas</h1>
        <p class="slide-subtitle">Estruturação dos Agentes Operacionais, Demandas Paperclip, Entregáveis RF046/RF047 e Decisões de Continuidade</p>
      </div>
      <img src="data:image/png;base64,{b64_logo}" class="slide-logo" alt="X-Testing Logo">
    </div>

    <div class="grid-2x2">
      <!-- Card 1: Agentes -->
      <div class="grid-card green-dark">
        <div class="card-num" style="color: var(--green-primary);">ESTRUTURA OPERACIONAL • 5 AGENTES</div>
        <h2 style="font-size: 15px; font-weight: 800; margin-bottom: 8px; color: var(--dark-text);">Criação e Configuração de Agentes</h2>
        <ul style="list-style: none; display: flex; flex-direction: column; gap: 5px; font-size: 11.5px; color: #333;">
          <li><strong style="color: var(--green-primary);">• QAI (CEO):</strong> Liderança executiva, governança e validação final da esteira.</li>
          <li><strong style="color: var(--green-primary);">• Gerência de Projetos:</strong> Planejamento de sprints, gestão de backlog e prazos.</li>
          <li><strong style="color: var(--green-primary);">• Análise de Processos:</strong> Modelagem BPMN 2.0 dos fluxos e regras de negócio.</li>
          <li><strong style="color: var(--green-primary);">• Análise de Testes:</strong> Especificação de cenários e suítes completas TestLink.</li>
          <li><strong style="color: var(--green-primary);">• Testador:</strong> Execução WEB/Playwright, evidências e reporte de defeitos.</li>
        </ul>
      </div>

      <!-- Card 2: Entregáveis RF046/RF047 -->
      <div class="grid-card green-mid">
        <div class="card-num" style="color: var(--green-accent);">DEMANDA SANASA • OS 2026/2652</div>
        <h2 style="font-size: 15px; font-weight: 800; margin-bottom: 8px; color: var(--dark-text);">Entregáveis da Demanda RF046/RF047</h2>
        <ul style="list-style: none; display: flex; flex-direction: column; gap: 5px; font-size: 11.5px; color: #333;">
          <li><strong>📄 RF046-RF047-Julgamento-Desclassificacao.bpmn:</strong> Modelagem formal BPMN 2.0.</li>
          <li><strong>📄 RF046-RF047-Documentacao-BPMN.md:</strong> Documentação técnica e conformidade Lei 14.133.</li>
          <li><strong>📄 RF046-RF047-Suite-Testes-TestLink.xml:</strong> Suíte padronizada com 15 casos estruturados.</li>
          <li><strong>📄 RF046-RF047-Planilha-Divergencia-SANASA.csv:</strong> Matriz com 27 requisitos avaliados.</li>
        </ul>
        <div style="margin-top: 6px;"><a href="https://github.com/labsclaw/openclaw-x-integration" target="_blank" style="color: var(--green-primary); font-weight: 700; text-decoration: none; font-size: 11px;">🔗 Repositório GitHub (openclaw-x-integration) &rarr;</a></div>
      </div>

      <!-- Card 3: 33 Tarefas Paperclip -->
      <div class="grid-card green-deep">
        <div class="card-num" style="color: var(--green-dark);">PAINEL DE DEMANDAS NO PAPERCLIP</div>
        <h2 style="font-size: 15px; font-weight: 800; margin-bottom: 8px; color: var(--dark-text);">33 Tarefas Registradas</h2>
        <div style="display: flex; flex-direction: column; gap: 7px; font-size: 11.5px;">
          <div><strong style="color: var(--green-primary);">✔ 15 Concluídas (45.5%):</strong> Especificações TestLink, BPMNs e planilhas de divergência de 5 OSs (RF002, RF027, RF043, RF050 e RF058/RF061).</div>
          <div><strong style="color: var(--orange-alert);">⛔ 6 Bloqueadas (18.2%):</strong> Impedimento por credenciais externas/homologação SANASA (ex.: XTE-18 execução CS-01..10, XTE-16, XTE-23).</div>
          <div><strong style="color: #156082;">⏳ 12 Em Revisão / Backlog (36.3%):</strong> Validações técnicas, conectores e preparação da Fase 1.</div>
        </div>
      </div>

      <!-- Card 4: Decisões Operacionais -->
      <div class="grid-card orange">
        <div class="card-num" style="color: var(--orange-alert);">PROATIVIDADE & BYPASS TÉCNICO</div>
        <h2 style="font-size: 15px; font-weight: 800; margin-bottom: 8px; color: var(--dark-text);">Decisões para Seguir Implementando</h2>
        <div style="display: flex; flex-direction: column; gap: 7px; font-size: 11.5px; color: #333; line-height: 1.4;">
          <div><strong style="color: var(--dark-text);">1. Validação WEB via Mocks Locais (Playwright):</strong> Execução das suítes diretamente contra os fluxos modelados com emulação/mocks via Playwright, eliminando espera passiva por ambientes externos.</div>
          <div><strong style="color: var(--dark-text);">2. Pacotes de Exportação Estruturada (Mantis):</strong> Defeitos (MANTIS-SANASA-1045..1048) gerados em pacotes (XML/JSON/CSV) pré-formatados para carga em lote imediata pós-credenciais.</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>PROJETO QAI • FÁBRICA DE TESTES X-TESTING</span>
      <span>WWW.XTESTING.COM.BR</span>
    </div>
  </section>

  <!-- SLIDE 5 -->
  <section class="slide">
    <div class="slide-header">
      <div class="slide-header-text">
        <div class="slide-tag">05 / PLANEJAMENTO & GOVERNANÇA</div>
        <h1 class="slide-title">Próximas Tarefas</h1>
        <p class="slide-subtitle">Mapeamento Operacional, Skills de Compliance Regulatório e Prontidão para Auditoria de IA</p>
      </div>
      <img src="data:image/png;base64,{b64_logo}" class="slide-logo" alt="X-Testing Logo">
    </div>

    <div class="cards-grid-3">
      <!-- Card 1: Reunião X-Testing -->
      <div class="card-box green-dark">
        <div class="card-num">ALINHAMENTO OPERACIONAL</div>
        <div class="card-title">Detalhamento do Fluxo X-Testing</div>
        <div class="card-badge" style="color: var(--green-primary);">IMERSÃO & DIAGNÓSTICO DA ESTEIRA</div>
        <p class="card-desc">Alinhamento aprofundado dos ritos operacionais e critérios de transição entre analistas e agentes.</p>
        <ul class="card-list">
          <li>• Reunião técnica com time de liderança e especialistas da X-Testing.</li>
          <li>• Mapeamento detalhado da esteira atual de testes manuais e rituais operacionais.</li>
          <li>• Levantamento de critérios de aceite, triagem de defeitos e transição para esteira autônoma.</li>
          <li>• Mapeamento de critérios de passagem, geração de massa de teste e homologação.</li>
          <li>• Identificação de gargalos operacionais e pontos de atrito para automação imediata.</li>
          <li>• Definição de interfaces de colaboração entre analistas humanos e agentes de IA.</li>
        </ul>
      </div>

      <!-- Card 2: Skills de Compliance -->
      <div class="card-box green-mid">
        <div class="card-num">PRIVACIDADE & SEGURANÇA</div>
        <div class="card-title">Skills de Compliance dos Agentes</div>
        <div class="card-badge" style="color: var(--green-accent);">LGPD • GDPR • HIPAA • CCPA • SOC 2 • ISO 27001 • PCI-DSS</div>
        <p class="card-desc">Pesquisa e planejamento de guardrails procedural para comportamento seguro dos agentes.</p>
        <ul class="card-list">
          <li>• <strong>Anonimização & Pseudonimização (K2View, Protecto.ai):</strong> Mascaramento dinâmico, tokenização e hashing irreversível com sal.</li>
          <li>• <strong>Diretrizes ANPD & UFCA:</strong> Aplicação dos padrões regulatórios brasileiros para desidentificação de bases de homologação.</li>
          <li>• <strong>Tarjamento de Evidências (MavenDoc):</strong> Censura automatizada de PII (CPFs, nomes, valores) em screenshots e PDFs de teste.</li>
          <li>• <strong>Coleta Segura & OSINT Ético (OSINT Brasil):</strong> Higiene de dados para evitar vazamento de credenciais e dados em prompts.</li>
        </ul>
      </div>

      <!-- Card 3: Prontidão para Auditoria de IA -->
      <div class="card-box orange">
        <div class="card-num">GOVERNANÇA REGULATÓRIA</div>
        <div class="card-title">Prontidão para Auditoria de IA</div>
        <div class="card-badge" style="color: var(--orange-alert);">SOC 2 AI • IA GDPR • ISO 27001 IA</div>
        <p class="card-desc">Controles formais de segurança, auditoria contínua e certificação de pipelines agênticos.</p>
        <ul class="card-list">
          <li>• <strong>SOC 2 AI:</strong> Controles de integridade, confidencialidade, auditabilidade de inferências e trilhas de log imutáveis.</li>
          <li>• <strong>IA GDPR / LGPD:</strong> Minimização estrita de dados em prompts, política de zero-data retention com LLMs e explicabilidade técnica.</li>
          <li>• <strong>ISO 27001 IA (ref: Mukul975 / GetClaudeSkills):</strong> Políticas de segurança da informação aplicadas a agentes e gestão de riscos.</li>
          <li>• <strong>Procedural Gates:</strong> Barreira de checagem automática que bloqueia qualquer ação externa não-conforme antes da persistência ou envio.</li>
        </ul>
      </div>
    </div>

    <div class="slide-footer">
      <span>PROJETO QAI • FÁBRICA DE TESTES X-TESTING</span>
      <span>WWW.XTESTING.COM.BR</span>
    </div>
  </section>

</div>

<div class="footer-note">
  Status Report QAI • X-Testing & SANASA • Atualizado em Setembro/2026 • Apresentação de Acompanhamento Mensal
</div>

</body>
</html>
"""

with open(r"artifacts\x-testing\status-report-qai-2026-09.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML generated successfully with X-Testing visual identity and embedded logo.")
