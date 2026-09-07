from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "manuscript"
DIST = ROOT / "dist"
OUTPUT = DIST / "FDE橙皮书-从业务问题到生产系统-v1.0.docx"

ORANGE = "F47C20"
ORANGE_DARK = "C95700"
INK = "1F2937"
MUTED = "6B7280"
CREAM = "FFF7ED"
LIGHT = "F3F4F6"
WHITE = "FFFFFF"
BODY_FONT = "Noto Sans SC"
HEAD_FONT = "Noto Sans SC"


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_geometry(table, widths_dxa: list[int]) -> None:
    total = sum(widths_dxa)
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(total))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), "120")
    tbl_ind.set(qn("w:type"), "dxa")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths_dxa:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)
    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.find(qn("w:tcW"))
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:w"), str(widths_dxa[min(idx, len(widths_dxa) - 1)]))
            tc_w.set(qn("w:type"), "dxa")
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def new_decimal_numbering(doc: Document) -> int:
    numbering = doc.part.numbering_part.element
    abstract_ids = [int(x.get(qn("w:abstractNumId"))) for x in numbering.findall(qn("w:abstractNum"))]
    abstract_id = max(abstract_ids, default=-1) + 1
    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)
    level = OxmlElement("w:lvl")
    level.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), "decimal")
    lvl_text = OxmlElement("w:lvlText")
    lvl_text.set(qn("w:val"), "%1.")
    suffix = OxmlElement("w:suff")
    suffix.set(qn("w:val"), "tab")
    p_pr = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "540")
    tabs.append(tab)
    indent = OxmlElement("w:ind")
    indent.set(qn("w:left"), "540")
    indent.set(qn("w:hanging"), "270")
    p_pr.extend([tabs, indent])
    level.extend([start, num_fmt, lvl_text, suffix, p_pr])
    abstract.append(level)
    numbering.append(abstract)
    nums = [int(x.get(qn("w:numId"))) for x in numbering.findall(qn("w:num"))]
    num_id = max(nums, default=0) + 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract_ref = OxmlElement("w:abstractNumId")
    abstract_ref.set(qn("w:val"), str(abstract_id))
    num.append(abstract_ref)
    numbering.append(num)
    return num_id


def apply_decimal_numbering(paragraph, num_id: int) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_id_node = OxmlElement("w:numId")
    num_id_node.set(qn("w:val"), str(num_id))
    num_pr.extend([ilvl, num_id_node])
    p_pr.append(num_pr)


def set_keep_with_next(paragraph, value=True) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    node = p_pr.find(qn("w:keepNext"))
    if value and node is None:
        p_pr.append(OxmlElement("w:keepNext"))


