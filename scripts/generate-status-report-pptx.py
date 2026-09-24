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

    # -------------------------------------------------------------
    # BRAND COLORS (X-Testing Brand Guidelines)
    # -------------------------------------------------------------
    GREEN_PRIMARY = RGBColor(56, 118, 29)    # #38761D (Verde Institucional Principal)
    GREEN_ACCENT = RGBColor(80, 149, 70)     # #509546 (Verde Vivo / Acento)
    GREEN_LIGHT = RGBColor(106, 168, 79)     # #6AA84F (Verde Claro)
    GREEN_DARK = RGBColor(39, 78, 19)        # #274E13 (Verde Escuro)
    ORANGE_ALERT = RGBColor(255, 87, 34)     # #FF5722 (Laranja Destaque / Badges)
    DARK_TEXT = RGBColor(26, 26, 26)         # #1A1A1A (Grafite / Quase Preto)
    GRAY_SUBTITLE = RGBColor(127, 127, 127)  # #7F7F7F (Cinza Subtítulo)
    GRAY_BORDER = RGBColor(216, 216, 216)    # #D8D8D8 (Borda Neutra)
    LIGHT_BG = RGBColor(248, 250, 248)       # #F8FAF8 (Fundo Off-White Suave)
    CARD_BG = RGBColor(255, 255, 255)        # #FFFFFF (Branco Puro)
    BLUE_REF = RGBColor(21, 96, 130)         # #156082 (Azul do tema corporativo)

    LOGO_PATH = os.path.abspath(r"artifacts\x-testing\assets\image2.png")
    SEAL_PATH = os.path.abspath(r"artifacts\x-testing\assets\image3.png")

    FONT_FAMILY = "Raleway"

    def apply_header(slide, section_tag, title_text, subtitle_text):
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = LIGHT_BG
        bg.line.fill.background()

        # Top decorative thin line (brand green)
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = GREEN_PRIMARY
        top_line.line.fill.background()

        # Header box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.5), Inches(1.15))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.name = FONT_FAMILY
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ORANGE_ALERT

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_TEXT

        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_FAMILY
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = GRAY_SUBTITLE

        # Logo on Top-Right
        if os.path.exists(LOGO_PATH):
            slide.shapes.add_picture(LOGO_PATH, Inches(10.8), Inches(0.4), width=Inches(1.75))

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tff = footer_box.text_frame
        tff.margin_left = tff.margin_top = tff.margin_right = tff.margin_bottom = 0
        pf = tff.paragraphs[0]
        pf.text = "PROJETO QAI • FÁBRICA DE TESTES X-TESTING  |  ESTEIRA DE QUALIDADE & SANASA  |  WWW.XTESTING.COM.BR"
        pf.font.name = FONT_FAMILY
        pf.font.size = Pt(8)
        pf.font.bold = True
        pf.font.color.rgb = RGBColor(160, 160, 160)

    # -------------------------------------------------------------
    # SLIDE 1: KEY OBJECTIVES & ESTRATÉGIA DE FASES
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    apply_header(slide1, "01 / ESTRATÉGIA OPERACIONAL", "Key Objectives & Estratégia de Fases", 
                 "Evolução da operação de testes manuais para esteira autônoma com agentes de IA (OpenClaw + Paperclip)")

    phases = [
        {
            "num": "01",
            "phase": "FASE 01",
            "title": "WEB: Testes Manuais",
            "tag": "EM ANDAMENTO • BASELINE",
            "color": GREEN_PRIMARY,
            "desc": "Espelhamento dos papéis operacionais e automação do suporte à execução manual.",
            "items": [
                "Extração estruturada de requisitos (Tree-RAG / PageIndex)",
                "Geração de fluxos e regras em BPMN 2.0 formal",
                "Elaboração automatizada de Casos de Teste (TestLink)",
                "Triagem e pré-preenchimento de defeitos (Mantis)"
            ]
        },
        {
            "num": "02",
            "phase": "FASE 02",
            "title": "WEB: Integração & Aceitação",
            "tag": "PLANEJADA • SEQUENCIAL",
            "color": GREEN_ACCENT,
            "desc": "Automação E2E com execução autônoma no navegador e evidências rastreáveis.",
            "items": [
                "Execução agêntica via Playwright / Camoufox",
                "Validação de integração de APIs e regras de negócio",
                "Geração de evidências com prints e vídeos por passo",
                "Pipeline de regressão contínua integrada ao CI/CD"
            ]
        },
        {
            "num": "03",
            "phase": "FASE 03",
            "title": "MOBILE: Todos os Anteriores",
            "tag": "CONDICIONAL • PÓS-WEB",
            "color": ORANGE_ALERT,
            "desc": "Transposição do ecossistema agêntico completo para aplicações mobile nativas.",
            "items": [
                "Início condicionado ao término das Fases 01 e 02",
                "Testes funcionais, usabilidade e fluxos de tela nativos",
                "Integração e testes de aceitação em Android/iOS",
                "Automação agêntica em dispositivos reais e emuladores"
            ]
        }
    ]

    c_w = Inches(3.64)
    c_gap = Inches(0.4)
    c_top = Inches(1.75)
    c_h = Inches(5.1)

    for i, p_info in enumerate(phases):
        c_left = Inches(0.8) + i * (c_w + c_gap)
        
        # Card Background
        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, c_top, c_w, c_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = GRAY_BORDER
        card.line.width = Pt(1.2)

        # Top Accent Line
        acc = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), c_top + Inches(0.18), Inches(1.2), Inches(0.06))
        acc.fill.solid()
        acc.fill.fore_color.rgb = p_info["color"]
        acc.line.fill.background()

        # Text Frame
        tb = slide1.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.35), c_w - Inches(0.4), c_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = f"{p_info['phase']}  •  {p_info['num']}"
        p_num.font.name = FONT_FAMILY
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = p_info["color"]

        p_t = tf.add_paragraph()
        p_t.text = p_info["title"]
        p_t.font.name = FONT_FAMILY
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = DARK_TEXT
        p_t.space_after = Pt(4)

        p_tag = tf.add_paragraph()
        p_tag.text = p_info["tag"]
        p_tag.font.name = FONT_FAMILY
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = p_info["color"]
        p_tag.space_after = Pt(10)

        p_desc = tf.add_paragraph()
        p_desc.text = p_info["desc"]
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = GRAY_SUBTITLE
        p_desc.space_after = Pt(14)

        for it in p_info["items"]:
            pi = tf.add_paragraph()
            pi.text = f"•  {it}"
            pi.font.name = FONT_FAMILY
            pi.font.size = Pt(9.5)
            pi.font.color.rgb = DARK_TEXT
            pi.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 2: ROADMAP (Set/2026 a Dez/2026)
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    apply_header(slide2, "02 / ROADMAP ESTRATÉGICO", "Product Stages Roadmap (Setembro - Dezembro 2026)",
                 "Evolução estruturada em 4 etapas bimestrais com entregas tangíveis e critérios de avanço")

    col_x = [Inches(0.8), Inches(2.8), Inches(5.4), Inches(8.0), Inches(10.6)]
    col_w = [Inches(1.8), Inches(2.45), Inches(2.45), Inches(2.45), Inches(2.45)]

    months = [
        {"num": "1", "name": "Setembro 2026", "sub": "Setup & Baseline", "color": GREEN_PRIMARY},
        {"num": "2", "name": "Outubro 2026", "sub": "WEB Manuais", "color": GREEN_ACCENT},
        {"num": "3", "name": "Novembro 2026", "sub": "WEB Integração", "color": BLUE_REF},
        {"num": "4", "name": "Dezembro 2026", "sub": "Mobile & Escala", "color": ORANGE_ALERT}
    ]

    stage_header_top = Inches(1.7)
    stage_header_h = Inches(0.65)

    cat_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x[0], stage_header_top, col_w[0], stage_header_h)
    cat_box.fill.solid()
    cat_box.fill.fore_color.rgb = CARD_BG
    cat_box.line.color.rgb = GRAY_BORDER
    tf = cat_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Our Approach"
    p.font.name = FONT_FAMILY
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_TEXT
    p.alignment = PP_ALIGN.CENTER

    for idx, m in enumerate(months):
        m_box = slide2.shapes.add_shape(MSO_SHAPE.CHEVRON, col_x[idx+1], stage_header_top, col_w[idx], stage_header_h)
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = m["color"]
        m_box.line.fill.background()
        tf = m_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{m['num']}. {m['name']}"
        p.font.name = FONT_FAMILY
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    rows = [
        {
            "name": "Strategic\nObjectives",
            "y": Inches(2.45),
            "h": Inches(1.45),
            "content": [
                ["• Instalar Paperclip & estruturar XTE", "• Baseline agêntico com QAI (CEO)", "• Rastreabilidade sem chunking"],
                ["• Operar WEB Testes Manuais", "• Automatizar geração de TC / Mantis", "• Integrar conectores ALM"],
                ["• Automação WEB Integração/E2E", "• Execução autônoma Playwright", "• Validação contínua de regras"],
                ["• Kickoff esteira MOBILE", "• Transpor skills para apps nativos", "• Homologação completa"]
            ]
        },
        {
            "name": "Key\nMilestones",
            "y": Inches(4.0),
            "h": Inches(1.45),
            "content": [
                ["• Ambiente Paperclip 100% ativo", "• Tree-RAG SANASA indexado", "• Skill de BPMN validada"],
                ["• 1º Ciclo de testes gerado por IA", "• Geração de CTs no TestLink", "• Validação com time SANASA"],
                ["• Bateria de testes E2E executada", "• Cobertura de regras críticas", "• Evidências visuais auditáveis"],
                ["• Matriz de testes Mobile pronta", "• Execução emuladores/reais", "• Handover operacional 2027"]
            ]
        },
        {
            "name": "Deliverables",
            "y": Inches(5.55),
            "h": Inches(1.45),
            "content": [
                ["• Planilha de Classificação / Riscos", "• sanasa-requirements-tree.json", "• Segmentos SSC no Memory Viewer"],
                ["• Suíte TestLink gerada por IA", "• Relatório de aderência manual", "• Dashboards operacionais QAI"],
                ["• Scripts Playwright automatizados", "• Pipeline de testes WEB ativa", "• Relatórios de bugs no Mantis"],
                ["• Suíte Mobile completa (Fase 3)", "• Relatório consolidado de KPIs", "• Manual operacional agêntico"]
            ]
        }
    ]

    for r in rows:
        cat = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x[0], r["y"], col_w[0], r["h"])
        cat.fill.solid()
        cat.fill.fore_color.rgb = CARD_BG
        cat.line.color.rgb = GRAY_BORDER
        tf = cat.text_frame
        p = tf.paragraphs[0]
        p.text = r["name"]
        p.font.name = FONT_FAMILY
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.alignment = PP_ALIGN.CENTER

        for col_i in range(4):
            c_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x[col_i+1], r["y"], col_w[col_i], r["h"])
            c_box.fill.solid()
            if col_i == 0:
                c_box.fill.fore_color.rgb = RGBColor(237, 247, 237) # Verde institucional sutil
                c_box.line.color.rgb = GREEN_PRIMARY
                c_box.line.width = Pt(1.5)
            else:
                c_box.fill.fore_color.rgb = CARD_BG
                c_box.line.color.rgb = GRAY_BORDER
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
                p.font.name = FONT_FAMILY
                p.font.size = Pt(9)
                p.font.color.rgb = GREEN_DARK if col_i == 0 else DARK_TEXT
                if col_i == 0:
                    p.font.bold = True
                p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 3: MONTHLY SCHEDULE & TRACKING
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    apply_header(slide3, "03 / CRONOGRAMA EXECUTIVO", "Schedule Executivo & Marcos de Progresso (Mês a Mês)",
                 "Acompanhamento sistemático por Work Packages alinhados aos marcos contratuais e técnicos")

    sched_x = [Inches(0.8), Inches(4.5), Inches(6.7), Inches(8.9), Inches(11.1)]
    sched_w = [Inches(3.5), Inches(2.1), Inches(2.1), Inches(2.1), Inches(2.1)]
    
    table_top = Inches(1.7)
    table_hdr_h = Inches(0.5)

    hdr_titles = ["Work Package / Trilha de Execução", "SET/2026 (Atual)", "OUT/2026", "NOV/2026", "DEZ/2026"]
    hdr_colors = [DARK_TEXT, GREEN_PRIMARY, GREEN_ACCENT, BLUE_REF, ORANGE_ALERT]

    for idx, (hx, hw, ht, hc) in enumerate(zip(sched_x, sched_w, hdr_titles, hdr_colors)):
        h_shape = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, hx, table_top, hw, table_hdr_h)
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = hc
        h_shape.line.fill.background()
        tf = h_shape.text_frame
        p = tf.paragraphs[0]
        p.text = ht
        p.font.name = FONT_FAMILY
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    schedule_rows = [
        {
            "wp": "WP1 • Setup Agêntico & Paperclip\nAmbiente, organograma e governança QAI",
            "cells": [
                {"text": "100% CONCLUÍDO\n• Paperclip ativo\n• Empresa XTE configurada", "status": "done"},
                {"text": "Operação Contínua\n• Monitoramento", "status": "ongoing"},
                {"text": "Operação Contínua\n• Manutenção", "status": "ongoing"},
                {"text": "Operação Contínua\n• Governança", "status": "ongoing"}
            ]
        },
        {
            "wp": "WP2 • Extração de Requisitos & BPMN\nTree-RAG sem chunking e fluxos de negócio",
            "cells": [
                {"text": "100% CONCLUÍDO\n• Árvore de requisitos\n• Skill BPMN validada", "status": "done"},
                {"text": "Refinamento\n• Novos fluxos", "status": "plan"},
                {"text": "Suporte a E2E\n• Validação cruzada", "status": "plan"},
                {"text": "Migração p/ Mobile\n• Mapeamento", "status": "plan"}
            ]
        },
        {
            "wp": "WP3 • FASE 1: WEB Testes Manuais\nSuporte IA para TestLink e Mantis",
            "cells": [
                {"text": "Em Andamento\n• Matriz prioridades\n• Riscos SANASA", "status": "active"},
                {"text": "EXECUÇÃO PLENA\n• Suíte TestLink\n• Triagem Mantis", "status": "target"},
                {"text": "Estabilização\n• Homologação", "status": "plan"},
                {"text": "Fase Concluída\n• Transição", "status": "plan"}
            ]
        },
        {
            "wp": "WP4 • FASE 2: WEB Integração & E2E\nAutomação autônoma Playwright / Camoufox",
            "cells": [
                {"text": "Planejamento\n• Spike arquitetura", "status": "plan"},
                {"text": "Desenvolvimento\n• Conectores E2E", "status": "plan"},
                {"text": "EXECUÇÃO PLENA\n• Automação E2E\n• Evidências vídeo", "status": "target"},
                {"text": "Fase Concluída\n• Regressão ativa", "status": "plan"}
            ]
        },
        {
            "wp": "WP5 • FASE 3: MOBILE (Todos)\nTestes manuais e automação em apps nativos",
            "cells": [
                {"text": "Bloqueado\n(Aguardando WEB)", "status": "blocked"},
                {"text": "Bloqueado\n(Aguardando WEB)", "status": "blocked"},
                {"text": "Preparação\n• Setup device farm", "status": "plan"},
                {"text": "EXECUÇÃO PLENA\n• Testes Manuais &\n• E2E Mobile", "status": "target"}
            ]
        }
    ]

    row_y = table_top + table_hdr_h + Inches(0.08)
    row_h = Inches(0.92)

    for r_idx, r in enumerate(schedule_rows):
        curr_y = row_y + r_idx * (row_h + Inches(0.06))
        
        wp_box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, sched_x[0], curr_y, sched_w[0], row_h)
        wp_box.fill.solid()
        wp_box.fill.fore_color.rgb = CARD_BG
        wp_box.line.color.rgb = GRAY_BORDER
        tf = wp_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = r["wp"]
        p.font.name = FONT_FAMILY
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT

        for c_idx, cell in enumerate(r["cells"]):
            c_box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, sched_x[c_idx+1], curr_y, sched_w[c_idx+1], row_h)
            c_box.fill.solid()
            
            if cell["status"] == "done":
                c_box.fill.fore_color.rgb = RGBColor(237, 247, 237)
                c_box.line.color.rgb = GREEN_PRIMARY
                c_box.line.width = Pt(1.2)
            elif cell["status"] == "active":
                c_box.fill.fore_color.rgb = RGBColor(255, 243, 238)
                c_box.line.color.rgb = ORANGE_ALERT
                c_box.line.width = Pt(1.5)
            elif cell["status"] == "target":
                c_box.fill.fore_color.rgb = RGBColor(240, 249, 240)
                c_box.line.color.rgb = GREEN_ACCENT
            elif cell["status"] == "blocked":
                c_box.fill.fore_color.rgb = RGBColor(245, 245, 245)
                c_box.line.color.rgb = GRAY_BORDER
            else:
                c_box.fill.fore_color.rgb = CARD_BG
                c_box.line.color.rgb = GRAY_BORDER

            tf = c_box.text_frame
            tf.word_wrap = True
            lines = cell["text"].split("\n")
            for l_i, l_txt in enumerate(lines):
                if l_i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = l_txt
                p.font.name = FONT_FAMILY
                p.font.size = Pt(8.5)
                if l_i == 0:
                    p.font.bold = True
                p.font.color.rgb = DARK_TEXT
                p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 4: TAREFAS REALIZADAS (2x2 Grid)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    apply_header(slide4, "04 / STATUS DA OPERAÇÃO", "Tarefas Realizadas",
                 "Estruturação dos Agentes Operacionais, Demandas Paperclip, Entregáveis RF046/RF047 e Decisões de Continuidade")

    grid_w = Inches(5.69)
    grid_h = Inches(2.55)
    gx1 = Inches(0.8)
    gx2 = Inches(6.84)
    gy1 = Inches(1.68)
    gy2 = Inches(4.38)

    # CARD 1: Criação e Configuração de Agentes
    card1 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx1, gy1, grid_w, grid_h)
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = GRAY_BORDER
    card1.line.width = Pt(1.2)

    acc1 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx1 + Inches(0.18), gy1 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc1.fill.solid()
    acc1.fill.fore_color.rgb = GREEN_PRIMARY
    acc1.line.fill.background()

    tb1 = slide4.shapes.add_textbox(gx1 + Inches(0.18), gy1 + Inches(0.24), grid_w - Inches(0.36), grid_h - Inches(0.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "ESTRUTURA OPERACIONAL • 5 AGENTES"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = GREEN_PRIMARY

    p_t = tf1.add_paragraph()
    p_t.text = "Criação e Configuração de Agentes"
    p_t.font.name = FONT_FAMILY
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_TEXT
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
        pa.font.name = FONT_FAMILY
        pa.font.size = Pt(9)
        pa.font.color.rgb = DARK_TEXT
        pa.space_after = Pt(2)

    # CARD 2: Entregáveis Demanda RF046/RF047
    card2 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx2, gy1, grid_w, grid_h)
    card2.fill.solid()
    card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = GRAY_BORDER
    card2.line.width = Pt(1.2)

    acc2 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx2 + Inches(0.18), gy1 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc2.fill.solid()
    acc2.fill.fore_color.rgb = GREEN_ACCENT
    acc2.line.fill.background()

    tb2 = slide4.shapes.add_textbox(gx2 + Inches(0.18), gy1 + Inches(0.24), grid_w - Inches(0.36), grid_h - Inches(0.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "DEMANDA SANASA • OS 2026/2652"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT

    p_t = tf2.add_paragraph()
    p_t.text = "Entregáveis da Demanda RF046/RF047"
    p_t.font.name = FONT_FAMILY
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_TEXT
    p_t.space_after = Pt(4)

    rf_items = [
        ("📄 RF046-RF047-Julgamento-Desclassificacao.bpmn", "Modelagem BPMN 2.0 formal de regras e saneamento."),
        ("📄 RF046-RF047-Documentacao-BPMN.md", "Documentação técnica completa e conformidade com Lei 14.133."),
        ("📄 RF046-RF047-Suite-Testes-TestLink.xml", "Suíte padronizada com 15 casos estruturados (SANASAPV2-71..85)."),
        ("📄 RF046-RF047-Planilha-Divergencia-SANASA.csv", "Matriz de conferência com 27 requisitos avaliados.")
    ]
    for fn, fd in rf_items:
        pf = tf2.add_paragraph()
        pf.text = f"{fn}: {fd}"
        pf.font.name = FONT_FAMILY
        pf.font.size = Pt(9)
        pf.font.color.rgb = DARK_TEXT
        pf.space_after = Pt(2)
    pl = tf2.add_paragraph()
    pl.text = "🔗 Artefatos versionados no repositório GitHub (openclaw-x-integration)"
    pl.font.name = FONT_FAMILY
    pl.font.size = Pt(8.5)
    pl.font.color.rgb = GREEN_PRIMARY
    pl.font.underline = True

    # CARD 3: 33 Tarefas Registradas
    card3 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx1, gy2, grid_w, grid_h)
    card3.fill.solid()
    card3.fill.fore_color.rgb = CARD_BG
    card3.line.color.rgb = GRAY_BORDER
    card3.line.width = Pt(1.2)

    acc3 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx1 + Inches(0.18), gy2 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc3.fill.solid()
    acc3.fill.fore_color.rgb = GREEN_DARK
    acc3.line.fill.background()

    tb3 = slide4.shapes.add_textbox(gx1 + Inches(0.18), gy2 + Inches(0.24), grid_w - Inches(0.36), grid_h - Inches(0.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "PAINEL DE DEMANDAS NO PAPERCLIP"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = GREEN_DARK

    p_t = tf3.add_paragraph()
    p_t.text = "33 Tarefas Registradas"
    p_t.font.name = FONT_FAMILY
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_TEXT
    p_t.space_after = Pt(4)

    tasks_info = [
        ("✔ 15 Concluídas (45.5%):", "Especificações TestLink, BPMNs e planilhas de divergência de 5 OSs (RF002, RF027, RF043, RF050 e RF058/RF061).", GREEN_PRIMARY),
        ("⛔ 6 Bloqueadas (18.2%):", "Impedimento por falta de credenciais externas/homologação SANASA (ex.: XTE-18 execução CS-01..10, XTE-16, XTE-23).", ORANGE_ALERT),
        ("⏳ 12 Em Revisão / Backlog (36.3%):", "Validações técnicas de artefatos, automação de conectores e saneamento de regras da Fase 1.", BLUE_REF)
    ]
    for tag_txt, desc_txt, col in tasks_info:
        pt = tf3.add_paragraph()
        pt.text = tag_txt
        pt.font.name = FONT_FAMILY
        pt.font.size = Pt(9.5)
        pt.font.bold = True
        pt.font.color.rgb = col
        pd = tf3.add_paragraph()
        pd.text = desc_txt
        pd.font.name = FONT_FAMILY
        pd.font.size = Pt(9)
        pd.font.color.rgb = DARK_TEXT
        pd.space_after = Pt(3)

    # CARD 4: Decisões para Seguir Implementando
    card4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx2, gy2, grid_w, grid_h)
    card4.fill.solid()
    card4.fill.fore_color.rgb = CARD_BG
    card4.line.color.rgb = GRAY_BORDER
    card4.line.width = Pt(1.2)

    acc4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx2 + Inches(0.18), gy2 + Inches(0.14), Inches(1.2), Inches(0.05))
    acc4.fill.solid()
    acc4.fill.fore_color.rgb = ORANGE_ALERT
    acc4.line.fill.background()

    tb4 = slide4.shapes.add_textbox(gx2 + Inches(0.18), gy2 + Inches(0.24), grid_w - Inches(0.36), grid_h - Inches(0.3))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "PROATIVIDADE & BYPASS TÉCNICO"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = ORANGE_ALERT

    p_t = tf4.add_paragraph()
    p_t.text = "Decisões para Seguir Implementando"
    p_t.font.name = FONT_FAMILY
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_TEXT
    p_t.space_after = Pt(4)

    decisions = [
        ("1. Validação WEB via Mocks Locais (Playwright):", "Execução das suítes de teste diretamente contra os fluxos modelados com emulação/mocks via Playwright, eliminando a espera passiva por liberação de infraestrutura externa."),
        ("2. Pacotes de Exportação Estruturada para o Mantis:", "Defeitos mapeados (MANTIS-SANASA-1045..1048) gerados em pacotes estruturados (XML/JSON/CSV) pré-formatados para carga em lote imediata assim que as credenciais forem liberadas.")
    ]
    for dt, dd in decisions:
        pdt = tf4.add_paragraph()
        pdt.text = dt
        pdt.font.name = FONT_FAMILY
        pdt.font.size = Pt(9.5)
        pdt.font.bold = True
        pdt.font.color.rgb = DARK_TEXT
        pdd = tf4.add_paragraph()
        pdd.text = dd
        pdd.font.name = FONT_FAMILY
        pdd.font.size = Pt(9)
        pdd.font.color.rgb = DARK_TEXT
        pdd.space_after = Pt(3)

    # -------------------------------------------------------------
    # SLIDE 5: PRÓXIMAS TAREFAS (3 Vertical Cards)
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    apply_header(slide5, "05 / PLANEJAMENTO & GOVERNANÇA", "Próximas Tarefas",
                 "Mapeamento Operacional, Skills de Compliance Regulatório e Prontidão para Auditoria de IA")

    card_width5 = Inches(3.64)
    card_gap5 = Inches(0.4)
    top_pos5 = Inches(1.75)
    card_height5 = Inches(5.1)

    tasks_cards = [
        {
            "tag": "ALINHAMENTO OPERACIONAL",
            "title": "Detalhamento do Fluxo X-Testing",
            "sub": "Imersão e Diagnóstico da Esteira Atual",
            "color": GREEN_PRIMARY,
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
            "color": GREEN_ACCENT,
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
            "color": ORANGE_ALERT,
            "items": [
                "SOC 2 AI: Controles de integridade, confidencialidade, auditabilidade de inferências e trilhas de auditoria imutáveis.",
                "IA GDPR / LGPD: Minimização de dados em prompts, política de zero-data retention com LLMs e explicabilidade das decisões.",
                "ISO 27001 IA: Gestão de riscos de IA, inventário de modelos e controles de segurança da informação (ref: Mukul975 / GetClaudeSkills).",
                "Procedural Gates: Barreira de checagem automática que bloqueia qualquer ação externa não-conforme antes da persistência ou envio."
            ]
        }
    ]

    for i, tc in enumerate(tasks_cards):
        c_left = Inches(0.8) + i * (card_width5 + card_gap5)
        
        c_shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, top_pos5, card_width5, card_height5)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = CARD_BG
        c_shape.line.color.rgb = GRAY_BORDER
        c_shape.line.width = Pt(1.2)

        acc = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), top_pos5 + Inches(0.18), Inches(1.2), Inches(0.06))
        acc.fill.solid()
        acc.fill.fore_color.rgb = tc["color"]
        acc.line.fill.background()

        tb = slide5.shapes.add_textbox(c_left + Inches(0.2), top_pos5 + Inches(0.32), card_width5 - Inches(0.4), card_height5 - Inches(0.45))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tc["tag"]
        p.font.name = FONT_FAMILY
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = tc["color"]

        pt = tf.add_paragraph()
        pt.text = tc["title"]
        pt.font.name = FONT_FAMILY
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = DARK_TEXT
        pt.space_after = Pt(2)

        ps = tf.add_paragraph()
        ps.text = tc["sub"]
        ps.font.name = FONT_FAMILY
        ps.font.size = Pt(8.5)
        ps.font.bold = True
        ps.font.color.rgb = GRAY_SUBTITLE
        ps.space_after = Pt(10)

        for it in tc["items"]:
            pi = tf.add_paragraph()
            pi.text = f"•  {it}"
            pi.font.name = FONT_FAMILY
            pi.font.size = Pt(9)
            pi.font.color.rgb = DARK_TEXT
            pi.space_after = Pt(6)

    os.makedirs("artifacts/x-testing", exist_ok=True)
    out_path = "artifacts/x-testing/status-report-qai-2026-09.pptx"
    prs.save(out_path)
    print(f"PPTX saved successfully to {out_path}")

if __name__ == "__main__":
    create_deck()
