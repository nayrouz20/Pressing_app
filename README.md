🧺 Pressing Management App
📌 Description

Cette application web développée avec Django permet de gérer un service de pressing (lavage à sec).
Les utilisateurs peuvent :

Créer un compte et se connecter.

Parcourir les articles disponibles (qu'on peut laver) et les ajouter à leur panier.

Passer une commande et suivre son statut (LINGE_RECU → EN_COURS → PRET_A_LIVRER).

Consulter l’historique de leurs commandes non livrées.

L’administrateur peut :

Valider, traiter et mettre à jour le statut des commandes.

Gérer les articles de vêtements disponibles.

⚙️ Fonctionnalités principales

Authentification utilisateur (inscription / connexion / déconnexion).

Gestion du panier (ajout, suppression, visualisation).

Suivi en temps réel de l’état des commandes.

Interface d’administration Django pour la gestion des commandes et des vêtements.

🚀 Installation et exécution
1️⃣ Cloner le projet
git clone https://github.com/nayrouz20/pressing-app.git
cd pressing-app

2️⃣ Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Installer les dépendances
pip install -r requirements.txt

4️⃣ Appliquer les migrations
python manage.py migrate

5️⃣ Créer un superutilisateur (admin)
python manage.py createsuperuser

6️⃣ Lancer le serveur
python manage.py runserver


Ensuite, rendez-vous sur http://127.0.0.1:8000
 
📂 Structure du projet
pressing-app/
│── pressing/            # Application Django principale
│── templates/           # Templates HTML
│── static/              # Fichiers CSS, JS, images
│── db.sqlite3           # Base de données SQLite
│── manage.py            # Fichier principal Django
│── requirements.txt     # Dépendances Python

