"""
Projet Réalité Augmentée — WebAR, Flask & PythonAnywhere
=========================================================

Application Flask servant les scènes de réalité augmentée du module.

Rôle du serveur : il ne fait **aucun** calcul de réalité augmentée. Il se contente
de servir des gabarits HTML, un catalogue de modèles 3D et une petite API REST.
Tout le suivi (*tracking*) se passe dans le navigateur du smartphone. C'est ce qui
rend le projet compatible avec les 100 CPU-secondes/jour de l'offre gratuite de
PythonAnywhere.

Organisation en couches (attendu d'architecture du module) :
    - couche données    : data/catalogue.json  + les fonctions `charger_catalogue`…
    - couche métier     : authentification, recherche
    - couche API        : les routes /api/*, consommées par les scènes AR
    - couche présentation : templates/ + static/

Les sections marquées « TODO ATELIER n » sont le travail demandé aux étudiants.
"""

import json
import secrets
import sys
from functools import wraps
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# PythonAnywhere place votre application derrière un proxy qui termine le TLS.
# Sans ProxyFix, `request.is_secure` vaudrait toujours False et la route /sante
# vous annoncerait à tort que le HTTPS est inactif.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

RACINE = Path(__file__).resolve().parent
FICHIER_CATALOGUE = RACINE / "data" / "catalogue.json"


# ---------------------------------------------------------------------------
# Couche données — le catalogue de modèles 3D
# ---------------------------------------------------------------------------

def charger_catalogue():
    """Retourne la liste des modèles décrits dans data/catalogue.json.

    Le fichier est relu à chaque appel : c'est volontaire. Pendant un atelier on
    modifie le catalogue très souvent, et une erreur de syntaxe JSON doit être
    signalée immédiatement plutôt qu'au prochain redémarrage du serveur.
    """
    try:
        with FICHIER_CATALOGUE.open(encoding="utf-8") as flux:
            donnees = json.load(flux)
    except FileNotFoundError:
        app.logger.error("Catalogue introuvable : %s", FICHIER_CATALOGUE)
        return []
    except json.JSONDecodeError as erreur:
        # Erreur la plus fréquente de l'atelier 2 : une virgule en trop.
        app.logger.error("data/catalogue.json est invalide : %s", erreur)
        return []

    return donnees.get("modeles", [])


def fichier_statique_present(chemin_relatif):
    """Indique si un fichier existe dans static/ (None et "" renvoient False)."""
    if not chemin_relatif:
        return False
    return (Path(app.static_folder) / chemin_relatif).is_file()


def enrichir(modele):
    """Ajoute au modèle les informations calculées utiles aux gabarits.

    `glb_present` permet à la page d'accueil d'afficher un avertissement clair
    quand le fichier .glb déclaré dans le catalogue n'a pas encore été déposé —
    c'est le cas au démarrage de l'atelier 2.
    """
    return {
        **modele,
        "glb_present": fichier_statique_present(f"models/{modele.get('glb')}"),
        "usdz_present": fichier_statique_present(f"models/{modele.get('usdz')}"),
        "cible_presente": fichier_statique_present(f"targets/{modele.get('cible_mind')}"),
    }


def trouver_modele(slug):
    """Retourne le modèle portant ce slug, ou None."""
    for modele in charger_catalogue():
        if modele.get("slug") == slug:
            return modele
    return None


def trouver_modele_ou_404(slug):
    modele = trouver_modele(slug)
    if modele is None:
        abort(404, description=f"Aucun modèle nommé « {slug} » dans le catalogue.")
    return enrichir(modele)


# ---------------------------------------------------------------------------
# Couche métier — authentification (exercice 3.2)
# ---------------------------------------------------------------------------
#
# ⚠️ AVERTISSEMENT PÉDAGOGIQUE
# Des identifiants écrits en clair dans le code source sont INACCEPTABLES en
# production. C'est une simplification d'atelier, cohérente avec l'énoncé de
# l'exercice 3.2 (user / 12345).
#
# En conditions réelles : variables d'environnement (fichier WSGI de
# PythonAnywhere), mots de passe hachés via werkzeug.security.generate_password_hash,
# et jamais de secret dans Git. C'est exactement le problème que résolvent les
# 4 secrets GitHub de la séquence 0.3.

