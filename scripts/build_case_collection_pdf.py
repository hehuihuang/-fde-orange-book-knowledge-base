#!/usr/bin/env python3
"""Build a standalone PDF for the 21 Chinese FDE case articles."""

from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont as FontToolsFont
from fontTools.varLib.instancer import instantiateVariableFont
from markdown_it import MarkdownIt
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'knowledge-base' / '07-中国社区实践' / '08-FDE实战案例文章集.md'
OUT = ROOT / 'dist' / 'FDE实战案例文章集.pdf'
QA = ROOT / 'qa' / 'case-collection'
FONT_SOURCE = ROOT / 'fonts' / 'NotoSansSC.ttf'
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
WIDTH = PAGE_W - MARGIN * 2
MD = MarkdownIt('commonmark', {'html': False}).enable('table')


def register_fonts():
    QA.mkdir(parents=True, exist_ok=True)
    for weight, name in [(400, 'CaseBook'), (700, 'CaseBookBold')]:
        dest = QA / f'NotoSansSC-{weight}.ttf'
        font = FontToolsFont(FONT_SOURCE)
        instantiateVariableFont(font, {'wght': weight}, inplace=True).save(dest)
        pdfmetrics.registerFont(TTFont(name, str(dest)))
    pdfmetrics.registerFontFamily('CaseBook', normal='CaseBook', bold='CaseBookBold', italic='CaseBook', boldItalic='CaseBookBold')


def style(name, **kwargs):
    defaults = dict(fontName='CaseBook', fontSize=10.5, leading=17, textColor=colors.HexColor('#292524'),
                    wordWrap='CJK', alignment=TA_LEFT, spaceAfter=7)
    defaults.update(kwargs)
    return ParagraphStyle(name, **defaults)


STYLES = {
    'h1': style('case-title', fontName='CaseBookBold', fontSize=22, leading=30,
                textColor=colors.HexColor('#C2410C'), spaceBefore=8, spaceAfter=17, keepWithNext=True),
    'h2': style('case-heading', fontName='CaseBookBold', fontSize=14, leading=21,
                textColor=colors.HexColor('#9A3412'), spaceBefore=14, spaceAfter=6, keepWithNext=True),
    'h3': style('case-subheading', fontName='CaseBookBold', fontSize=11.5, leading=18,
                spaceBefore=9, spaceAfter=4, keepWithNext=True),
    'p': style('case-body'),
    'quote': style('case-quote', leftIndent=12, rightIndent=8, textColor=colors.HexColor('#57534E'),
                   borderColor=colors.HexColor('#D6D3D1'), borderWidth=0.5, borderPadding=6,
                   backColor=colors.HexColor('#FFF7ED')),
    'list': style('case-list', leftIndent=14, firstLineIndent=-8, fontSize=10, leading=16),
    'small': style('case-small', fontSize=8.5, leading=13, textColor=colors.HexColor('#57534E')),
}


def inline_html(token):
    if token.type in ('text', 'code_inline'):
        value = escape(token.content)
        if token.type == 'code_inline':
            return f'<font name="Courier">{value}</font>'
        return value
    if token.type == 'softbreak' or token.type == 'hardbreak':
        return '<br/>'
    if token.type == 'image':
        return escape(token.content or '[图片]')
    if token.type == 'link_open':
        attrs = token.attrs or {}
        href = attrs.get('href', '') if isinstance(attrs, dict) else next((value for key, value in attrs if key == 'href'), '')
        return f'<link href="{escape(href).replace(chr(34), "&quot;")}">'
    if token.type == 'link_close':
        return '</link>'
    if token.type == 'strong_open':
        return '<b>'
    if token.type == 'strong_close':
        return '</b>'
    if token.type == 'em_open':
        return '<i>'
    if token.type == 'em_close':
        return '</i>'
    return escape(token.content or '')


def render_inline(token):
    return ''.join(inline_html(child) for child in (token.children or []))


def flowables():
    tokens = MD.parse(SOURCE.read_text(encoding='utf-8'))
    story = []
    list_depth = 0
    ordered = False
    item_index = 0
    for index, token in enumerate(tokens):
        if token.type == 'heading_open':
            continue
        if token.type == 'heading_close':
            continue
        if token.type == 'inline':
            if token.map is None:
                continue
            parent = tokens[index - 1] if index else None
            # The token's tag identifies the containing block in CommonMark output.
            if parent and parent.type == 'heading_open':
                level = int(parent.tag[1:])
                story.append(Paragraph(render_inline(token), STYLES.get(f'h{level}', STYLES['h3'])))
            elif parent and parent.type == 'blockquote_open':
                story.append(Paragraph(render_inline(token), STYLES['quote']))
            elif parent and parent.type == 'list_item_open':
                item_index += 1
                marker = f'{item_index}. ' if ordered else '• '
                story.append(Paragraph(marker + render_inline(token), STYLES['list']))
            else:
                story.append(Paragraph(render_inline(token), STYLES['p']))
            continue
        if token.type == 'bullet_list_open':
            list_depth += 1
            ordered = False
            item_index = 0
            continue
        if token.type == 'ordered_list_open':
            list_depth += 1
            ordered = True
            item_index = 0
            continue
        if token.type in ('bullet_list_close', 'ordered_list_close'):
            list_depth = max(0, list_depth - 1)
            story.append(Spacer(1, 2))
            continue
        if token.type == 'blockquote_open' or token.type == 'blockquote_close':
            continue
        if token.type == 'hr':
            story.append(Spacer(1, 5))
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('CaseBook', 8)
    canvas.setFillColor(colors.HexColor('#78716C'))
    canvas.drawString(MARGIN, 10 * mm, 'FDE橙皮书 · 破局 FDE 实战案例文章集')
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, str(doc.page))
    canvas.restoreState()


def main():
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN, bottomMargin=16 * mm, title='FDE实战案例文章集',
                          author='FDE橙皮书')
    doc.addPageTemplates([PageTemplate(id='cases', frames=[Frame(MARGIN, 16 * mm, WIDTH, PAGE_H - MARGIN - 16 * mm, id='body')], onPage=footer)])
    doc.build(flowables())
    print(f'OK: wrote {OUT} ({OUT.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
