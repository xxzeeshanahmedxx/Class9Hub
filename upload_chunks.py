import os
import requests

token = "{{TOKEN}}"
acct = "1280e3d14604463fb09424beb9ed8400"
src = r'D:\Downloads\9th Books\chunks'

for fname in sorted(os.listdir(src)):
    if not fname.endswith('.pdf'):
        continue
    fpath = os.path.join(src, fname)
    size_mb = os.path.getsize(fpath) / 1024 / 1024

    # Check if already exists via HEAD
    head = requests.head(
        f'https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/class9hub-pdfs/objects/{fname}',
        headers={'Authorization': f'Bearer {token}'}
    )
    if head.status_code == 200:
        print(f"SKIP (exists): {fname} ({size_mb:.1f} MB)")
        continue

    with open(fpath, 'rb') as f:
        r = requests.put(
            f'https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/class9hub-pdfs/objects/{fname}',
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/octet-stream'},
            data=f
        )
    if r.status_code == 200:
        print(f"OK: {fname} ({size_mb:.1f} MB)")
    else:
        print(f"FAIL: {fname} ({r.status_code}): {r.text[:100]}")

print("\nDone!")
