import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    # Colors
    NAVY = RGBColor(15, 23, 42)        # #0f172a
    DARK_BLUE = RGBColor(30, 41, 59)   # #1e293b
    PRIMARY_BLUE = RGBColor(37, 99, 235) # #2563eb
    TEAL = RGBColor(13, 148, 136)      # #0d9488
    ORANGE = RGBColor(234, 88, 12)     # #ea580c
    PURPLE = RGBColor(147, 51, 234)    # #9333ea
    GREEN = RGBColor(22, 163, 74)      # #16a34a
    GRAY_TEXT = RGBColor(100, 116, 139) # #64748b
    LIGHT_BG = RGBColor(248, 250, 252) # #f8fafc
    WHITE = RGBColor(255, 255, 255)
    BORDER_GRAY = RGBColor(226, 232, 240)

    # -------------------------------------------------------------
    # SLIDE 1: KEY OBJECTIVES
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    
    # Background
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = LIGHT_BG
    bg.line.fill.background()

    # Header container
    header_box = slide1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.2))
    tf1 = header_box.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "PROJETO QAI • X-TESTING & SANASA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p2 = tf1.add_paragraph()
    p2.text = "Key Objectives & Estratégia de Fases"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = NAVY

    p3 = tf1.add_paragraph()
    p3.text = "Evolução da operação de testes manuais para esteira autônoma com agentes de IA (OpenClaw + Paperclip)"
    p3.font.size = Pt(12)
    p3.font.color.rgb = GRAY_TEXT

    # 3 Phase Cards
    phases = [
        {
            "num": "FASE 01",
            "title": "WEB: Testes Manuais",
            "tag": "EM ANDAMENTO • BASELINE",
            "color": ORANGE,
            "desc": "Espelhamento dos papéis operacionais e automação do suporte à execução manual.",
            "items": [
                "Extração estruturada de requisitos (Tree-RAG / PageIndex)",
                "Geração de fluxos e regras em BPMN via skill especializada",
                "Elaboração automatizada de Casos de Teste (TestLink)",
                "Triagem e pré-preenchimento de defeitos (Mantis)"
            ]
        },
        {
            "num": "FASE 02",
            "title": "WEB: Integração & Aceitação",
            "tag": "PLANEJADA • SEQUENCIAL",
            "color": PRIMARY_BLUE,
            "desc": "Automação E2E com execução autônoma no navegador e evidências rastreáveis.",
            "items": [
                "Execução agêntica via Playwright / Camoufox (Ultra Browser)",
                "Validação de integração de APIs e regras de negócio",
                "Geração de evidências com prints e vídeos por passo",
                "Pipeline de regressão contínua integrada ao CI/CD"
            ]
        },
        {
            "num": "FASE 03",
            "title": "MOBILE: Todos os Anteriores",
            "tag": "CONDICIONAL • PÓS-WEB",
            "color": PURPLE,
            "desc": "Transposição do ecossistema agêntico completo para aplicações mobile nativas.",
            "items": [
                "Início condicionado ao término das Fases 01 e 02",
                "Testes funcionais, usabilidade e fluxos de tela nativos",
                "Integração e testes de aceitação em Android/iOS",
                "Automação agêntica em dispositivos reais e emuladores"
            ]
        }
    ]

    card_width = Inches(3.64)
    card_gap = Inches(0.38)
    left_margin = Inches(0.8)
    top_pos = Inches(2.0)
    card_height = Inches(4.8)

    for i, phase in enumerate(phases):
        card_left = left_margin + i * (card_width + card_gap)
        
        # Card Background
        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_left, top_pos, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_GRAY
        card.line.width = Pt(1.5)

        # Top Accent Line
        accent = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_left + Inches(0.2), top_pos + Inches(0.18), Inches(1.2), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = phase["color"]
        accent.line.fill.background()

        # Text inside card
        tb = slide1.shapes.add_textbox(card_left + Inches(0.2), top_pos + Inches(0.35), card_width - Inches(0.4), card_height - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = phase["num"]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = phase["color"]

        p_t = tf.add_paragraph()
        p_t.text = phase["title"]
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY
        p_t.space_after = Pt(6)

        p_tag = tf.add_paragraph()
        p_tag.text = phase["tag"]
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = phase["color"]
        p_tag.space_after = Pt(10)

        p_d = tf.add_paragraph()
        p_d.text = phase["desc"]
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = GRAY_TEXT
        p_d.space_after = Pt(14)

        for item in phase["items"]:
            p_i = tf.add_paragraph()
            p_i.text = f"•  {item}"
            p_i.font.size = Pt(10)
            p_i.font.color.rgb = DARK_BLUE
            p_i.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 2: ROADMAP (Set/2026 a Dez/2026) - Template Chevrons
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    bg2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = LIGHT_BG
    bg2.line.fill.background()

    # Header
    header2 = slide2.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
    tf2 = header2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "PROJETO QAI • X-TESTING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p2 = tf2.add_paragraph()
    p2.text = "Product Stages Roadmap (Setembro - Dezembro 2026)"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = NAVY

    # Columns: 1 Category column + 4 Month columns
    col_x = [Inches(0.8), Inches(2.8), Inches(5.4), Inches(8.0), Inches(10.6)]
    col_w = [Inches(1.8), Inches(2.45), Inches(2.45), Inches(2.45), Inches(2.45)]

    months = [
        {"num": "1", "name": "Setembro 2026", "sub": "Setup & Baseline", "color": ORANGE},
        {"num": "2", "name": "Outubro 2026", "sub": "WEB Manuais", "color": PRIMARY_BLUE},
        {"num": "3", "name": "Novembro 2026", "sub": "WEB Integração", "color": PURPLE},
        {"num": "4", "name": "Dezembro 2026", "sub": "Mobile & Escala", "color": GREEN}
    ]

    # Draw Chevrons / Headers
    stage_header_top = Inches(1.7)
    stage_header_h = Inches(0.7)

    # Category Header
    cat_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x[0], stage_header_top, col_w[0], stage_header_h)
    cat_box.fill.solid()
    cat_box.fill.fore_color.rgb = WHITE
    cat_box.line.color.rgb = BORDER_GRAY
    tf = cat_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Our Approach"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

    for idx, m in enumerate(months):
        m_box = slide2.shapes.add_shape(MSO_SHAPE.CHEVRON, col_x[idx+1], stage_header_top, col_w[idx], stage_header_h)
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = m["color"]
        m_box.line.fill.background()
        tf = m_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{m['num']}. {m['name']}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    # Rows: Strategic Objectives, Key Milestones, Deliverables
    rows = [
        {
            "name": "Strategic\nObjectives",
            "y": Inches(2.5),
            "h": Inches(1.5),
            "content": [
                [ # Setembro (Done)
                    "• Instalar Paperclip & estruturar XTE",
                    "• Baseline agêntico com QAI (CEO)",
                    "• Rastreabilidade sem chunking"
                ],
                [ # Outubro
                    "• Operar WEB Testes Manuais",
                    "• Automatizar geração de TC / Mantis",
                    "• Integrar conectores ALM"
                ],
                [ # Novembro
                    "• Automação WEB Integração/E2E",
                    "• Execução autônoma Playwright",
                    "• Validação contínua de regras"
                ],
                [ # Dezembro
                    "• Kickoff esteira MOBILE",
                    "• Transpor skills para apps nativos",
                    "• Homologação completa"
                ]
            ]
        },
        {
            "name": "Key\nMilestones",
            "y": Inches(4.1),
            "h": Inches(1.45),
            "content": [
                [ # Setembro
                    "• Ambiente Paperclip 100% ativo",
                    "• Tree-RAG SANASA indexado",
                    "• Skill de BPMN validada"
                ],
                [ # Outubro
                    "• 1º Ciclo de testes gerado por IA",
                    "• Geração de CTs no TestLink",
                    "• Validação com time SANASA"
                ],
                [ # Novembro
                    "• Bateria de testes E2E executada",
                    "• Cobertura de regras críticas",
                    "• Evidências visuais auditáveis"
                ],
                [ # Dezembro
                    "• Matriz de testes Mobile pronta",
                    "• Execução emuladores/reais",
                    "• Handover operacional 2027"
                ]
            ]
        },
        {
            "name": "Deliverables",
            "y": Inches(5.65),
            "h": Inches(1.5),
            "content": [
                [ # Setembro
                    "• Planilha de Classificação / Riscos",
                    "• sanasa-requirements-tree.json",
                    "• Segmentos SSC no Memory Viewer"
                ],
                [ # Outubro
                    "• Suíte TestLink gerada por IA",
                    "• Relatório de aderência manual",
                    "• Dashboards operacionais QAI"
                ],
                [ # Novembro
                    "• Scripts Playwright automatizados",
                    "• Pipeline de testes WEB ativa",
                    "• Relatórios de bugs no Mantis"
                ],
                [ # Dezembro
                    "• Suíte Mobile completa (Fase 3)",
                    "• Relatório consolidado de KPIs",
                    "• Manual operacional agêntico"
                ]
            ]
        }
    ]

    for r in rows:
        # Category label box
        cat = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x[0], r["y"], col_w[0], r["h"])
        cat.fill.solid()
        cat.fill.fore_color.rgb = WHITE
        cat.line.color.rgb = BORDER_GRAY
        tf = cat.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = r["name"]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        p.alignment = PP_ALIGN.CENTER

        for col_i in range(4):
            c_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x[col_i+1], r["y"], col_w[col_i], r["h"])
            c_box.fill.solid()
            # Highlight current month with subtle tint
            if col_i == 0:
                c_box.fill.fore_color.rgb = RGBColor(254, 243, 199) # soft amber tint for current
                c_box.line.color.rgb = ORANGE
                c_box.line.width = Pt(1.5)
            else:
                c_box.fill.fore_color.rgb = WHITE
                c_box.line.color.rgb = BORDER_GRAY
                c_box.line.width = Pt(1)

            tf = c_box.text_frame
            tf.word_wrap = True
            lines = r["content"][col_i]
            for l_idx, line in enumerate(lines):
                if l_idx == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = line
                p.font.size = Pt(9.5)
                p.font.color.rgb = NAVY if col_i == 0 else DARK_BLUE
                if col_i == 0:
                    p.font.bold = True
                p.space_after = Pt(3)

    # -------------------------------------------------------------
    # SLIDE 3: MONTHLY SCHEDULE (Cronograma Executivo Mensal)
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    bg3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = LIGHT_BG
    bg3.line.fill.background()

    # Header
    header3 = slide3.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
    tf3 = header3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "PROJETO QAI • X-TESTING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p2 = tf3.add_paragraph()
    p2.text = "Schedule Executivo & Marcos de Progresso (Mês a Mês)"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = NAVY

    # Schedule Table Container
    # 4 month columns + Activity Column
    sched_x = [Inches(0.8), Inches(4.5), Inches(6.7), Inches(8.9), Inches(11.1)]
    sched_w = [Inches(3.5), Inches(2.1), Inches(2.1), Inches(2.1), Inches(2.1)]
    
    table_top = Inches(1.7)
    table_hdr_h = Inches(0.5)

    # Header row
    hdr_titles = ["Work Package / Trilha de Execução", "SET/2026 (Atual)", "OUT/2026", "NOV/2026", "DEZ/2026"]
    hdr_colors = [NAVY, ORANGE, PRIMARY_BLUE, PURPLE, GREEN]

    for idx, (hx, hw, ht, hc) in enumerate(zip(sched_x, sched_w, hdr_titles, hdr_colors)):
        h_shape = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, hx, table_top, hw, table_hdr_h)
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = hc
        h_shape.line.fill.background()
        tf = h_shape.text_frame
        p = tf.paragraphs[0]
        p.text = ht
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    schedule_rows = [
        {
            "wp": "WP1 • Infraestrutura & Paperclip\nAmbiente agêntico e governança",
            "cells": [
                {"text": "100% CONCLUÍDO\n• Paperclip ativo\n• QAI configurado", "status": "done"},
                {"text": "Operação Contínua\n• Monitoramento", "status": "ongoing"},
                {"text": "Operação Contínua\n• Manutenção", "status": "ongoing"},
                {"text": "Operação Contínua\n• Governança", "status": "ongoing"}
            ]
        },
        {
            "wp": "WP2 • Extração de Requisitos & BPMN\nTree-RAG sem chunking e modelagem",
            "cells": [
                {"text": "100% CONCLUÍDO\n• Árvore SANASA\n• Skill BPMN", "status": "done"},
                {"text": "Refinamento\n• Novos fluxos", "status": "plan"},
                {"text": "Suporte a E2E\n• Validação", "status": "plan"},
                {"text": "Migração p/ Mobile\n• Especificações", "status": "plan"}
            ]
        },
        {
            "wp": "WP3 • FASE 1: WEB Testes Manuais\nSuporte IA para TestLink e Mantis",
            "cells": [
                {"text": "Em Andamento\n• Prioridades\n• Matriz de Riscos", "status": "active"},
                {"text": "EXECUÇÃO PLENA\n• Suíte TestLink\n• Triagem Mantis", "status": "target"},
                {"text": "Estabilização\n• Homologação", "status": "plan"},
                {"text": "Fase Concluída\n• Transição", "status": "plan"}
            ]
        },
        {
            "wp": "WP4 • FASE 2: WEB Integração & E2E\nAutomação autônoma Playwright",
            "cells": [
                {"text": "Planejamento\n• Spike arquitetura", "status": "plan"},
                {"text": "Desenvolvimento\n• Conectores E2E", "status": "plan"},
                {"text": "EXECUÇÃO PLENA\n• Automação E2E\n• Evidências vídeo", "status": "target"},
                {"text": "Fase Concluída\n• Regressão ativa", "status": "plan"}
            ]
        },
        {
            "wp": "WP5 • FASE 3: MOBILE (Todos)\nNativo pós-conclusão de WEB",
            "cells": [
                {"text": "Bloqueado\n(Aguardando WEB)", "status": "blocked"},
                {"text": "Bloqueado\n(Aguardando WEB)", "status": "blocked"},
                {"text": "Preparação\n• Setup device farm", "status": "plan"},
                {"text": "EXECUÇÃO PLENA\n• Testes Manuais &\n• Integração Mobile", "status": "target"}
            ]
        }
    ]

    row_y = table_top + table_hdr_h + Inches(0.08)
    row_h = Inches(0.95)

    for r_idx, r in enumerate(schedule_rows):
        curr_y = row_y + r_idx * (row_h + Inches(0.06))
        
        # WP Title Box
        wp_box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, sched_x[0], curr_y, sched_w[0], row_h)
        wp_box.fill.solid()
        wp_box.fill.fore_color.rgb = WHITE
        wp_box.line.color.rgb = BORDER_GRAY
        tf = wp_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = r["wp"]
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY

        for c_idx, cell in enumerate(r["cells"]):
            c_box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, sched_x[c_idx+1], curr_y, sched_w[c_idx+1], row_h)
            c_box.fill.solid()
            
            # Styling by status
            if cell["status"] == "done":
                c_box.fill.fore_color.rgb = RGBColor(220, 252, 231) # green tint
                c_box.line.color.rgb = GREEN
            elif cell["status"] == "active":
                c_box.fill.fore_color.rgb = RGBColor(254, 243, 199) # amber tint
                c_box.line.color.rgb = ORANGE
                c_box.line.width = Pt(1.5)
            elif cell["status"] == "target":
                c_box.fill.fore_color.rgb = RGBColor(239, 246, 255) # blue tint
                c_box.line.color.rgb = PRIMARY_BLUE
            elif cell["status"] == "blocked":
                c_box.fill.fore_color.rgb = RGBColor(241, 245, 249) # gray
                c_box.line.color.rgb = BORDER_GRAY
            else:
                c_box.fill.fore_color.rgb = WHITE
                c_box.line.color.rgb = BORDER_GRAY

            tf = c_box.text_frame
            tf.word_wrap = True
            lines = cell["text"].split("\n")
            for l_i, l_txt in enumerate(lines):
                if l_i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = l_txt
                p.font.size = Pt(9)
                if l_i == 0:
                    p.font.bold = True
                p.font.color.rgb = DARK_BLUE
                p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 4: TAREFAS REALIZADAS (2x2 Dashboard Grid)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    bg4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = LIGHT_BG
    bg4.line.fill.background()

    # Header
    header4 = slide4.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(1.1))
    tf4 = header4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "PROJETO QAI • FÁBRICA DE TESTES X-TESTING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p2 = tf4.add_paragraph()
    p2.text = "Tarefas Realizadas"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = NAVY

    p3 = tf4.add_paragraph()
    p3.text = "Estruturação dos Agentes Operacionais, Demandas Paperclip, Entregáveis RF046/RF047 e Decisões de Continuidade"
    p3.font.size = Pt(11)
    p3.font.color.rgb = GRAY_TEXT

    # 2x2 Grid Coordinates
    c_w = Inches(5.69)
    c_h = Inches(2.6)
    c_x1 = Inches(0.8)
    c_x2 = Inches(6.84)
    c_y1 = Inches(1.65)
    c_y2 = Inches(4.45)

    # CARD 1 (Top-Left): Criação e Configuração de Agentes
    card1 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x1, c_y1, c_w, c_h)
    card1.fill.solid()
    card1.fill.fore_color.rgb = WHITE
    card1.line.color.rgb = BORDER_GRAY
    card1.line.width = Pt(1.2)

    acc1 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x1 + Inches(0.18), c_y1 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc1.fill.solid()
    acc1.fill.fore_color.rgb = PRIMARY_BLUE
    acc1.line.fill.background()

    tb1 = slide4.shapes.add_textbox(c_x1 + Inches(0.18), c_y1 + Inches(0.24), c_w - Inches(0.36), c_h - Inches(0.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "ESTRUTURA OPERACIONAL • 5 AGENTES"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p_t = tf1.add_paragraph()
    p_t.text = "Criação e Configuração de Agentes"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_t.space_after = Pt(4)

    agents = [
        ("QAI (CEO)", "Liderança executiva, governança e validação final da esteira."),
        ("Gerência de Projetos", "Planejamento de sprints, gestão de backlog e prazos."),
        ("Análise de Processos", "Modelagem BPMN 2.0 dos fluxos e regras de negócio."),
        ("Análise de Testes", "Especificação de cenários e suítes completas TestLink."),
        ("Testador", "Execução WEB/Playwright, evidências e reporte de defeitos.")
    ]
    for ag_n, ag_r in agents:
        pa = tf1.add_paragraph()
        pa.text = f"•  {ag_n}: {ag_r}"
        pa.font.size = Pt(9)
        pa.font.color.rgb = DARK_BLUE
        pa.space_after = Pt(2)

    # CARD 2 (Bottom-Left): 33 Tarefas Registradas
    card2 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x1, c_y2, c_w, c_h)
    card2.fill.solid()
    card2.fill.fore_color.rgb = WHITE
    card2.line.color.rgb = BORDER_GRAY
    card2.line.width = Pt(1.2)

    acc2 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x1 + Inches(0.18), c_y2 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc2.fill.solid()
    acc2.fill.fore_color.rgb = GREEN
    acc2.line.fill.background()

    tb2 = slide4.shapes.add_textbox(c_x1 + Inches(0.18), c_y2 + Inches(0.24), c_w - Inches(0.36), c_h - Inches(0.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "PAINEL DE DEMANDAS NO PAPERCLIP"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = GREEN

    p_t = tf2.add_paragraph()
    p_t.text = "33 Tarefas Registradas"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_t.space_after = Pt(4)

    tasks_info = [
        ("✔ 15 Concluídas (45.5%):", "Especificações TestLink, BPMNs e planilhas de divergência de 5 OSs (RF002, RF027, RF043, RF050 e RF058/RF061).", GREEN),
        ("⛔ 6 Bloqueadas (18.2%):", "Impedimento por falta de credenciais externas/homologação SANASA (ex.: XTE-18 execução CS-01..10, XTE-16, XTE-23).", ORANGE),
        ("⏳ 12 Em Revisão / Backlog (36.3%):", "Validações técnicas de artefatos, automação de conectores e saneamento de regras da Fase 1.", PRIMARY_BLUE)
    ]
    for tag_txt, desc_txt, col in tasks_info:
        pt = tf2.add_paragraph()
        pt.text = tag_txt
        pt.font.size = Pt(9.5)
        pt.font.bold = True
        pt.font.color.rgb = col
        pd = tf2.add_paragraph()
        pd.text = desc_txt
        pd.font.size = Pt(9)
        pd.font.color.rgb = DARK_BLUE
        pd.space_after = Pt(3)

    # CARD 3 (Top-Right): Entregáveis Demanda RF046/RF047
    card3 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x2, c_y1, c_w, c_h)
    card3.fill.solid()
    card3.fill.fore_color.rgb = WHITE
    card3.line.color.rgb = BORDER_GRAY
    card3.line.width = Pt(1.2)

    acc3 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x2 + Inches(0.18), c_y1 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc3.fill.solid()
    acc3.fill.fore_color.rgb = TEAL
    acc3.line.fill.background()

    tb3 = slide4.shapes.add_textbox(c_x2 + Inches(0.18), c_y1 + Inches(0.24), c_w - Inches(0.36), c_h - Inches(0.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "DEMANDA SANASA • OS 2026/2652"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = TEAL

    p_t = tf3.add_paragraph()
    p_t.text = "Entregáveis da Demanda RF046/RF047"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_t.space_after = Pt(4)

    rf_items = [
        ("📄 RF046-RF047-Julgamento-Desclassificacao.bpmn", "Modelagem BPMN 2.0 formal de regras e saneamento."),
        ("📄 RF046-RF047-Documentacao-BPMN.md", "Documentação técnica completa e conformidade com Lei 14.133."),
        ("📄 RF046-RF047-Suite-Testes-TestLink.xml", "Suíte padronizada com 15 casos estruturados (SANASAPV2-71..85)."),
        ("📄 RF046-RF047-Planilha-Divergencia-SANASA.csv", "Matriz de conferência com 27 requisitos avaliados.")
    ]
    for fn, fd in rf_items:
        pf = tf3.add_paragraph()
        pf.text = f"{fn}: {fd}"
        pf.font.size = Pt(9)
        pf.font.color.rgb = DARK_BLUE
        pf.space_after = Pt(2)
    pl = tf3.add_paragraph()
    pl.text = "🔗 Artefatos versionados no repositório GitHub (openclaw-x-integration)"
    pl.font.size = Pt(8.5)
    pl.font.color.rgb = PRIMARY_BLUE
    pl.font.underline = True

    # CARD 4 (Bottom-Right): Decisões para Seguir Implementando
    card4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x2, c_y2, c_w, c_h)
    card4.fill.solid()
    card4.fill.fore_color.rgb = WHITE
    card4.line.color.rgb = BORDER_GRAY
    card4.line.width = Pt(1.2)

    acc4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x2 + Inches(0.18), c_y2 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc4.fill.solid()
    acc4.fill.fore_color.rgb = ORANGE
    acc4.line.fill.background()

    tb4 = slide4.shapes.add_textbox(c_x2 + Inches(0.18), c_y2 + Inches(0.24), c_w - Inches(0.36), c_h - Inches(0.3))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "PROATIVIDADE & BYPASS TÉCNICO"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = ORANGE

    p_t = tf4.add_paragraph()
    p_t.text = "Decisões para Seguir Implementando"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_t.space_after = Pt(4)

    decisions = [
        ("1. Validação WEB via Mocks Locais (Playwright):", "Execução das suítes de teste diretamente contra os fluxos modelados com emulação/mocks via Playwright, eliminando a espera passiva por liberação de infraestrutura externa."),
        ("2. Pacotes de Exportação Estruturada para o Mantis:", "Defeitos mapeados (MANTIS-SANASA-1045..1048) gerados em pacotes estruturados (XML/JSON/CSV) pré-formatados para carga em lote imediata assim que as credenciais forem liberadas.")
    ]
    for dt, dd in decisions:
        pdt = tf4.add_paragraph()
        pdt.text = dt
        pdt.font.size = Pt(9.5)
        pdt.font.bold = True
        pdt.font.color.rgb = NAVY
        pdd = tf4.add_paragraph()
        pdd.text = dd
        pdd.font.size = Pt(9)
        pdd.font.color.rgb = DARK_BLUE
        pdd.space_after = Pt(3)

    # -------------------------------------------------------------
    # SLIDE 5: PRÓXIMAS TAREFAS (3 Vertical Cards)
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    bg5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = LIGHT_BG
    bg5.line.fill.background()

    # Header
    header5 = slide5.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(1.1))
    tf5 = header5.text_frame
    tf5.word_wrap = True
    p = tf5.paragraphs[0]
    p.text = "PROJETO QAI • PLANEJAMENTO & GOVERNANÇA AGÊNTICA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p2 = tf5.add_paragraph()
    p2.text = "Próximas Tarefas"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = NAVY

    p3 = tf5.add_paragraph()
    p3.text = "Mapeamento Operacional, Skills de Compliance Regulatório e Prontidão para Auditoria de IA"
    p3.font.size = Pt(11)
    p3.font.color.rgb = GRAY_TEXT

    # 3 Cards Side-by-Side (Mesmo padrão do Slide 1)
    card_width5 = Inches(3.64)
    card_gap5 = Inches(0.38)
    left_margin5 = Inches(0.8)
    top_pos5 = Inches(1.7)
    card_height5 = Inches(5.2)

    tasks_cards = [
        {
            "tag": "ALINHAMENTO OPERACIONAL",
            "title": "Detalhamento do Fluxo X-Testing",
            "sub": "Imersão e Diagnóstico da Esteira Atual",
            "color": ORANGE,
            "items": [
                "Reunião técnica com a liderança e equipe da X-Testing.",
                "Mapeamento detalhado da esteira atual de testes manuais e rituais operacionais.",
                "Levantamento de critérios de aceite, triagem de defeitos e transição para esteira autônoma.",
                "Mapeamento de critérios de passagem, geração de massa de teste e homologação.",
                "Identificação de gargalos operacionais e pontos de atrito para automação imediata.",
                "Definição de interfaces de colaboração entre analistas humanos e agentes de IA."
            ]
        },
        {
            "tag": "PRIVACIDADE & SEGURANÇA",
            "title": "Skills de Compliance dos Agentes",
            "sub": "LGPD • GDPR • HIPAA • CCPA • SOC 2 • ISO 27001 • PCI-DSS",
            "color": PRIMARY_BLUE,
            "items": [
                "Pesquisa e arquitetura de skills para comportamento seguro dos agentes.",
                "Técnicas de Anonimização & Pseudonimização (K2View, Protecto.ai): mascaramento dinâmico, tokenização e hashing irreversível com sal.",
                "Diretrizes Oficiais ANPD & UFCA: aplicação dos padrões regulatórios brasileiros para desidentificação de dados.",
                "Tarjamento de Evidências (MavenDoc): censura automatizada de PII (CPFs, nomes, valores) em screenshots e PDFs de teste.",
                "Coleta Segura & OSINT Ético (OSINT Brasil): higiene de dados para evitar vazamento de credenciais e dados em prompts."
            ]
        },
        {
            "tag": "GOVERNANÇA REGULATÓRIA",
            "title": "Prontidão para Auditoria de IA",
            "sub": "SOC 2 AI • IA GDPR • ISO 27001 IA",
            "color": PURPLE,
            "items": [
                "SOC 2 AI: Controles de integridade, confidencialidade, auditabilidade de inferências e trilhas de auditoria imutáveis.",
                "IA GDPR / LGPD: Minimização de dados em prompts, política de zero-data retention com LLMs e explicabilidade das decisões.",
                "ISO 27001 IA: Gestão de riscos de IA, inventário de modelos e controles de segurança da informação (ref: Mukul975 / GetClaudeSkills).",
                "Procedural Gates: Barreira de checagem automática que bloqueia qualquer ação externa não-conforme antes da persistência ou envio."
            ]
        }
    ]

    for i, tc in enumerate(tasks_cards):
        c_left = left_margin5 + i * (card_width5 + card_gap5)
        
        # Card Background
        c_shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, top_pos5, card_width5, card_height5)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = WHITE
        c_shape.line.color.rgb = BORDER_GRAY
        c_shape.line.width = Pt(1.5)

        # Top Accent Line
        acc = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), top_pos5 + Inches(0.18), Inches(1.2), Inches(0.06))
        acc.fill.solid()
        acc.fill.fore_color.rgb = tc["color"]
        acc.line.fill.background()

        # Text Frame
        tb = slide5.shapes.add_textbox(c_left + Inches(0.2), top_pos5 + Inches(0.32), card_width5 - Inches(0.4), card_height5 - Inches(0.45))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tc["tag"]
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = tc["color"]

        pt = tf.add_paragraph()
        pt.text = tc["title"]
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = NAVY
        pt.space_after = Pt(2)

        ps = tf.add_paragraph()
        ps.text = tc["sub"]
        ps.font.size = Pt(8.5)
        ps.font.bold = True
        ps.font.color.rgb = GRAY_TEXT
        ps.space_after = Pt(10)

        for it in tc["items"]:
            pi = tf.add_paragraph()
            pi.text = f"•  {it}"
            pi.font.size = Pt(9)
            pi.font.color.rgb = DARK_BLUE
            pi.space_after = Pt(6)

    os.makedirs("artifacts/x-testing", exist_ok=True)
    out_path = "artifacts/x-testing/status-report-qai-2026-09.pptx"
    prs.save(out_path)
    print(f"PPTX saved successfully to {out_path}")

if __name__ == "__main__":
    create_deck()
