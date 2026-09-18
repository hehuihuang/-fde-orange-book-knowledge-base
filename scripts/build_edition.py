#!/usr/bin/env python3
"""Build the book PDF and reading HTML from the same chapter manifest.

uv run --with reportlab --with fonttools --with markdown-it-py --with pypdf \
    python scripts/build_edition.py
"""
from pathlib import Path
import html
import hashlib
import json
import re
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont as FontToolsFont
from fontTools.varLib.instancer import instantiateVariableFont
from markdown_it import MarkdownIt
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak, Table,
    TableStyle, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'book'
OUT = ROOT / 'dist'
QA = ROOT / 'qa' / 'edition3'
META = json.loads((BOOK / 'book.json').read_text())
MD = MarkdownIt('commonmark', {'html': False}).enable('table')
INK = colors.HexColor('#292524')
MUTED = colors.HexColor('#57534E')
ORANGE = colors.HexColor('#C2410C')
PAPER = colors.HexColor('#FFFBEB')
RULE = colors.HexColor('#D6D3D1')
W, H = 170 * mm, 240 * mm
MARGIN = 18 * mm
WIDTH = W - MARGIN * 2


def title_of(name):
    return (BOOK / name).read_text().splitlines()[0].removeprefix('# ')


def register_fonts():
    for weight, name in [(400, 'Book'), (700, 'BookBold')]:
        dest = QA / f'NotoSansSC-{weight}.ttf'
        if not dest.exists():
            font = FontToolsFont(ROOT / 'fonts' / 'NotoSansSC.ttf')
            instantiateVariableFont(font, {'wght': weight}, inplace=True).save(dest)
        pdfmetrics.registerFont(TTFont(name, str(dest)))
    pdfmetrics.registerFontFamily('Book', normal='Book', bold='BookBold', italic='Book', boldItalic='BookBold')


