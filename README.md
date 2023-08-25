## Installation:
- Clonez le projet  
- Installez les dépendances:  
`pip install requirements.txt`
- Créez la bdd PostgreSQL (vous pouvez vous baser sur les paramètres qui sont dans settings.py si vous le souhaitez)
- Ajoutez les infos de connexion de votre bdd dans la variable d'environnement
  DATABASES du fichier settings.py se trouvant dans le dossier project.
- Utilisez les commandes makemigrations & migrate pour initialiser la bdd:
  `python manage.py makemigrations` et `python manage.py migrate`
- Créez un utilisateur admin via `python manage.py createsuperuser`
- Connectez-vous à l'interface admin et créez deux groupes :
  - `sales_team` avec les permissions suivantes :
    - `epic_events | client | Can add client`
    - `epic_events | client | Can change client`
    - `epic_events | client | Can view client`
    - `epic_events | contract | Can change contract`
    - `epic_events | contract | Can view contract`
    - `epic_events | event | Can add event`
  - `support_team` avec les permissions suivantes :
    - `epic_events | client | Can view client`
    - `epic_events | contract | Can change event`
    - `epic_events | contract | Can view event`


