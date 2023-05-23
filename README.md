[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# SoftDesk

## About The Project

SoftDesk est un projet d'API en utilisant Django RestFramework dans le cadre d'une formation.

L'objectif de l'API SoftDesk est de permettre à ses utilisateurs de remonter et suivre des problèmes techniques qui concernent les projets dont ils ont la gestion.
Cette solution s'adresse à des entreprises clientes, en B2B.

## Technologies

- Python 3.10

## Getting Started

### Installation (Windows)

1. Pour installer Python, vous pouvez vous rendre sur https://wiki.python.org/moin/BeginnersGuide/Download
2. Pour créer un environnement virtuel, saisissez dans votre terminal à l'endroit où vous souhaitez le créer:
    - `python -m venv env`
3. Pour activer votre environnement, saisissez:
    - `source env/Scripts/activate`
4. Il vous faudra ensuite installer les packages dans votre environnement. Pour cela:
   - Allez dans le dossier P10_Projet_SoftDesk/softdesk
   - Installez les packages avec la commande ci-dessous:
     - `pip install -r requirements.txt`

### Usage

1. Pour lancer le serveur local, allez dans le dossier softdesk et utilisez dans votre terminal la commande suivante:
    - `python manage.py runserver`
2. Ouvrez un navigateur internet, et tapez dans la barre de recherche "http://localhost:8000/" pour accéder à l'API

Des exemples utilisateurs sont inclus dans la base de donnée.
Pour se connecter avec un exemple d'utilisateur, saissisez dans la page login les identifiants suivants:
- Nom d'utilisateur: toto
- Mot de passe: Hello1234!

## Features

- Création d'un compte utilisateur.
- CRUD d'un projet, d'un problème, d'un commentaire lorsque l'utilisateur en est son créateur/auteur.
- Création et lecture (CR) d'un projet, d'un problème, d'un commentaire lorsque l'utilisateur est un contributeur du projet.
- Ajout et suppression d'un contributeur, pour le créateur d'un projet.

## Author

Vpich
