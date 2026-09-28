#!/usr/bin/env python3
"""Convertit les photos sources en WebP multi-largeurs pour le srcset.

Les sources font 800x600 (chantiers) ou 1440x549 (banniere hero) : on ne
sur-echantillonne jamais, une largeur plus grande que l'original est ignoree.
Les logos gardent leur taille native, ils sont deja petits.

    python3 tools/images.py
"""
import pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "photos"
OUT = ROOT / "dist" / "img"

WIDTHS = (480, 960, 1600)
# AVIF d'abord, WebP en repli : ~30 % plus leger a qualite percue egale.
FORMATS = (("avif", {"quality": 52, "speed": 4}),
           ("webp", {"quality": 82, "method": 6}))
# on ajoute toujours la largeur native : sans elle, une source 800px
# ne sortirait qu'en 480 et la vignette serait floue sur ecran retina.
# Images reellement referencees par les pages : tout le reste est du poids mort.
# La liste est verifiee par tools/build.py, qui echoue si une image manque.
KEEP_UNREFERENCED = {"acdc-logo.png"}


# La banniere source est un diptyque (van a gauche, grue a droite) : montee
# telle quelle, la couture verticale tombe au milieu du hero. On decoupe.
DIPTYCH = {
    "hero-acdc-van-and-crane-lift-perth": ("hero-crane-lift-perth", "hero-acdc-van-perth"),
}


def split_diptych(path):
    """Ecrit les deux moities d'un diptyque comme sources a part entiere."""
    left_name, right_name = DIPTYCH[path.stem]
    im = Image.open(path)
    half = im.width // 2
    im.crop((0, 0, half, im.height)).save(SRC / f"{right_name}.jpg", quality=92)
    im.crop((half, 0, im.width, im.height)).save(SRC / f"{left_name}.jpg", quality=92)


def convert(path):
    """Ecrit <nom>-<largeur>.webp pour chaque largeur utile. Retourne les largeurs produites."""
    im = Image.open(path)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    made = []
    targets = sorted({w for w in WIDTHS if w <= im.width} | {im.width})
    for w in targets:
        h = round(im.height * w / im.width)
        resized = im.resize((w, h), Image.LANCZOS)
        for ext, opts in FORMATS:
            resized.save(OUT / f"{path.stem}-{w}.{ext}", ext.upper(), **opts)
        made.append(w)
    return made, im.size


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total_src = total_out = 0
    for path in sorted(SRC.iterdir()):
        if path.stem in DIPTYCH:
            split_diptych(path)
    for path in sorted(SRC.iterdir()):
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        if path.stem in DIPTYCH:
            continue  # remplace par ses deux moities
        made, size = convert(path)
        out_bytes = sum((OUT / f"{path.stem}-{w}.{ext}").stat().st_size
                        for w in made for ext, _ in FORMATS)
        total_src += path.stat().st_size
        total_out += out_bytes
        print(f"{path.name:58} {size[0]}x{size[1]} -> {made}")
    # le PNG reste en dernier recours pour les navigateurs sans AVIF ni WebP
    for keep in ("acdc-logo.png",):
        (OUT / keep).write_bytes((SRC / keep).read_bytes())
        total_out += (SRC / keep).stat().st_size
    print(f"\nsources {total_src/1024:.0f} Ko -> sortie {total_out/1024:.0f} Ko "
          f"({100 - total_out/total_src*100:.0f} % de moins)")


if __name__ == "__main__":
    main()
