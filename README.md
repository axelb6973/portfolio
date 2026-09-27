# ACDC Air Conditioning — maquette de démonstration

Proposition de refonte du site d'ACDC Air Conditioning (Perth, WA).
**Maquette non officielle.** Chaque page porte `noindex, nofollow` en meta et en
en-tête HTTP, et un bandeau de mention figure en bas de page.

Direction artistique : référence DJI — void noir en hero, canevas `#ededed`,
cartes blanches à 4 px sans bordure ni ombre, un seul bleu fonctionnel `#0070d5`,
boutons pilule 64 px, Open Sans 300–600, aucun dégradé sur les surfaces plates.

## Lancer

```bash
npm install
npm run dev        # build + serveur sur http://localhost:8000
```

## Build

```bash
npm run build      # images + pages + CSS
```

| Étape | Commande | Ce qu'elle fait |
|---|---|---|
| Images | `npm run images` | `photos/*.jpg|png` → `dist/img/*.webp` en 480/800/960/1440 selon la source |
| Pages | `npm run pages` | assemble les 8 pages depuis `tools/build.py` |
| CSS | `npm run css` | Tailwind CLI v4, purgé et minifié → `dist/assets/site.css` |

Le dossier `dist/` est versionné : l'hébergeur n'a donc **aucune commande à exécuter**,
et le build n'exige pas Python + Pillow sur la machine de déploiement.

## Déploiement Vercel

```bash
npx vercel --prod
```

`vercel.json` sert `dist/`, force `X-Robots-Tag: noindex, nofollow` sur toutes les
réponses et met `assets/` et `img/` en cache un an.

## Structure

```
photos/                 sources d'origine (JPG/PNG)
src/css/tailwind.css    @theme (tokens DJI) + couche composants et animations
src/js/main.js          interactions
tools/images.py         conversion WebP + découpe du diptyque hero
tools/build.py          source unique du header, du footer, du formulaire, des pages
dist/                   sortie servie telle quelle
```

Header, footer et formulaire vivent dans `tools/build.py`. Pour les modifier :
éditer le script, puis `npm run build`.

## Photos

36 fichiers fournis, **29 uniques** après déduplication (5 doublons exacts détectés
par md5, 2 quasi-doublons).

**Utilisées : 13.** Ce sont les seules photos authentiquement ACDC — chantiers VRV,
toitures, véhicules floqués, mise en service. La bannière hero d'origine était un
diptyque ; `tools/images.py` la découpe en deux images pour éviter la couture
verticale au milieu du hero.

**Écartées : 6 fichiers de stock**, dont deux visiblement américaines (un groupe
Trane, des rooftop packaged units) et un rendu 3D. Elles ne sont ni en galerie, ni
en page service : afficher une toiture américaine sous un `alt` « installation
Perth » revient à inventer une réalisation, ce que le brief interdit.

La galerie ne contient donc que du réel, et le dit explicitement en tête de page.

## Contenu à fournir

Tout ce qui manque porte le même marqueur dans les pages : une croix suivie du
libellé et de la mention « to confirm with Daniel ». Liste :

- horaires d'ouverture, adresse exacte ;
- licence ARC / électricien, ABN ;
- fiche Google + 3 avis, liens réseaux sociaux ;
- nom de famille et photo de Daniel ;
- une photo de chantier de ventilation (aucune fournie) ;
- les FAQ des trois pages service ;
- l'endpoint Formspree (`action` est un placeholder, rien n'est envoyé) ;
- un logo haute définition, vectoriel de préférence : la source fait 313×147 et
  64 % de ses pixels ont une alpha intermédiaire, c'est un halo anti-aliasé et non
  une forme détourable. Le footer compose donc sa propre marque (flocon vectoriel +
  « ACDC » typographié) plutôt que d'afficher le PNG sur fond sombre, où il rend
  comme une tache. Le header garde la version couleur d'origine.

Aucun avis, chiffre, prix, garantie, licence ou certification n'a été inventé.
La seule donnée chiffrée vient du contenu fourni (« over 20 years of experience »).

## Défauts du site actuel corrigés

| Constat | Traitement |
|---|---|
| Shortcode `[contact-form-7 id="15"]` affiché brut, formulaire mort | Formulaire de devis sur l'accueil et sur Contact, avec validation |
| Liens `http://url/` et `mailto:your@email` | Supprimés ; tous les liens pointent quelque part |
| Aucune meta description, aucun H1, titres dupliqués | Title et meta uniques par page, exactement un H1 par page |
| Aucune preuve sociale | Galerie de réalisations réelles + emplacements d'avis Google |
| Texte citant Daikin et LG, logos montrant Hitachi/Toshiba/Panasonic | Les 9 marques sont citées et affichées de façon cohérente |
| Menu non sémantique | `<nav>` avec `aria-label`, lien d'évitement, état actif |
| Images JPG de 2021, ~9 Mo | WebP multi-largeurs avec `srcset` — 4,3 Mo de sources → 1,3 Mo |
| Fautes (« client's », « if your systems need serviced ») | Textes réécrits en anglais australien correct |

## Animations

| Effet | Où |
|---|---|
| Flux d'air en canvas, dévié par le curseur | hero |
| Titres découpés en mots, révélés sous masque | `[data-split]` |
| Apparition au scroll en cascade | `[data-reveal]`, `data-delay` en ms |
| Parallaxe | `[data-parallax]` |
| Boutons magnétiques | `[data-magnetic]` |
| Inclinaison 3D au survol | `[data-tilt]` |
| Curseur anneau qui grossit sur les cibles | souris uniquement |
| Barre de progression de lecture | haut de page |
| Soulignement de nav suiveur | header |
| Zoom photo + légende qui monte | vignettes de galerie |
| Bandeau marques défilant, couleur au survol | accueil |
| Compteur | « 20+ years » |
| Lightbox clavier (←, →, Échap) avec piège à focus | galerie |

Tout est neutralisé sous `prefers-reduced-motion: reduce` ; canvas et curseur
personnalisé sont désactivés sur pointeur tactile.

## Conversion et SEO

- Barre « Call now » fixe en bas d'écran sous 880 px.
- Numéro visible dans le bandeau haut et dans le header sur les 8 pages.
- JSON-LD `HVACBusiness` par page : nom, deux téléphones, email, zone Perth, marques.
- Title et meta description uniques ciblant « air conditioning Perth »,
  « split system installation Perth », « ducted air conditioning Perth »,
  « aircon service Perth », « mechanical ventilation Perth ».
- `robots.txt` en `Disallow: /`, `sitemap.xml`, favicon SVG redessiné à partir du
  flocon du logo (la source 512×512 était un agrandissement bitmap).

## Accessibilité

Lien d'évitement, focus visible, un seul H1 par page, `alt` descriptif sur toutes
les images, libellés sur tous les champs, erreurs de formulaire annoncées via
`aria-live` et `aria-invalid`, lightbox modale au clavier avec piège à focus.
