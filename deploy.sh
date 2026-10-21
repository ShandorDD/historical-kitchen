#!/usr/bin/env bash
# Deploy The Historical Kitchen to GitHub Pages.
# Pattern matches the existing eJoe_SF270_helper repo: index.html at repo
# root, Pages served from the main branch.
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
rm -rf .git
git init -q -b main
git config user.name  "ShandorDD"
git config user.email "ShandorDD@users.noreply.github.com"

cat > .gitignore <<'EOF'
__pycache__/
*.pyc
EOF

git add index.html build.py data/ .gitignore README.md 2>/dev/null || git add index.html build.py data/ .gitignore
git commit -q -m "The Historical Kitchen: 29 sourced recipes, era filter, pantry matching, scaling"

# --- create the repo if it is not there yet
if ! curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $TOKEN" \
     "https://api.github.com/repos/$OWNER/$REPO" | grep -q 200; then
  echo "Creating repo $OWNER/$REPO..."
  curl -s -X POST -H "Authorization: token $TOKEN" \
       -H "Content-Type: application/json" \
       -d "{\"name\":\"$REPO\",\"description\":\"Cook 2,000 years of history from what is already in your kitchen. Era filter, pantry matching, modern substitutes, scaling.\",\"private\":false,\"has_pages\":true}" \
       "https://api.github.com/user/repos" -o /tmp/createrepo.json -w "HTTP %{http_code}\n"
else
  echo "Repo $OWNER/$REPO already exists."
fi

git remote add origin "https://github.com/$OWNER/$REPO.git"
git push -q -u origin main
echo "Pushed main."

# --- enable Pages (legacy build, served from main root)
curl -s -X POST -H "Authorization: token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"source":{"branch":"main","path":"/"}}' \
     "https://api.github.com/repos/$OWNER/$REPO/pages" \
     -o /tmp/pages.json -w "Pages API: HTTP %{http_code}\n"
cat /tmp/pages.json | head -c 400; echo
echo "---"
echo "URL: https://$OWNER.github.io/$REPO/"
