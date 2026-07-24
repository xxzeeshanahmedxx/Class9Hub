import pikepdf

pdf_path = r'D:\Downloads\9th Books\9th-Math.pdf'
pdf = pikepdf.open(pdf_path)

chapters = [
    "Real Numbers", "Logarithms", "Sets & Functions", "Factorization",
    "Linear Equations", "Trigonometry", "Coordinate Geometry", "Logic",
    "Similar Figures", "Graphs of Functions", "Construction of Triangles",
    "Statistics", "Probability", "Resources"
]

# Try to find each chapter title in the PDF text content
import re

for i, page in enumerate(pdf.pages):
    text = ""
    try:
        contents = page.get('/Contents')
        if contents:
            if isinstance(contents, pikepdf.Array):
                for content in contents:
                    if content:
                        try:
                            data = content.read_bytes()
                            text += data.decode('latin-1')
                        except:
                            pass
                    else:
                        pass
            elif contents:
                try:
                    data = contents.read_bytes()
                    text = data.decode('latin-1')
                except:
                    pass
    except:
        pass
    
    # Check for chapter-like patterns (simple text search)
    text_lower = text.lower()
    for ch_name in chapters:
        if ch_name.lower() in text_lower:
            print(f"Page {i+1}: Found '{ch_name}'")
    
    # Also check for "Chapter X" or "Unit X" patterns
    if re.search(r'(chapter|unit)\s*\d+', text_lower):
        print(f"Page {i+1}: {text[:200]}")