def set_font(run, name=BODY_FONT, size=None, bold=None, color=None, italic=None) -> None:
    run.font.name = name
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.rFonts
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.insert(0, r_fonts)
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        r_fonts.set(qn(f"w:{key}"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_inline(paragraph, text: str, size=10.5, color=INK) -> None:
    parts = re.split(r"(\*\*.*?\*\*|`.*?`)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            set_font(run, size=size, bold=True, color=color)
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            set_font(run, name="Arial", size=size - 0.5, color=ORANGE_DARK)
            run.font.highlight_color = None
        else:
            run = paragraph.add_run(part)
            set_font(run, size=size, color=color)


def set_repeat_page_field(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("第 ")
    set_font(run, name="Arial", size=8.5, color=MUTED)
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char1, instr, fld_char2])
    end = paragraph.add_run(" 页")
    set_font(end, size=8.5, color=MUTED)


def configure_styles(doc: Document) -> None:
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.25

    for name, size, color, before, after in (
        ("Heading 1", 23, ORANGE_DARK, 0, 14),
        ("Heading 2", 16, INK, 18, 8),
        ("Heading 3", 12.5, ORANGE_DARK, 12, 5),
    ):
        style = styles[name]
        style.font.name = HEAD_FONT
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style._element.rPr.rFonts.set(qn("w:eastAsia"), HEAD_FONT)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.line_spacing = 1.05
        style.paragraph_format.keep_with_next = True

    for list_name in ("List Bullet", "List Number"):
        style = styles[list_name]
        style.font.name = BODY_FONT
        style.font.size = Pt(10.5)
        style._element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
        style.paragraph_format.left_indent = Inches(0.375)
        style.paragraph_format.first_line_indent = Inches(-0.188)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.line_spacing = 1.25


def configure_section(section) -> None:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.82)
    section.bottom_margin = Inches(0.78)
    section.left_margin = Inches(0.88)
    section.right_margin = Inches(0.88)
    section.header_distance = Inches(0.42)
    section.footer_distance = Inches(0.42)
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("FDE ORANGE BOOK  /  从业务问题到生产系统")
    set_font(r, name="Arial", size=8, bold=True, color=MUTED)
    footer = section.footer
    set_repeat_page_field(footer.paragraphs[0])


def add_cover(doc: Document) -> None:
    for _ in range(5):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("FDE ORANGE BOOK")
    set_font(r, name="Arial", size=13, bold=True, color=ORANGE)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("FDE 橙皮书")
    set_font(r, name=HEAD_FONT, size=34, bold=True, color=ORANGE_DARK)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    r = p.add_run("从业务问题到生产系统")
    set_font(r, name=HEAD_FONT, size=20, bold=True, color=INK)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(100)
    r = p.add_run("AI 时代前线部署工程师的认知、方法、技术与成长指南")
    set_font(r, size=12, color=MUTED)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("FIELD METHOD · 2026")
    set_font(r, name="Arial", size=10, bold=True, color=ORANGE)
    doc.add_page_break()


def add_contents(doc: Document, headings: list[tuple[int, str]]) -> None:
    p = doc.add_paragraph(style="Heading 1")
    p.add_run("目录")
    for level, title in headings:
        if title in {"FDE 橙皮书", "目录"}:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0 if level == 1 else 0.28 if level == 2 else 0.55)
        p.paragraph_format.space_after = Pt(2 if level > 1 else 5)
        size = 10.5 if level == 1 else 9.3
        color = ORANGE_DARK if level == 1 else INK
        add_inline(p, title, size=size, color=color)
    doc.add_page_break()


