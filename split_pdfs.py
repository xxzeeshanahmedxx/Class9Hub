import pikepdf

pdf_path = r'D:\Downloads\9th Books\9th-Math.pdf'
pdf = pikepdf.open(pdf_path)

root = pdf.Root
print("Root keys:", list(root.keys()))

outlines = root['/Outlines']
print("Outlines keys:", list(outlines.keys()))

def walk(item, depth=0):
    if item is None:
        return
    if isinstance(item, pikepdf.Array):
        for sub in item:
            walk(sub, depth)
    elif isinstance(item, pikepdf.Dictionary):
        title = str(item.get('/Title', '?'))
        dest = None
        pg = None
        if '/Dest' in item:
            dest = item['/Dest']
        if '/A' in item and '/D' in item['/A']:
            dest = item['/A']['/D']
        if dest is not None:
            if isinstance(dest, pikepdf.Array) and len(dest) >= 2:
                pg = str(dest[1])
            elif hasattr(dest, '__getitem__'):
                try:
                    pg = str(dest[0])
                except:
                    pg = str(dest)
            else:
                pg = str(dest)
        page_label = pg or ''
        print(f"{'  ' * depth}{title} -> page={page_label}")
        if '/First' in item:
            walk(item['/First'], depth + 1)
        if '/Next' in item:
            walk(item['/Next'], depth)

first = outlines.get('/First')
print("First outline:", first)
walk(first)
