#!/usr/bin/env python3
"""Download source texts from Project Gutenberg.

One place, one method, so every source in the corpus is fetched the same
way and is reproducible.  Gutenberg's plain-text endpoint is:

    https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt

Some older ids redirect; we follow redirects and verify we got prose and
not an error page.
"""
import os
import sys
import time
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "data", "sources")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) HistoricalKitchen/1.0 "
                  "(recipe research; contact via GitHub Pages repo)",
    "Accept": "text/plain,*/*",
}


def fetch(book_id, subdir, force=False):
    out_dir = os.path.join(ROOT, subdir)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"pg{book_id}.txt")
    if os.path.exists(out) and os.path.getsize(out) > 2000 and not force:
        return book_id, os.path.getsize(out), "cached"

    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            text = data.decode("utf-8", errors="replace")
            # sanity: real Gutenberg text has this marker or at least prose
            if len(text) < 2000:
                raise ValueError(f"too small ({len(text)} bytes)")
            if "PG" not in text[:3000] and len(text) < 8000:
                raise ValueError("looks like an error page, not a book")
            with open(out, "w", encoding="utf-8") as f:
                f.write(text)
            return book_id, len(text), "ok"
        except Exception as e:
            if attempt == 2:
                return book_id, 0, f"FAIL: {e}"
            time.sleep(2 + attempt * 2)
    return book_id, 0, "FAIL"


def main():
    plan = {}
    for line in sys.argv[1:]:
        if "=" not in line:
            continue
        subdir, ids = line.split("=", 1)
        plan[subdir] = [int(x) for x in ids.split(",") if x.strip()]

    total = 0
    ok = 0
    for subdir, ids in plan.items():
        for bid in ids:
            bid, size, status = fetch(bid, subdir)
            total += 1
            if size:
                ok += 1
            print(f"{subdir:10} pg{bid:<6} {size:>9} bytes  {status}", flush=True)
            time.sleep(0.4)
    print(f"\n{ok}/{total} fetched")
    if ok < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
