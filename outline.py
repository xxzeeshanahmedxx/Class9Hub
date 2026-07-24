import pikepdf

pdf = pikepdf.open(r'D:\Downloads\9th Books\9th-Math.pdf')

outlines = pdf.Root['/Outlines']
first = outlines['/First']

def walk(item, indent=''):
    if item is None:
        return
    title = str(item['/Title'])
    dest = item.get('/Dest')
    page_num = None
    if dest:
        if isinstance(dest, pikepdf.Array):
            target = dest[0]
            # find page index
            for i, p in enumerate(pdf.pages):
                if p.objgen == target.objgen:
                    page_num = i + 1
                    break
    print(f'{indent}{title} -> page {page_num}')
    child = item.get('/First')
    if child:
        walk(child, indent + '  ')
    nxt = item.get('/Next')
    if nxt:
        walk(nxt, indent)

walk(first)
print(f'\nTotal pages: {len(pdf.pages)}')
