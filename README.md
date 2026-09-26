# ACDC Air Conditioning — maquette de démonstration

Proposition de refonte du site d'ACDC Air Conditioning (Perth, WA).
**Maquette non officielle**, non indexable : chaque page porte
`<meta name="robots" content="noindex, nofollow">` et un bandeau de mention en bas.

Site statique, sans dépendance et sans étape de build côté hébergeur :
HTML + CSS + JS vanilla.

## Lancer

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Récupérer les images réelles

Le logo et les 21 photos de la galerie viennent du site actuel. Ils ne sont pas
dans le dépôt. Depuis une machine ayant accès à `acdcair.com.au` :

```bash
bash public/images/fetch-assets.sh
```

Tant qu'une image manque, la tuile affiche son nom de fichier en orange plutôt
qu'une image cassée, et le logo retombe sur le mot-clé texte « ACDC ».

## Structure

```
index.html  about.html  services.html  gallery.html  contact.html   # générés
tools/build.py          # source unique du header, du footer et des pages
assets/css/style.css    # tokens + composants
assets/js/main.js       # interactions
public/images/          # logo + galerie (à télécharger)
vercel.json             # en-têtes, dont X-Robots-Tag: noindex
```

Le header et le footer sont identiques sur les cinq pages. Pour éviter la dérive,
ils vivent dans `tools/build.py` : modifie le script, puis régénère.

```bash
python3 tools/build.py
```

Les `.html` générés sont commités, donc l'hébergeur n'a rien à exécuter.

## Déploiement Vercel

Projet statique, aucune commande de build :

```bash
vercel --prod
```

`vercel.json` ajoute `X-Robots-Tag: noindex, nofollow` sur toutes les réponses,
en plus des balises meta, et met les assets en cache un an.

## Contenu à fournir

Tout ce qui manque est marqué `[entre crochets]` en orange dans les pages :

- horaires d'ouverture ;
- numéro de licence AU / ARC et ABN ;
- liens réseaux sociaux (ceux du site actuel sont cassés) ;
- nom de famille et photo de Daniel ;
- URL de la fiche Google et trois avis à recopier ;
- endpoint Formspree pour les deux formulaires (`action` est un placeholder,
  la validation est aujourd'hui uniquement côté client, rien n'est envoyé).

Aucun avis, chiffre, prix, garantie, licence ou ABN n'a été inventé.
Les seules données chiffrées présentes viennent du contenu fourni
(« over 20 years of experience »).

## Animations

| Effet | Où |
|---|---|
| Flux d'air en canvas, dévié par le curseur | hero de l'accueil |
| Titres découpés en mots, révélés sous masque | `[data-split]` |
| Apparition au scroll en cascade | `[data-reveal]`, `data-delay` en ms |
| Parallaxe | `[data-parallax="-0.08"]` |
| Boutons magnétiques | `[data-magnetic]` |
| Inclinaison 3D au survol | `[data-tilt]` |
| Curseur anneau | global, souris uniquement |
| Barre de progression de lecture | haut de page |
| Soulignement de nav suiveur | header |
| Compteur | « 20+ years » |
| Lightbox clavier (←, →, Échap) | galerie |

Tout est neutralisé sous `prefers-reduced-motion: reduce` ; le canvas et le
curseur personnalisé sont désactivés sur pointeur tactile.

## Conversion et SEO

- Barre « Call now » fixe en bas d'écran sous 880 px.
- Numéro visible dans le bandeau haut et dans le header sur toutes les pages.
- JSON-LD `HVACBusiness` sur chaque page (nom, téléphones, email, Innaloo, zone Perth).
- Titres et meta descriptions par page ciblant « air conditioning Perth »,
  « split system installation Perth », « ducted air conditioning Perth », « Innaloo ».

## Accessibilité

Lien d'évitement, focus visible, `alt` sur toutes les images, libellés sur tous
les champs, contrastes AA — l'orange existe en deux valeurs, `#c2410c` sur fond
clair et `#f97316` sur fond noir, pour rester au-dessus de 4,5:1 dans les deux cas.
