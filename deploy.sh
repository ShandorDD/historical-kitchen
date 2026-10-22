#!/usr/bin/env bash
# Deploy The Historical Kitchen to GitHub Pages.
#
# Pattern matches the existing eJoe_SF270_helper repo: index.html at repo
# root, Pages served from the main branch.
#
# NOTE: an earlier version of this script did `rm -rf .git` and re-initialised
# the repository every time.  That destroys the commit history and, on a repo
# that already exists on GitHub, the push is rejected as non-fast-forward --
# so the second deploy silently does nothing.  This version commits on top of
# the existing history instead.  It also triggers a Pages build explicitly,
# because a push alone does not always kick one off.
set -euo pipefail

PROJ=/home/haus/historical-kitchen
REPO=historical-kitchen
OWNER=ShandorDD
TOKEN_FILE=$HOME/.config/hermes/github_token

if [[ ! -f "$TOKEN_FILE" ]]; then
  echo "FATAL: no token at $TOKEN_FILE" >&2
  exit 1
fi
TOKEN=$(cat "$TOKEN_FILE")

cd "$PROJ"

# --- build first, always
python3 build.py

# --- keep the repo lean: only the page + its sources
cat > .gitignore <<'EOF'
__pycache__/
*.pyc

# The downloaded Project Gutenberg source texts are large (56 MB) and
# fully reproducible from fetch_sources.py + the ids in the extraction
# scripts. Keep them out of the repository; the app only needs the
# generated JSON.
data/sources/

# Raw intermediates between extraction and conversion.
region_raw.json
novels_food.json
EOF

git add -A index.html build.py data/ .gitignore README.md *.py *.json 2>/dev/null || true
git add -A

if git diff --cached --quiet; then
  echo "Nothing to commit; the tree is already deployed."
else
  git commit -q -m "${1:-Update The Historical Kitchen}"
  echo "Committed $(git rev-parse --short HEAD)."
fi

# --- create the repo if it is not there yet
if ! curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $TOKEN" \
     "https://api.github.com/repos/$OWNER/$REPO" | grep -q 200; then
  echo "Creating repo $OWNER/$REPO..."
  curl -s -X POST -H "Authorization: token $TOKEN" \
       -H "Content-Type: application/json" \
       -d "{\"name\":\"$REPO\",\"description\":\"Cook 2,000 years of history from what is already in your kitchen. Era filter, pantry matching, modern substitutes, scaling.\",\"private\":false,\"has_pages\":true}" \
       "https://api.github.com/user/repos" -o /tmp/createrepo.json -w "HTTP %{http_code}\n"
  git remote add origin "https://github.com/$OWNER/$REPO.git"
fi

git push origin main
echo "Pushed main."

# --- enable Pages (legacy build, served from main root)
curl -s -X POST -H "Authorization: token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"source":{"branch":"main","path":"/"}}' \
     "https://api.github.com/repos/$OWNER/$REPO/pages" \
     -o /tmp/pages.json -w "Pages API: HTTP %{http_code}\n"

# --- trigger a build explicitly.  A push does not always start one, and a
# --- site that still serves the old file looks exactly like a failed deploy.
curl -s -X POST -H "Authorization: token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"source":{"branch":"main","path":"/"}}' \
     "https://api.github.com/repos/$OWNER/$REPO/pages/builds" \
     -o /tmp/build.json -w "Build API: HTTP %{http_code}\n"

echo "---"
echo "URL: https://$OWNER.github.io/$REPO/"
echo "Waiting for the Pages build, then verifying the LIVE file..."
echo

# --- verify the live artefact, not the local tree.  A build that was never
# --- deployed is not "done", and the only honest check is the served file.
URL="https://$OWNER.github.io/$REPO/"
LOCAL_HASH=$(md5sum "$PROJ/index.html" | cut -d' ' -f1)
for i in $(seq 1 30); do
  sleep 10
  curl -sL "$URL" -o /tmp/live_deploy.html || true
  LIVE_HASH=$(md5sum /tmp/live_deploy.html 2>/dev/null | cut -d' ' -f1)
  if [[ "$LIVE_HASH" == "$LOCAL_HASH" ]]; then
    echo "LIVE MATCHES LOCAL after $((i*10))s -- deploy verified."
    exit 0
  fi
  echo "  ${i}: live=$LIVE_HASH local=$LOCAL_HASH (build still running?)"
done

echo "WARNING: the live file still does not match the local build." >&2
echo "Check the Pages build status:" >&2
echo "  curl -s -H 'Authorization: token \$TOKEN' \\" >&2
echo "    https://api.github.com/repos/$OWNER/$REPO/pages/builds/latest" >&2
exit 1
