
# BOAMP Extractor 

> BOAMP-Extractor permet d'extraire les offres de marchés publics publiées au bulletin officiel des annonces des marchés publics (BOAMP).
L'extraction se base sur des mots clefs
Le script ignore les appels d'offres dont la date limite de réponse est dépassée.

## Badges
[![boamp-extractor](https://github.com/JMousqueton/boamp-extractor/actions/workflows/boamp-extractor.yml/badge.svg)](https://github.com/JMousqueton/boamp-extractor/actions/workflows/boamp-extractor.yml)[![pages-build-deployment](https://github.com/JMousqueton/boamp-extractor/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/JMousqueton/boamp-extractor/actions/workflows/pages/pages-build-deployment)

[![Twitter: JMousqueton](https://img.shields.io/twitter/follow/JMousqueton.svg?style=social)](https://twitter.com/JMousqueton)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

## Documentation

### En utilisant les fichiers de configuration 
Renseignez les mots-clés de recherches dans le fichier `keywords.txt` avec un mot ou une expression par ligne.

Il est possible d'exclure les appels d'offres contenants certains mots-clés.
Pour cela, renseignez les mots interdits dans le fichier `exception.txt` avec un mot ou une expression par ligne.
Les appels d'offres exclus par ce biais seront tout de même inscrits dans le fichier `annoncesrejetees.txt`.

### En ligne de commande 

Lancez le script `extractor.py` avec l'option `-k` suivi du mot clef recherché 

Le résultat sera généré dans le fichier `annonces.txt` (ou dans le fichier spécifié avec l'option `-o`)

## En utilisant Github-Action 

Voir le fichier [boamp-extractor](https://github.com/JMousqueton/boamp-extractor/blob/main/.github/workflows/boamp-extractor.yml)

## Usage

```
usage: extractor.py [-h] [-d] [-k <keyword>] [-l] [-o <filename>]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           increase output verbosity
  -k <keyword>, --keyword <keyword>
                        the keyword
  -l, --list            use a list from file recherche.txt
  -o <filename>, --output <filename>
                        outputfile
```

## Roadmap

- ~~Utiliser Github-Action~~ 

- ~~Utiliser Github-Page~~


## Author

👤 **Julien Mousqueton**

* Website: <https://www.julienmousqueton.fr>
* LinkedIn: [Julien Mousqueton](https://linkedin.com/in/julienmousqueton)
* Twitter: [@JMousqueton](https://twitter.com/JMousqueton)
* Github: [@JMousqueton](https://github.com/JMousqueton)


## Acknowledgements

 - [fr-boamp-api-extractor](https://github.com/bastien313/fr-boamp-api-extractor) pour l'inspiration 
 - [Guillaume Cresta](https://www.linkedin.com/in/guillaume-cresta-88185234) pour l'idée et les axes d'amélioration
