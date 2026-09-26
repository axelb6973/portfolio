# AXAIR — site vitrine climatisation

Site statique d'une page, sans dépendance ni étape de build.
Direction artistique : canevas noir façon reveal produit, canevas gris clair pour la grille,
un seul bleu fonctionnel (`#0070d5`), surfaces plates, boutons pilule 64 px.

## Lancer

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Structure

- `index.html` — contenu et structure des sections
- `assets/css/style.css` — tokens (couleurs, type, espacements, rayons) + composants
- `assets/js/main.js` — interactions

## Animations

| Effet | Où |
|---|---|
| Flux d'air en canvas, dévié par le curseur | hero |
| Titres découpés en mots, révélés sous masque | tous les `[data-split]` |
| Apparition au scroll avec cascade | `[data-reveal]`, `data-delay` en ms |
| Parallaxe | `[data-parallax="0.12"]` (valeur = intensité, signe = sens) |
| Boutons magnétiques | `[data-magnetic]` |
| Inclinaison 3D au survol | `[data-tilt]` |
| Curseur anneau qui grossit sur les cibles | global, pointeur fin uniquement |
| Barre de progression de lecture | haut de page |
| Soulignement de nav qui suit le survol + lien actif | nav |
| Carrousel auto, flèches, points, swipe | section Gammes |
| Compteurs chiffrés | section stats |
| Ligne de progression des étapes pilotée au scroll | section Méthode |

Tout est neutralisé sous `prefers-reduced-motion: reduce`, et le canvas et le curseur
sont désactivés sur pointeur tactile.

## À brancher

Le formulaire ne fait que de la validation côté client (`assets/js/main.js`, bloc final) :
il n'envoie rien. Brancher un `fetch` vers l'endpoint voulu.
Coordonnées, numéro F-Gaz et noms de gammes sont des valeurs de remplissage.
