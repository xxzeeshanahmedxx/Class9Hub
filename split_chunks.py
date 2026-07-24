import pikepdf
import os

pdfs = [
    ("9th-Math.pdf", 288),
    ("9th-Physics.pdf", 200),
    ("9th-Chemistry.pdf", 192),
    ("9th-Urdu.pdf", 144),
    ("9th-Biology.pdf", 180),
    ("9th-English.pdf", 168),
]

SRC = r'D:\Downloads\9th Books'
DST = r'D:\Downloads\9th Books\chunks'
os.makedirs(DST, exist_ok=True)

CHUNK_SIZE = 50

for fname, total_pages in pdfs:
    path = os.path.join(SRC, fname)
    pdf = pikepdf.open(path)
    base = fname.replace('.pdf', '')
    
    for start in range(0, total_pages, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, total_pages)
        part = start // CHUNK_SIZE + 1
        out_name = f"{base}-part{part}.pdf"
        out_path = os.path.join(DST, out_name)
        
        if os.path.exists(out_path):
            print(f"SKIP (exists): {out_name}")
            continue
        
        dst = pikepdf.Pdf.new()
        for i in range(start, end):
            dst.pages.append(pdf.pages[i])
        dst.save(out_path)
        dst.close()
        size_mb = os.path.getsize(out_path) / 1024 / 1024
        print(f"OK: {out_name} (pages {start+1}-{end}, {size_mb:.1f} MB)")
    
    pdf.close()

print("\nDone!")