def style(name, **kw):
    defaults = dict(fontName='Book', fontSize=10.5, leading=16.5, textColor=INK,
                    wordWrap='CJK', alignment=TA_LEFT, spaceAfter=6,
                    allowWidows=0, allowOrphans=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


STYLES = {
    'p': style('body'),
    'h1': style('chapter', fontName='BookBold', fontSize=22, leading=31, textColor=ORANGE, spaceBefore=16, spaceAfter=22, keepWithNext=True),
    'h2': style('section', fontName='BookBold', fontSize=13, leading=20, spaceBefore=12, spaceAfter=6, keepWithNext=True),
    'h3': style('subsection', fontName='BookBold', fontSize=11, leading=18, spaceBefore=8, keepWithNext=True),
    'small': style('small', fontSize=8.5, leading=13, textColor=MUTED),
    'cell': style('cell', fontSize=9, leading=14, spaceAfter=0),
    'headcell': style('headcell', fontName='BookBold', fontSize=9, leading=14, textColor=ORANGE, spaceAfter=0),
    'list': style('list', leftIndent=10, firstLineIndent=-8, fontSize=9.5, leading=15),
    'part': style('part', fontName='BookBold', fontSize=27, leading=38, textColor=ORANGE, spaceAfter=24),
}


def inline(tokens):
    result = []
    for token in tokens or []:
        if token.type in ('text', 'code_inline'):
            result.append(escape(token.content))
        elif token.type == 'strong_open': result.append('<b>')
        elif token.type == 'strong_close': result.append('</b>')
        elif token.type == 'em_open': result.append('<i>')
        elif token.type == 'em_close': result.append('</i>')
        elif token.type == 'link_open':
            result.append(f'<link href="{escape(token.attrGet("href"), {chr(34): "&quot;"})}" color="#C2410C">')
        elif token.type == 'link_close': result.append('</link>')
        elif token.type in ('softbreak', 'hardbreak'): result.append(' ')
    return ''.join(result)


def markdown_flow(name, key):
    tokens = MD.parse((BOOK / name).read_text())
    flows = []
    i = 0
    in_list = 0
    source_start = None
    while i < len(tokens):
        t = tokens[i]
        if t.type in ('bullet_list_open', 'ordered_list_open'): in_list += 1
        elif t.type in ('bullet_list_close', 'ordered_list_close'): in_list -= 1
        elif t.type == 'heading_open':
            heading = tokens[i + 1].content
            if heading in ('延伸阅读', '来源与回读'):
                source_start = len(flows)
            p = Paragraph(inline(tokens[i + 1].children), STYLES['h3' if source_start is not None else t.tag])
            if t.tag == 'h1':
                p.toc = (1, title_of(name), key)
            flows.append(p)
            i += 2
        elif t.type == 'paragraph_open':
            s = inline(tokens[i + 1].children)
            paragraph_style = STYLES['small'] if source_start is not None else STYLES['list' if in_list else 'p']
            flows.append(Paragraph(('· ' if in_list else '') + s, paragraph_style))
            i += 2
        elif t.type == 'table_open':
            rows, row, is_head = [], [], False
            i += 1
            while tokens[i].type != 'table_close':
                tok = tokens[i]
                if tok.type == 'tr_open': row = []
                elif tok.type in ('th_open', 'td_open'):
                    is_head = tok.type == 'th_open'
                elif tok.type == 'inline':
                    row.append(Paragraph(inline(tok.children), STYLES['headcell' if is_head else 'cell']))
                elif tok.type == 'tr_close': rows.append(row)
                i += 1
            table = Table(rows, colWidths=[WIDTH / len(rows[0])] * len(rows[0]), repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFEDD5')),
                ('LINEBELOW', (0, 0), (-1, 0), .65, ORANGE),
                ('LINEBELOW', (0, 1), (-1, -1), .25, RULE),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            flows.extend([table, Spacer(1, 10)])
        elif t.type == 'fence':
            flows.append(Paragraph(escape(t.content).replace('\n', '<br/>'), STYLES['small']))
        i += 1
    if source_start is not None:
        flows = flows[:source_start] + [KeepTogether(flows[source_start:])]
    return flows


class BookDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(str(filename), pagesize=(W, H), leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=20 * mm, bottomMargin=19 * mm,
                         title=META['title'], author='FDE橙皮书项目', subject=META['subtitle'])
        self.current_heading = ''
        self.chapter_pages = {}
        frame = Frame(MARGIN, 19 * mm, WIDTH, H - 39 * mm,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='book', frames=frame, onPage=self.decorate, onPageEnd=self.page_end))

    def beforeDocument(self):
        self.current_heading = ''
        self.chapter_pages = {}

    def decorate(self, c, doc):
        c.saveState()
        if doc.page == 1:
            c.setFillColor(ORANGE)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            c.setFillColor(PAPER)
            c.setFont('Book', 9)
            c.drawString(MARGIN, H - 30 * mm, 'FORWARD DEPLOYED ENGINEERING')
            c.setFont('BookBold', 89)
            c.drawString(MARGIN - 2, H - 82 * mm, 'FDE')
            c.setFont('BookBold', 39)
            c.drawString(MARGIN, H - 110 * mm, '橙皮书')
            c.setStrokeColor(PAPER)
            c.setLineWidth(.8)
            c.line(MARGIN, H - 125 * mm, W - MARGIN, H - 125 * mm)
            c.setFont('Book', 13)
            c.drawString(MARGIN, H - 143 * mm, '从业务现场到 AI 系统交付')
            c.setFont('Book', 9)
            for i, line in enumerate(['认识 FDE / 技术基础 / 交付实务 / 案例拆解', '按章阅读 · 27 章 · 公开来源与实践练习']):
                c.drawString(MARGIN, 49 * mm - i * 7 * mm, line)
            c.drawString(MARGIN, 22 * mm, META['edition'])
            c.drawRightString(W - MARGIN, 22 * mm, META['date'])
        else:
            c.setFillColor(colors.HexColor('#FFFEF8'))
            c.rect(0, 0, W, H, fill=1, stroke=0)
        c.restoreState()

    def page_end(self, c, doc):
        c.saveState()
        if doc.page != 1:
            c.setFillColor(MUTED)
            c.setFont('Book', 7.5)
            c.drawString(MARGIN, H - 12 * mm, META['title'])
            label = self.current_heading
            if pdfmetrics.stringWidth(label, 'Book', 7.5) > WIDTH * .7:
                label = label[:27] + '…'
            c.drawRightString(W - MARGIN, H - 12 * mm, label)
            c.setStrokeColor(RULE)
            c.setLineWidth(.35)
            c.line(MARGIN, 14 * mm, W - MARGIN, 14 * mm)
            c.setFont('Book', 8)
            c.drawString(MARGIN, 9 * mm, '从业务现场到 AI 系统交付')
            c.drawRightString(W - MARGIN, 9 * mm, str(doc.page))
        c.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, 'toc'):
            level, label, key = flowable.toc
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(label, key, level=level, closed=False)
            self.notify('TOCEntry', (level, label, self.page, key))
            self.current_heading = label
            self.chapter_pages[key] = self.page