COMPTES = {
    "user": {"mot_de_passe": "12345", "role": "user"},
    # TODO ATELIER 3 — exercice 3.2
    # Ajoutez ici le compte administrateur, avec le rôle "admin".
}

# TODO ATELIER 3 — exercice 3.2
# Décrivez la hiérarchie des rôles : un "admin" doit pouvoir accéder à ce qui
# est ouvert au rôle "user", l'inverse étant faux.
# Piste : un dictionnaire {role: set(des rôles couverts)} consulté par
# `role_suffisant()` ci-dessous.
HIERARCHIE_DES_ROLES = {}


def verifier_identifiants(autorisation):
    """Retourne le compte correspondant aux identifiants fournis, ou None.

    `secrets.compare_digest` compare en temps constant : cela évite de révéler
    la longueur du mot de passe par le temps de réponse.
    """
    if autorisation is None or not autorisation.username:
        return None

    compte = COMPTES.get(autorisation.username)
    if compte is None:
        return None

    if not secrets.compare_digest(autorisation.password or "", compte["mot_de_passe"]):
        return None

    return compte


def role_suffisant(role_du_compte, role_exige):
    """Indique si `role_du_compte` donne accès à une ressource `role_exige`.

    Comportement actuel : égalité stricte. C'est volontairement restrictif
    (« fail closed ») — tant que la hiérarchie n'est pas implémentée, mieux vaut
    refuser un accès légitime que d'en autoriser un illégitime.
    """
    if role_du_compte == role_exige:
        return True

    # TODO ATELIER 3 — exercice 3.2
    # Exploitez HIERARCHIE_DES_ROLES pour qu'un admin couvre le rôle user.
    return False


def demander_authentification():
    """Renvoie un 401 qui déclenche la fenêtre de connexion du navigateur."""
    return Response(
        "Authentification requise pour accéder à cette ressource.",
        401,
        {"WWW-Authenticate": 'Basic realm="Atelier AR", charset="UTF-8"'},
    )


def authentification_requise(role="user"):
    """Décorateur protégeant une route par authentification HTTP Basic.

    Usage :
        @app.get("/secret")
        @authentification_requise(role="admin")
        def secret():
            ...
    """
    def decorateur(vue):
        @wraps(vue)
        def enveloppe(*args, **kwargs):
            compte = verifier_identifiants(request.authorization)
            if compte is None:
                return demander_authentification()
            if not role_suffisant(compte["role"], role):
                abort(403, description="Votre rôle ne permet pas cet accès.")
            return vue(*args, **kwargs)
        return enveloppe
    return decorateur


# ---------------------------------------------------------------------------
# Couche présentation — les pages
# ---------------------------------------------------------------------------

@app.get("/")
def accueil():
    """Page d'accueil : le catalogue. Fournie et fonctionnelle (atelier 0)."""
    modeles = [enrichir(modele) for modele in charger_catalogue()]
    return render_template("index.html", modeles=modeles)


@app.get("/camera")
def test_camera():
    """Page de diagnostic caméra — séquence 0.4, vérification n°4.

    Fournie et fonctionnelle : c'est elle qui prouve que la chaîne HTTPS est
    opérationnelle avant d'aborder les ateliers AR.
    """
    return render_template("camera.html")


@app.get("/viewer/<slug>")
def viewer(slug):
    """ATELIER 2 — affichage d'un modèle avec <model-viewer>.

    Le gabarit templates/viewer.html est à compléter.
    """
    return render_template("viewer.html", modele=trouver_modele_ou_404(slug))


