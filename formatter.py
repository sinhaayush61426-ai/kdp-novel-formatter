import os
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
    
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
            
        # Detect Chapter Headings
        if text.startswith("Chapter") or p.style.name.startswith("Heading 2"):
            if current_chapter_open:
                html_content += "</div>\n"
            html_content += f'<div class="chapter">\n<h2 class="chapter-heading">{text}</h2>\n'
            current_chapter_open = True
        else:
            if not current_chapter_open:
                html_content += '<div class="chapter">\n'
                current_chapter_open = True
            html_content += f'<p>{text}</p>\n'

    if current_chapter_open:
        html_content += "</div>\n"

    html_content += "</body></html>"

    # Save temporary HTML for debugging if needed
    with open("temp_book.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Compiling print-ready PDF with WeasyPrint...")
    # Render PDF using external CSS stylesheet
    HTML(string=html_content, base_url=".").write_pdf(
        output_pdf_filename,
        stylesheets=[CSS('styles.css')]
    )
    
    # Cleanup temp file
    if os.path.exists("temp_book.html"):
        os.remove("temp_book.html")
        
    print(f"Success! Print-ready KDP PDF generated: {output_pdf_filename}")

if __name__ == "__main__":
    import sys
    input_doc = sys.argv[1] if len(sys.argv) > 1 else "the_last_signal.docx"
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else "the_last_signal_kdp.pdf"
    
    build_kdp_pdf(input_doc, output_pdf)