def build_pdf():
    register_fonts()
    doc = BookDoc(OUT / 'FDE橙皮书.pdf')
    story = [Spacer(1, H - 40 * mm), PageBreak()]
    opening = markdown_flow(META['frontmatter'], 'reading')
    opening[0].toc = (0, '阅读说明', 'reading')
    story += opening + [PageBreak(), Paragraph('目录', STYLES['h1'])]
    toc = TableOfContents()
    toc.levelStyles = [
        style('tocpart', fontName='BookBold', fontSize=11, leading=19, textColor=ORANGE, spaceBefore=9, spaceAfter=5),
        style('tocchapter', fontSize=9.5, leading=17, leftIndent=11, firstLineIndent=0, spaceAfter=3),
    ]
    toc.dotsMinLevel = 1
    story += [Paragraph('页码与 PDF 实际页序一致。目录及书签均可点击。', STYLES['small']), toc]
    for pnum, part in enumerate(META['parts'], 1):
        story += [PageBreak(), Spacer(1, 22 * mm)]
        head = Paragraph(part['title'], STYLES['part'])
        head.toc = (0, part['title'], f'part-{pnum}')
        story += [head, Paragraph(part['description'], STYLES['p']), Spacer(1, 16 * mm)]
        for name in part['chapters']:
            story.append(Paragraph(title_of(name), STYLES['small']))
        for name in part['chapters']:
            story += [PageBreak()] + markdown_flow(name, f'ch-{name[:2]}')
    doc.multiBuild(story)
    reader = PdfReader(OUT / 'FDE橙皮书.pdf')
    report = {'pages': len(reader.pages), 'chapter_pages': doc.chapter_pages,
              'chapter_count': sum(len(p['chapters']) for p in META['parts']),
              'characters': sum(len((BOOK / f).read_text()) for p in META['parts'] for f in p['chapters'])}
    (QA / 'build-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    sources = [BOOK / META['frontmatter'], BOOK / 'book.json', ROOT / 'design/reader-template.html', Path(__file__).resolve()]
    sources += [BOOK / f for p in META['parts'] for f in p['chapters']]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    (OUT / 'edition.json').write_text(json.dumps({**META, **report, 'source_sha256': hashes}, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False))


def build_html():
    nav = ['<a href="#home" class="home-link">封面与总目录</a>', '<a href="#reading">阅读说明</a>']
    articles = [f'<article id="reading" hidden>{MD.render((BOOK / META["frontmatter"]).read_text())}</article>']
    contents = []
    all_chapters = [(name, part['title']) for part in META['parts'] for name in part['chapters']]
    for part in META['parts']:
        nav.append(f'<h2>{html.escape(part["title"])}</h2>')
        contents.append(f'<section class="toc-part"><h2>{html.escape(part["title"])}</h2><p>{html.escape(part["description"])}</p><ol>')
        for name in part['chapters']:
            key = f'ch-{name[:2]}'
            title = title_of(name)
            short = re.sub(r'^第 \d+ 章\s*', '', title)
            nav.append(f'<a href="#{key}"><span>{name[:2]}</span>{html.escape(short)}</a>')
            contents.append(f'<li><a href="#{key}"><span>{name[:2]}</span>{html.escape(short)}</a></li>')
            index = [f[0] for f in all_chapters].index(name)
            prev = 'reading' if index == 0 else f'ch-{all_chapters[index - 1][0][:2]}'
            nxt = 'home' if index == len(all_chapters) - 1 else f'ch-{all_chapters[index + 1][0][:2]}'
            label = '返回总目录' if nxt == 'home' else '下一章 →'
            content = MD.render((BOOK / name).read_text())
            articles.append(f'<article id="{key}" hidden><p class="eyebrow">{html.escape(part["title"])}</p>{content}<nav class="chapter-nav" aria-label="章节导航"><a href="#{prev}">← 上一章</a><a href="#{nxt}">{label}</a></nav></article>')
        contents.append('</ol></section>')
    template = (ROOT / 'design' / 'reader-template.html').read_text()
    for key, value in {'NAV': ''.join(nav), 'ARTICLES': ''.join(articles), 'CONTENTS': ''.join(contents), 'EDITION': META['edition'], 'DATE': META['date']}.items():
        template = template.replace('{{' + key + '}}', value)
    (OUT / 'FDE橙皮书.html').write_text(template)
    toc_lines = ['# FDE橙皮书目录', '', '[阅读说明](00-阅读说明.md)', '']
    for part in META['parts']:
        toc_lines += ['## ' + part['title'], '', part['description'], '']
        toc_lines += [f'- [{title_of(f)}]({f})' for f in part['chapters']]
        toc_lines += ['']
    (BOOK / '目录.md').write_text('\n'.join(toc_lines))


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    build_html()
    build_pdf()