def markdown_headings(files: list[Path]) -> list[tuple[int, str]]:
    result = []
    for file in files:
        for line in file.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^(#{1,3})\s+(.+)$", line)
            if match:
                result.append((len(match.group(1)), match.group(2).strip()))
    return result


def add_markdown_table(doc: Document, rows: list[list[str]]) -> None:
    if len(rows) < 2:
        return
    data_rows = [r for idx, r in enumerate(rows) if idx != 1]
    cols = max(len(r) for r in data_rows)
    table = doc.add_table(rows=len(data_rows), cols=cols)
    table.style = "Table Grid"
    widths = [int(9360 / cols)] * cols
    widths[-1] += 9360 - sum(widths)
    set_table_geometry(table, widths)
    for ridx, source_row in enumerate(data_rows):
        for cidx in range(cols):
            cell = table.cell(ridx, cidx)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            add_inline(p, source_row[cidx].strip() if cidx < len(source_row) else "", size=9.2)
            if ridx == 0:
                set_cell_shading(cell, ORANGE)
                for run in p.runs:
                    run.font.color.rgb = RGBColor.from_string(WHITE)
                    run.bold = True
    set_repeat_table_header(table.rows[0])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def parse_table_row(line: str) -> list[str]:
    return [item.strip() for item in line.strip().strip("|").split("|")]


def add_body(doc: Document, files: list[Path]) -> None:
    first_h1_seen = False
    active_num_id = None
    for file in files:
        lines = file.read_text(encoding="utf-8").splitlines()
        if file.name == "00-frontmatter.md":
            lines = lines[7:]
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            if not line:
                i += 1
                continue
            if line == "---":
                i += 1
                continue
            if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?[\s:|-]+\|?$", lines[i + 1]):
                active_num_id = None
                table_rows = [parse_table_row(line), parse_table_row(lines[i + 1])]
                i += 2
                while i < len(lines) and lines[i].startswith("|"):
                    table_rows.append(parse_table_row(lines[i]))
                    i += 1
                add_markdown_table(doc, table_rows)
                continue
            heading = re.match(r"^(#{1,3})\s+(.+)$", line)
            if heading:
                active_num_id = None
                level = len(heading.group(1))
                title = heading.group(2).strip()
                if level == 1:
                    if first_h1_seen:
                        doc.add_page_break()
                    first_h1_seen = True
                p = doc.add_paragraph(style=f"Heading {level}")
                add_inline(p, title, size={1: 23, 2: 16, 3: 12.5}[level], color=ORANGE_DARK if level != 2 else INK)
                if level == 1:
                    p.paragraph_format.space_before = Pt(18)
                    bar = doc.add_paragraph()
                    bar.paragraph_format.space_after = Pt(18)
                    p_pr = bar._p.get_or_add_pPr()
                    p_bdr = OxmlElement("w:pBdr")
                    bottom = OxmlElement("w:bottom")
                    bottom.set(qn("w:val"), "single")
                    bottom.set(qn("w:sz"), "18")
                    bottom.set(qn("w:space"), "1")
                    bottom.set(qn("w:color"), ORANGE)
                    p_bdr.append(bottom)
                    p_pr.append(p_bdr)
                i += 1
                continue
            if line.startswith("> "):
                active_num_id = None
                table = doc.add_table(rows=1, cols=1)
                table.style = "Table Grid"
                set_table_geometry(table, [9360])
                # Treat the single-row callout as its semantic header so assistive
                # tooling does not interpret it as an unlabeled data table.
                set_repeat_table_header(table.rows[0])
                cell = table.cell(0, 0)
                set_cell_shading(cell, CREAM)
                cell.text = ""
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                add_inline(p, line[2:].strip(), size=10.5, color=ORANGE_DARK)
                doc.add_paragraph().paragraph_format.space_after = Pt(1)
                i += 1
                continue
            bullet = re.match(r"^-\s+(.+)$", line)
            numbered = re.match(r"^\d+\.\s+(.+)$", line)
            if bullet or numbered:
                if bullet:
                    active_num_id = None
                    p = doc.add_paragraph(style="List Bullet")
                else:
                    if active_num_id is None:
                        active_num_id = new_decimal_numbering(doc)
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Inches(0.375)
                    p.paragraph_format.first_line_indent = Inches(-0.188)
                    p.paragraph_format.space_after = Pt(4)
                    p.paragraph_format.line_spacing = 1.25
                    apply_decimal_numbering(p, active_num_id)
                add_inline(p, (bullet or numbered).group(1))
                i += 1
                continue
            # Merge adjacent prose lines only when Markdown uses a wrapped paragraph.
            para_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,3})\s|^-\s|^\d+\.\s|^>\s|^\|", lines[i]):
                para_lines.append(lines[i].strip())
                i += 1
            text = " ".join(para_lines)
            active_num_id = None
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Inches(0.22)
            p.paragraph_format.widow_control = True
            add_inline(p, text)


def build() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    files = sorted(MANUSCRIPT.glob("*.md"))
    doc = Document()
    configure_styles(doc)
    for section in doc.sections:
        configure_section(section)
    add_cover(doc)
    add_contents(doc, markdown_headings(files))
    add_body(doc, files)
    core = doc.core_properties
    core.title = "FDE 橙皮书：从业务问题到生产系统"
    core.subject = "AI 时代前线部署工程师的认知、方法、技术与成长指南"
    core.keywords = "FDE, Forward Deployed Engineer, AI, Agent, Evals, 企业 AI"
    core.comments = "v1.0, 2026-08"
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
