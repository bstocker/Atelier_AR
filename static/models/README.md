# `static/models/` — vos modèles 3D

Déposez ici vos fichiers de modèles, puis déclarez-les dans
[`data/catalogue.json`](../../data/catalogue.json).

## Deux formats, et pourquoi

| Format | Extension | Sert à |
|---|---|---|
| **glTF binaire** | `.glb` | Android + affichage 3D dans le navigateur. **C'est le format principal.** |
| **USDZ** | `.usdz` | **AR Quick Look sur iPhone / iPad uniquement.** |

> ⚠️ **Le piège de l'atelier 2.** Sans fichier `.usdz` renseigné dans l'attribut
> `ios-src`, le bouton « Voir en AR » **ne s'affiche tout simplement pas** sur
> iPhone. Ce n'est pas un bug de votre code : c'est Apple qui n'accepte que
> l'USDZ pour Quick Look.

Convertir glTF → USDZ :
[Reality Converter](https://developer.apple.com/augmented-reality/tools/) (macOS),
ou un convertisseur en ligne.

## Où trouver des modèles libres

- [Khronos glTF Sample Assets](https://github.com/KhronosGroup/glTF-Sample-Assets) — les modèles de référence du format
- [Poly Pizza](https://poly.pizza/) — *low-poly*, très légers, parfaits pour le mobile
- [Sketchfab](https://sketchfab.com/features/free-3d-models) — filtrez sur **Downloadable**

## Contrainte de poids : visez moins de 5 Mo

Deux raisons, et la seconde est la plus concrète :

1. l'offre gratuite de PythonAnywhere plafonne à **512 Mo** de disque ;
2. **vos camarades téléchargeront ce fichier sur le réseau de la salle.** Un
   modèle de 40 Mo rend votre démonstration de soutenance inutilisable.

Pour compresser : [gltf-transform](https://gltf-transform.dev/) ou
[gltfpack](https://meshoptimizer.org/gltf/).

```bash
npx @gltf-transform/cli optimize gros.glb leger.glb --texture-compress webp
```

## Échelle

Les unités glTF sont des **mètres**. Un modèle exporté en centimètres apparaîtra
**100 fois trop grand**. Ajustez `echelle` dans le catalogue, ou réexportez.

## Crédits

Renseignez toujours `auteur` et `licence` dans le catalogue. Pour la plupart des
licences libres (CC-BY notamment), **créditer l'auteur est une obligation
légale**, pas une politesse.
