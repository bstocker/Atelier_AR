# `static/targets/` — cibles de suivi d'image (MindAR, atelier 3b)

Déposez ici les fichiers **`.mind`** compilés, puis renseignez `cible_mind` dans
[`data/catalogue.json`](../../data/catalogue.json).

## Compiler une cible

1. Ouvrez le [compilateur de cibles MindAR](https://hiukim.github.io/mind-ar-js-doc/tools/compile).
2. Glissez votre image, lancez la compilation, téléchargeant le `targets.mind`.
3. Renommez-le et déposez-le ici.
4. **Imprimez l'image** : c'est elle que vous viserez avec le téléphone.

Un même fichier `.mind` peut contenir **plusieurs images**. L'attribut
`targetIndex` désigne alors la position de l'image dans le fichier, en partant
de `0` — dans l'ordre où vous les avez ajoutées au compilateur.

## Choisir une bonne image — c'est 90 % du résultat

MindAR extrait des **points caractéristiques** de l'image et les reconnaît dans
le flux caméra. La qualité du suivi dépend donc presque entièrement de l'image
source.

### ✅ Une bonne cible

- **riche en détails fins** et **non répétitifs** ;
- **très contrastée** ;
- **asymétrique** (sinon l'orientation est ambiguë) ;
- **nette**, et imprimée sur papier **mat** ;
- format **plutôt carré** ou proche de 1:1.

### ❌ Une mauvaise cible

- larges zones uniformes (ciel, mur blanc, fond de couleur unie) ;
- motifs répétitifs (damier, rayures, grille, texture de tissu) ;
- image floue, peu contrastée, ou majoritairement du texte ;
- symétrie forte (logo circulaire centré) ;
- papier glacé ou écran : les reflets détruisent le suivi.

> 💡 **Test en 10 secondes.** Plissez les yeux en regardant votre image. S'il
> reste des zones de contraste distinctes et identifiables, la cible est bonne.
> Si tout devient uniforme, changez d'image.

## Le décrochage est-il normal ?

Un peu, oui : il faut que **l'image reste visible** dans le champ de la caméra.
Contrairement au SLAM (qui mémorise la géométrie de la pièce), le suivi d'image
perd l'ancrage dès que la cible sort du cadre — c'est la limite de la famille de
suivi, pas un défaut de votre code.

Traitez-le explicitement : c'est l'objet du **TODO 3.9** (événements
`targetFound` / `targetLost`).

## Bonus — suivi de visage

MindAR sait aussi suivre un visage (`mindar-face-aframe.prod.js`) : filtres,
masques, lunettes virtuelles. Une piste pour le jalon **J6** ou un projet
« marketing » à l'atelier 4.
