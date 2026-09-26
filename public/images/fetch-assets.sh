#!/usr/bin/env bash
# Récupère les assets réels depuis le site actuel d'ACDC.
# À lancer depuis une machine ayant accès à acdcair.com.au :
#   bash public/images/fetch-assets.sh
set -euo pipefail
BASE="https://acdcair.com.au/wp-content/uploads/2021/07"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

curl -fsSL "$BASE/acdc-airconditioning-logo.png" -o "$DIR/acdc-logo.png"
echo "logo ok"

mkdir -p "$DIR/gallery"
for n in 1 2 3 4 5 6 7 9 10 11 12 13 14 15 16 17 18 19 20 21 22; do
  if curl -fsSL "$BASE/${n}-533x400.jpg" -o "$DIR/gallery/${n}.jpg"; then
    echo "gallery/${n}.jpg ok"
  else
    echo "gallery/${n}.jpg MANQUANT" >&2
  fi
done
