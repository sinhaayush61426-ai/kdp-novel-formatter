import os
import re
from docx import Document
from weasyprint import HTML, CSS

def build_kdp_pdf(docx_filename, output_pdf_filename):
    if not os.path.exists(docx_filename):
        print(f"Error: Could not find manuscript file '{docx_filename}'.")
        return

    print(f"Reading manuscript from {docx_filename}...")
    doc = Document(docx_filename)
    
    # Base HTML template shell
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    </head>
    <body>
    """

    # --- FRONT MATTER ---
    html_content += """
        <div class="front-page">
            <div class="book-title">THE LAST SIGNAL</div>
            <div class="book-subtitle">A NOVEL</div>
            <div class="author-name">[AUTHOR NAME]</div>
        </div>
        <div class="copyright-page">
            <p><strong>The Last Signal</strong></p>
            <p>Copyright © 2026 by [Author Name]. All rights reserved.</p>
            <p>This is a work of fiction. Names, characters, places, and incidents are products of the author's imagination.</p>
            <p>ISBN: [Insert Paperback ISBN]</p>
        </div>
        <div class="dedication-page">
            <p>For [Insert Dedication Name],<br>who kept the signal alive.</p>
        </div>
    """

    # --- PARSE MANUSCRIPT PARAGRAPHS ---
    current_chapter_open = False
    chapter_regex = re.compile(r'^(Chapter\s+\d+)\s*(?:---|[-–—])\s*(.*)', re.IGNORECASE)
    
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
            
        # Detect Chapter Headings & Split Number from Title
        match = chapter_regex.match(text)
        if match or p.style.name.startswith("Heading 2") and text.startswith("Chapter"):
            if current_chapter_open:
                html_content += "</div>\n"
            
            if match:
                ch_num = match.group(1)
                ch_title = match.group(2).strip('"“”')
            else:
                ch_num = text
                ch_title = ""

            html_content += f'<div class="chapter">\n'
            html_content += f'<div class="chapter-header-container">\n'
            html_content += f'  <div class="chapter-number">{ch_num}</div>\n'
            html_content += f'  <hr class="chapter-rule">\n'
            if ch_title:
                html_content += f'  <div class="chapter-title">{ch_title}</div>\n'
            html_content += f'</div>\n'
            current_chapter_open = True
        else:
            if not current_chapter_open:
                html_content += '<div class="chapter">\n'
                current_chapter_open = True
            html_content += f'<p>{text}</p>\n'

    if current_chapter_open:
        html_content += "</div>\n"

    html_content += "</body></html>"

    print("Compiling print-ready PDF with WeasyPrint...")
    HTML(string=html_content, base_url=".").write_pdf(
        output_pdf_filename,
        stylesheets=[CSS('styles.css')]
    )
    
    print(f"Success! Print-ready KDP PDF generated: {output_pdf_filename}")

if __name__ == "__main__":
    import sys
    input_doc = sys.argv[1] if len(sys.argv) > 1 else "the_last_signal.docx"
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else "the_last_signal_kdp.pdf"
    
    build_kdp_pdf(input_doc, output_pdf)