@app.get("/marqueur")
def marqueur():
    """ATELIER 3, jalons J1–J2 — suivi par marqueur avec A-Frame + AR.js.

    Le gabarit templates/marqueur.html est à compléter. Le modèle à afficher
    peut être choisi via le paramètre d'URL `?modele=<slug>`.
    """
    slug = request.args.get("modele")
    modele = enrichir(trouver_modele(slug)) if trouver_modele(slug) else None
    return render_template("marqueur.html", modele=modele)


@app.get("/image/<slug>")
def image(slug):
    """ATELIER 3, jalons J3–J4 — suivi d'image avec MindAR.

    Le gabarit templates/image.html est à compléter.
    """
    return render_template("image.html", modele=trouver_modele_ou_404(slug))


@app.get("/fiche/<slug>")
def fiche(slug):
    """ATELIER 3 — fiche détaillée d'un modèle.

    Le gabarit templates/fiche.html est à compléter.
    """
    return render_template("fiche.html", modele=trouver_modele_ou_404(slug))


@app.get("/fiche_nom/")
def fiche_nom():
    """ATELIER 3 — exercices 3.1 et 3.2.

    TODO ATELIER 3 — exercice 3.1
    Recherchez un modèle du catalogue d'après son nom, transmis en paramètre
    d'URL (ex. /fiche_nom/?nom=cube). La recherche doit être insensible à la
    casse et tolérer une correspondance partielle. Renvoyez la fiche du modèle
    trouvé, ou un message clair si la recherche ne donne rien.
    Pensez au cas où plusieurs modèles correspondent.

    TODO ATELIER 3 — exercice 3.2
    Protégez cette route au niveau `user` en ajoutant, au-dessus de la
    définition de la fonction :
        @authentification_requise(role="user")
    L'ordre des décorateurs compte : @app.get(...) doit rester le plus haut.
    """
    abort(501, description="Exercice 3.1 : recherche par nom à implémenter.")


# ---------------------------------------------------------------------------
# Couche API — consommée par les scènes AR (jalon J4)
# ---------------------------------------------------------------------------

@app.get("/api/modeles")
def api_modeles():
    """Catalogue complet au format JSON."""
    return jsonify([enrichir(modele) for modele in charger_catalogue()])


@app.get("/api/modeles/<slug>")
def api_modele(slug):
    """Métadonnées d'un modèle. C'est cette route qu'appelle `fetch()` au J4."""
    return jsonify(trouver_modele_ou_404(slug))


@app.get("/sante")
def sante():
    """Diagnostic de déploiement — séquence 0.4, vérification n°3.

    Si "https" vaut false, la caméra sera refusée par le navigateur : vous avez
    probablement ouvert le site en http://.
    """
    modeles = charger_catalogue()
    return jsonify({
        "ok": True,
        "https": request.is_secure,
        "schema": request.scheme,
        "hote": request.host,
        "python": sys.version.split()[0],
        "catalogue": {
            "modeles_declares": len(modeles),
            "fichiers_glb_presents": sum(
                1 for m in modeles if fichier_statique_present(f"models/{m.get('glb')}")
            ),
        },
    })


# ---------------------------------------------------------------------------
# Gestion des erreurs — les scènes AR consomment du JSON, les humains du HTML
# ---------------------------------------------------------------------------

def _repond_en_json():
    return request.path.startswith("/api/")


@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(501)
def erreur(exception):
    code = getattr(exception, "code", 500)
    message = getattr(exception, "description", "Erreur.")
    if _repond_en_json():
        return jsonify({"erreur": message, "code": code}), code
    return render_template("erreur.html", code=code, message=message), code


if __name__ == "__main__":
    # Utile dans votre codespace uniquement. PythonAnywhere n'exécute jamais ce
    # bloc : son serveur WSGI importe directement l'objet `app`.
    # Note : Codespaces expose le port 5000 sur une URL https://…app.github.dev,
    # donc en contexte sécurisé — la caméra y fonctionne. Pour tester depuis un
    # téléphone, passez la visibilité du port à « Public » (onglet PORTS).
    app.run(host="0.0.0.0", port=5000, debug=True)
