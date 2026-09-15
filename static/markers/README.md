# `static/markers/` — marqueurs fiduciaires (AR.js, atelier 3a)

## Le marqueur Hiro : à imprimer avant la séance

Pour les jalons **J1 et J2**, aucun fichier n'est nécessaire ici : AR.js embarque
le motif Hiro, activé par `<a-marker preset="hiro">`.

**Imprimez-le sur une feuille A4** :
<https://raw.githubusercontent.com/AR-js-org/AR.js/master/data/images/hiro.png>

### Trois règles pour que la détection fonctionne

1. **Conservez la bordure blanche** autour du motif noir. C'est elle qui délimite
   le marqueur : un motif rogné n'est jamais détecté.
2. **Imprimez grand** — au moins 8 à 10 cm de côté. Plus le marqueur est grand,
   plus le suivi est stable et plus vous pouvez vous en éloigner.
3. **Évitez les reflets.** Papier mat de préférence, et pas d'éclairage direct :
   un marqueur derrière une pochette plastique brillante ne se détecte pas.

## Marqueurs personnalisés

Pour créer votre propre motif (fichier `.patt`, à déposer ici) :
[générateur de marqueurs AR.js](https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html)

```html
<a-marker type="pattern"
          url="{{ url_for('static', filename='markers/mon-marqueur.patt') }}">
```

Un bon motif est **asymétrique**, **très contrasté** (noir et blanc franc) et
**simple**. Un motif symétrique rend l'orientation ambiguë : votre modèle pivotera
par sauts de 90°.

## Marqueurs `barcode` — pour plusieurs modèles

Si votre projet d'atelier 4 doit distinguer plusieurs objets (chasse au trésor,
guide de maintenance), les marqueurs `barcode` évitent de créer un `.patt` par
cible :

```html
<a-marker type="barcode" value="5">
```

## Marqueur ou suivi d'image ?

| | Marqueur (AR.js) | Suivi d'image (MindAR) |
|---|---|---|
| Robustesse | ✅ excellente, même en faible lumière | ⚠️ dépend de la qualité de l'image |
| Apparence | ❌ motif technique, peu présentable | ✅ n'importe quel visuel |
| Préparation | ✅ aucune (preset Hiro) | ⚠️ compilation d'une cible `.mind` |

C'est précisément pour ce contraste que l'atelier 3 vous fait pratiquer les deux.
