#!/usr/bin/env python3
"""Reduit la fonte variable aux seuls caracteres que le site emploie.

Les pages sont statiques : leur jeu de caracteres est connu au build. On garde
donc uniquement ces glyphes, plus une marge pour les champs de formulaire que
le visiteur remplira.

    python3 tools/subset_font.py
"""
import pathlib
import re
import string

from fontTools import subset

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "fonts" / "open-sans-latin.woff2"
OUT = ROOT / "dist" / "assets" / "open-sans.woff2"


def used_characters():
    chars = set(string.printable)  # ce que le visiteur peut taper dans le formulaire
    for page in (ROOT / "dist").glob("*.html"):
        text = page.read_text(encoding="utf-8")
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        chars |= set(text)
    return {c for c in chars if c.isprintable() or c == " "}


def main():
    chars = used_characters()
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "ccmp", "locl", "mark", "mkmk"]
    options.desubroutinize = False
    options.hinting = False
    options.notdef_outline = False
    options.name_IDs = ["*"]
    options.name_legacy = False
    options.recalc_bounds = True

    font = subset.load_font(str(SRC), options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text="".join(sorted(chars)))
    subsetter.subset(font)
    subset.save_font(font, str(OUT), options)

    before = SRC.stat().st_size / 1024
    after = OUT.stat().st_size / 1024
    print(f"police : {len(chars)} caracteres conserves, "
          f"{before:.1f} Ko -> {after:.1f} Ko ({100 - after / before * 100:.0f} % de moins)")


if __name__ == "__main__":
    main()
