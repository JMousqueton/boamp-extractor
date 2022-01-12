
# BOAMP Extractor ![Version](https://img.shields.io/badge/version-3.5-blue.svg)

> BOAMP-Extractor permet d'extraire les offres de marchés publics publiées au bulletin officiel des annonces des marchés publics (BOAMP).
L'extraction se base sur des mots clefs
Le script ignore les appels d'offres dont la date limite de réponse est dépassée.

[![boamp-extractor](https://github.com/JMousqueton/boamp-extractor/actions/workflows/boamp-extractor.yml/badge.svg)](https://github.com/JMousqueton/boamp-extractor/actions/workflows/boamp-extractor.yml)[![pages-build-deployment](https://github.com/JMousqueton/boamp-extractor/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/JMousqueton/boamp-extractor/actions/workflows/pages/pages-build-deployment)

[![Twitter: JMousqueton](https://img.shields.io/twitter/follow/JMousqueton.svg?style=social)](https://twitter.com/JMousqueton)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/jmousqueton/boamp-extractor/blob/main/LICENSE)

## Documentation 📖 

### En utilisant les fichiers de configuration 

Renseignez les mots-clés de recherches dans le fichier `keywords.txt` avec un mot ou une expression par ligne.

Il est possible d'exclure les appels d'offres contenants certains mots-clés.
Pour cela, renseignez les mots interdits dans le fichier `exception.txt` avec un mot ou une expression par ligne.

### En ligne de commande 💻

Lancez le script `boamp-extractor.py` avec l'option `-k` suivi du mot clef recherché 

### En utilisant Github-Action ⚙️

Voir le fichier [boamp-extractor](https://github.com/JMousqueton/boamp-extractor/blob/main/.github/workflows/boamp-extractor.yml)

Pour les notifications Microsoft Teams : 
Créer un WebHook sur Teams  
Créer un environnement `CI` dans la configuration GitHub et une variable `MSTEAMS_WEBHOOK`

## Installation 💿

### Installation des dépendances 

```
pip3 install -r requirements.txt
```

### Configuration 

Modifiez la configuration en fonction des besoins dans le fichier [config.cfg](https://github.com/JMousqueton/boamp-extractor/blob/main/config.cfg).

## Usage

```
usage: boamp-extractor.py [-h] [-d] [-k <keyword>]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           increase output verbosity
  -k <keyword>, --keyword <keyword>
```

## Roadmap

| Status | Tâche | Remarque | Version |
|---|---|---|---|
| ✅ |~~Utiliser Github-Action~~| | |
| ✅ |~~Utiliser Github-Page~~| | |
| ✅ |~~Ajouter les statistiques~~| | |
| ✅ |~~Afficher les mots-clés~~| 🍾 | |
| 🟡 |Gérer les lots dans les AOs |  |
| 🔴 |Trier les AO par deadline  |  |
| ✅ |~~Ajouter "nouveau" pour les parutions de 24h et moins~~| les nouveaux AOs sont affichés avec une 🔥  |  |
| ✅ |~~Mettre les montants au format US (avec virgule pour les milliers)~~|  |
| ✅ |~~Suivi des modifications~~| Une page de changelog est mise à jour à chaque extraction |   |
| ✅ |~~Nettoyer le code pour supprimer l'écrire dans un fichier texte~~|  |  |
| 🛠 |Corriger les issues de chez [SonarCloud](https://sonarcloud.io/project/overview?id=JMousqueton_boamp-extractor)| |  |
| ✅ |~~Faire un fichier de configuration~~| Utilisation de [config.cfg](https://github.com/JMousqueton/boamp-extractor/blob/main/config.cfg) |  3.0 |
| ✅ |~~Utiliser la description longue si le titre est trop court~~ | | 3.1 | 
| ✅ |~~Rendre la date de début de recherche dynamique et configurable~~|   | 3.2 |
| ✅ |~~Rendre la légende dynamique~~ | En utilisant les variables de [config.cfg](https://github.com/JMousqueton/boamp-extractor/blob/main/config.cfg) | 3.3 |
| ✅ |~~Inclus OepnGraph~~ |  | 3.3 |
| ✅ |~~Notification Microsoft Teams~~ |  | 3.5 |

#### Légende

| Status | Description |
|---|---|
| ✅ | Réalisé |
| 🛠 | En cours |
| 🟢 | Priorité forte | 
| 🟡 | Priorité moyenne |
| 🔴 | Priorité faible |

## Auteur

👤 **Julien Mousqueton**

* Website: <https://julien.io>
* LinkedIn: [Julien Mousqueton](https://linkedin.com/in/julienmousqueton)
* Twitter: [@JMousqueton](https://twitter.com/JMousqueton)
* Github: [@JMousqueton](https://github.com/JMousqueton)

## Remerciements

 - [fr-boamp-api-extractor](https://github.com/bastien313/fr-boamp-api-extractor) pour l'inspiration 💡
 - [Guillaume Cresta](https://www.linkedin.com/in/guillaume-cresta-88185234) pour l'idée et les axes d'amélioration 📈
 - [Guillaume Zeja](https://twitter.com/guzefr) pour le support sur python et les encouragements 🍻
