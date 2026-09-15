# Fiche projet — Module Réalité Augmentée / Réalité Virtuelle

**Campus Saint-Aspais (Melun)** — Titre de niveau 7 « Expert en architecture et développement logiciel »

| | |
|---|---|
| **Module** | Réalité Augmentée / VR |
| **Volume horaire** | 21 h |
| **Année** | 2ᵉ année |
| **Public** | Étudiant·e·s développeur·se·s (bases solides en POO et développement d'applications) |
| **Fil rouge** | 4 ateliers progressifs : comprendre → prototyper → développer → livrer un MVP |

---

## 1. Objectifs pédagogiques du module

À l'issue du module, l'étudiant·e est capable de :

- distinguer réalité augmentée (RA), réalité virtuelle (RV) et réalité mixte (RM), et situer une expérience sur le continuum de Milgram ;
- expliquer les grands principes de suivi (*tracking*) et de compréhension de scène (détection de plans, ancrage, estimation de lumière) ;
- choisir un moteur et un SDK adaptés à un besoin, en justifiant le choix ;
- concevoir, développer et livrer une application AR simple selon une logique MVP ;
- travailler en groupe sur un projet en respectant des jalons et une démarche de prototypage.

Ces objectifs couvrent les trois sections du syllabus : **Introduction (6 h)**, **Développement d'applications (8 h)**, **Cas pratiques / prototypage (7 h)**.

## 2. Compétences visées (référentiel niveau 7)

- Analyser un besoin et le traduire en spécifications techniques pour une application immersive.
- Concevoir l'architecture d'une application AR (couche rendu, couche suivi, couche métier/UI).
- Mettre en œuvre un environnement de développement et une chaîne de *build* multi-plateformes.
- Intégrer un SDK tiers et en maîtriser les limites matérielles.
- Documenter, versionner (Git) et présenter une réalisation logicielle.

## 3. Prérequis et matériel

**Prérequis** : programmation orientée objet (C# apprécié), notions de repères 3D (position, rotation, échelle), utilisation de Git.

**Matériel recommandé** :

- un poste de développement (Windows ou macOS) avec **Unity 6 LTS** + module *Android Build Support* (et *iOS Build Support* sur macOS) ;
- un smartphone **compatible AR** : Android **ARCore** ou iOS **ARKit** (liste des appareils supportés à vérifier avant la séance) ;
- un câble USB et le **mode développeur** activé sur le smartphone (débogage USB) ;
- solution de repli sans smartphone compatible : **WebAR** dans un navigateur mobile récent (voir Atelier 2).

## 4. Progression et volumes horaires

| # | Atelier | Section du syllabus | Format | Durée indicative |
|---|---------|--------------------|--------|------------------|
| 1 | Comprendre l'AR | 1. Introduction | Recherche guidée + restitution | 4 h |
| 2 | « Hello World » AR | 2. Développement | TP pas-à-pas | 3 h |
| 3 | Travail dirigé : développer une application AR | 2. Développement | TD encadré | 6 h |
| 4 | Projet : application AR (MVP en groupe) | 3. Cas pratiques | Projet + soutenance | 8 h |
| | **Total** | | | **21 h** |

> Les ateliers 1 et 2 posent le socle conceptuel et technique ; l'atelier 3 consolide par la pratique guidée ; l'atelier 4 met les acquis en autonomie. Conformément au syllabus, le projet de l'atelier 4 peut être décliné **en RA ou en RV**.

---

# Atelier 1 — Comprendre l'AR

**Rattachement** : Section 1 « Introduction à la RA et RV » · **Durée** : 4 h · **Modalité** : binômes, recherche guidée puis restitution orale courte.

## Objectifs

- Poser un vocabulaire commun et rigoureux (RA / RV / RM, continuum de Milgram).
- Comprendre *comment* la RA « tient » dans le réel : les familles de suivi et la compréhension de scène.
- Cartographier l'écosystème des moteurs et SDK, et savoir lequel répond à quel besoin.
- Relier la technologie à des cas d'usage réels (marketing, gaming, formation — les trois cas cités au syllabus).

## Contenu à explorer

1. **Définitions et frontières** : RA vs RV vs RM ; continuum réel–virtuel de Milgram ; RA *marker-based* vs *markerless*.
2. **Le suivi (*tracking*)** :
   - marqueurs fiduciaires (ex. type *Hiro*, QR),
   - suivi d'image (*image tracking*),
   - détection de plans et **SLAM** (*Simultaneous Localization and Mapping*),
   - ancrage (*anchors*), estimation de lumière, occlusion.
3. **Écosystème technique** : ARCore (Google), ARKit (Apple), **AR Foundation** (Unity, abstraction multi-plateformes), Vuforia, WebXR / WebAR, Unreal Engine.
4. **Cas d'usage** : un exemple documenté par catégorie (marketing, gaming, formation), avec bénéfice métier et limite technique associée.

## Travail demandé

Chaque binôme produit une **fiche de synthèse (2 pages)** et un **mini-exposé (5 min)** couvrant :

- un tableau comparatif RA / RV / RM ;
- un schéma du principe de suivi choisi (marqueur, image ou SLAM) ;
- une comparaison de **2 SDK** (forces, limites, plateformes, coût de licence) ;
- l'analyse d'**une application AR existante** du marché : cas d'usage, techno probable, ce qui marche / ce qui pêche.

## Livrable

`atelier1-synthese-<nom>.pdf` (ou `.md`) + support de restitution.

## Grille d'évaluation (sur 20)

| Critère | Points |
|---|---|
| Exactitude des concepts (RA/RV/RM, tracking) | 6 |
| Pertinence de la comparaison de SDK | 5 |
| Qualité de l'analyse de cas d'usage | 5 |
| Clarté de la restitution orale et du support | 4 |

---

# Atelier 2 — « Hello World » AR

**Rattachement** : Section 2 « Développement d'applications » · **Durée** : 3 h · **Modalité** : TP individuel guidé pas-à-pas.

## Choix de la technologie « la plus pertinente » — et sa justification

**Technologie retenue : Unity 6 + AR Foundation** (avec les plugins *ARCore XR Plugin* et *ARKit XR Plugin*).

Ce choix est le plus pertinent pour ce module pour quatre raisons :

1. **Alignement syllabus** : Unity est explicitement au programme (Section 2) ; on capitalise donc sur l'outil du cours.
2. **Multi-plateforme** : AR Foundation est une couche d'abstraction unique au-dessus d'ARCore (Android) et ARKit (iOS) — un seul code, deux cibles.
3. **Industrialisable** : c'est le standard de fait pour la RA mobile ; les acquis sont directement réutilisables aux ateliers 3 et 4, puis en entreprise.
4. **Courbe d'apprentissage maîtrisée** : la détection de plan et le placement d'objet sont accessibles en une séance, sans écrire de code de suivi bas niveau.

> **Alternative légère (repli / postes sans smartphone AR-compatible) : WebAR.** Sans installation, dans le navigateur : `<model-viewer>` de Google (bouton « Voir en AR »), **MindAR** ou **A-Frame + AR.js** (suivi de marqueur/image). Idéal pour une démonstration immédiate ; à privilégier si le parc de smartphones n'est pas homogène. Unreal Engine reste une option « moteur AAA » mais alourdit inutilement un premier Hello World.

## Objectif du TP

Afficher un **objet 3D (un cube, puis un modèle)** ancré sur une **surface réelle détectée**, visible à travers la caméra du smartphone, et le poser d'un **tap** à l'écran.

## Déroulé pas-à-pas

1. **Création du projet** : nouveau projet Unity (modèle *Universal 3D* ou *AR Mobile* selon la version).
2. **Installation des paquets** via le *Package Manager* : `AR Foundation`, `Google ARCore XR Plugin` (Android), `Apple ARKit XR Plugin` (iOS, sur macOS).
3. **Mise en place de la scène** :
   - remplacer la caméra par un **XR Origin (AR)** ;
   - ajouter les composants **AR Session**, **AR Plane Manager** (détection de plans), **AR Raycast Manager**.
4. **Placement au tap** : un court script C# qui lance un *raycast* depuis le point touché vers les plans détectés et instancie un préfabriqué à l'endroit visé.
5. **Réglages de *build*** : plateforme Android (ou iOS), nom de paquet, orientation, permission caméra, niveaux d'API minimum.
6. **Build & test sur appareil** : générer l'APK (ou déployer via Xcode) et vérifier le placement en conditions réelles.

### Extrait de code de référence (C#) — placement au tap

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

[RequireComponent(typeof(ARRaycastManager))]
public class PlaceOnPlane : MonoBehaviour
{
    [SerializeField] private GameObject prefabAPlacer;   // ex. un cube

    private ARRaycastManager raycastManager;
    private static readonly List<ARRaycastHit> hits = new();

    void Awake() => raycastManager = GetComponent<ARRaycastManager>();

    void Update()
    {
        if (Input.touchCount == 0) return;
        var touche = Input.GetTouch(0);
        if (touche.phase != TouchPhase.Began) return;

        if (raycastManager.Raycast(touche.position, hits, TrackableType.PlaneWithinPolygon))
        {
            Pose pose = hits[0].pose;                 // position + orientation du point visé
            Instantiate(prefabAPlacer, pose.position, pose.rotation);
        }
    }
}
```

## Livrable

- Projet Unity versionné (Git) ou APK de démonstration.
- Une **capture vidéo (30 s)** montrant l'objet ancré sur une surface réelle.
- Court README : techno, appareil de test, difficultés rencontrées.

## Critères de réussite

Un objet reste **ancré et stable** sur un plan détecté quand on déplace le téléphone ; le placement fonctionne sur au moins un appareil physique (ou en WebAR pour la voie de repli).

---

# Atelier 3 — Travail dirigé : développer une application AR

**Rattachement** : Section 2 « Développement d'applications » · **Durée** : 6 h · **Modalité** : TD encadré, binômes, jalons avec points de contrôle par l'enseignant·e.

## Principe

On transforme le « Hello World » de l'atelier 2 en une **petite application fonctionnelle** : une **visionneuse de produit / catalogue AR** (déclinable en visionneuse pédagogique, ex. maquette d'organe, molécule, pièce mécanique). Le TD est guidé mais laisse des choix de conception à l'étudiant·e.

## Fonctionnalités à implémenter (par jalons)

| Jalon | Fonctionnalité | Compétence travaillée |
|---|---|---|
| J1 | Placer un **modèle 3D importé** (format glTF/FBX) sur un plan | Import d'*assets*, préfabriqués |
| J2 | **Manipulations gestuelles** : déplacer, pivoter, redimensionner (pinch) | Gestion des entrées tactiles |
| J3 | **Interface (UI)** : sélectionner le modèle dans un menu, bouton *reset* | UI Unity (Canvas), architecture UI/métier |
| J4 | **Un objet à la fois + ancrage** propre (`ARAnchor`) | Cycle de vie des objets, stabilité |
| J5 (bonus) | **Estimation de lumière** et/ou **occlusion** pour un rendu réaliste | Réalisme, API avancée AR Foundation |

## Consignes de conception

- Séparer clairement la **couche AR** (détection, ancrage), la **couche présentation** (UI) et la **logique métier** (catalogue de modèles) — attendu d'architecture au niveau 7.
- Gérer les **cas d'erreur** : aucun plan détecté, permission caméra refusée, appareil non compatible.
- Versionner par petites *commits* signifiantes ; un `.gitignore` Unity correct.

## Déroulé indicatif (6 h)

1. **0 h – 0 h 30** : cadrage, rappel de l'architecture cible, prise en main des *assets*.
2. **0 h 30 – 3 h** : jalons J1 → J3 (placement, gestes, UI).
3. **3 h – 5 h** : jalon J4 (ancrage, robustesse) + gestion des erreurs.
4. **5 h – 6 h** : bonus J5, nettoyage du dépôt, mini-démo croisée entre binômes.

## Livrable

- Dépôt Git de l'application (README, instructions de *build*, captures).
- Démonstration en séance des jalons J1 à J4.

## Grille d'évaluation (sur 20)

| Critère | Points |
|---|---|
| Fonctionnalités des jalons J1–J4 opérationnelles | 8 |
| Qualité de l'architecture (séparation des couches) | 4 |
| Robustesse et gestion des erreurs | 3 |
| Qualité du dépôt Git et de la documentation | 3 |
| Bonus J5 (lumière / occlusion) | +2 |

---

# Atelier 4 — Projet : application AR (MVP en groupe)

**Rattachement** : Section 3 « Cas pratiques : prototypage » · **Durée** : 8 h · **Modalité** : projet en groupe (3–4 personnes), **logique MVP**, clôturé par une soutenance-démo.

## Énoncé du sujet

> **Concevoir, développer et livrer le MVP d'une application de réalité augmentée** répondant à un besoin réel dans l'un des domaines du syllabus (**marketing, gaming, formation, éducation**). Le groupe applique une démarche projet : cadrage du besoin, périmètre MVP, développement itératif, démonstration.

Conformément au syllabus, le projet peut être **décliné en RV** (casque ou WebXR) si le groupe le justifie.

## Démarche imposée (approche MVP)

1. **Cadrage** : problème adressé, utilisateur cible, proposition de valeur, une *user story* principale.
2. **Périmètre MVP** : lister les fonctionnalités *must / should / could*, ne développer que le *must*.
3. **Architecture** : schéma des couches (AR, UI, données) et des *assets* nécessaires.
4. **Développement itératif** : au moins deux itérations avec démonstration intermédiaire.
5. **Livraison & démo** : build fonctionnel + soutenance.

## Banque de sujets proposés

| Domaine | Sujet | Cœur fonctionnel MVP |
|---|---|---|
| Marketing | **Essayage / aperçu produit** (meuble, sneaker, objet déco chez soi) | Placer un modèle à l'échelle réelle sur le sol, changer de variante |
| Éducation | **Manuel augmenté** : une image du cours déclenche une animation 3D | Suivi d'image → superposition d'un modèle animé |
| Formation | **Guide de maintenance AR** : étapes superposées sur un équipement | Suivi d'image/objet + surcouche d'instructions séquencées |
| Gaming | **Chasse au trésor / créature AR** dans la pièce | Détection de plans, apparition d'entités, interaction au tap |
| Culture | **Visite augmentée** : socle → œuvre 3D + fiche d'info | Marqueur/image → modèle + panneau UI |
| Santé/Sciences | **Explorateur 3D** (organe, molécule, système solaire) | Modèle manipulable + annotations interactives |

> Les groupes peuvent proposer leur **propre sujet**, sous validation de l'enseignant·e (faisabilité en 8 h + périmètre MVP réaliste).

## Livrables attendus

- **Dépôt Git** du projet (code, `README`, instructions de *build*).
- **Application fonctionnelle** (APK / build WebAR / build RV) démontrable.
- **Dossier projet court (3–5 pages)** : besoin, périmètre MVP, architecture, choix techniques, limites et perspectives.
- **Soutenance (10 min + démo live)**.

## Jalons de suivi

| Jalon | Attendu |
|---|---|
| J0 (fin H1) | Sujet validé, *user story* principale, périmètre MVP |
| J1 (mi-parcours) | Prototype jouable du cœur fonctionnel (démonstration intermédiaire) |
| J2 (fin) | MVP livré, dossier rendu, soutenance |

## Grille d'évaluation (sur 20)

| Critère | Points |
|---|---|
| Pertinence du besoin et cadrage MVP | 4 |
| Fonctionnalité et stabilité du MVP livré | 6 |
| Qualité technique (architecture, code, intégration SDK) | 4 |
| Dossier projet et documentation | 3 |
| Soutenance et démonstration | 3 |

---

## Annexe — Ressources et bibliographie

- **Unity — AR Foundation** : documentation officielle du paquet `com.unity.xr.arfoundation` (samples inclus).
- **Google ARCore** : *fundamental concepts* (planes, anchors, light estimation) et liste des appareils supportés.
- **Apple ARKit** : documentation développeur et appareils compatibles.
- **WebAR** : `model-viewer` (Google), **MindAR**, **A-Frame + AR.js** pour la voie sans installation.
- **Cadre théorique** : P. Milgram & F. Kishino, *A Taxonomy of Mixed Reality Visual Displays* (continuum RA/RV).

> Les liens précis et versions des SDK sont à vérifier en début de module (les compatibilités matérielles évoluent vite).

---

*Fiche projet — Module RA/RV, 21 h, Titre niveau 7. Document pédagogique à adapter selon le parc matériel et le calendrier de la promotion.*
