# P11 - Améliorez un projet existant en Python.

Voici les améliorations apportées au projet 8 :  
- Les utilisateurs peuvent changer leurs nom, prénoms et mot de passe.  
- Fonctionnalité "Mot de passe oublié".  
- Ajout des tests selenium.  
- Sauvegarde des produits sélectionnés avec des variables de session pour les utilisateurs non connectés.  

### Installation
1. Virtualenv & requirements.txt
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

2. Variables d'environnement
```
NAME="nom_de_la_bdd"
USER="votre_nom"
PASSWORD="mot_de_passe"
SENDGRID_API_KEY="clé_api"
```

3. Faire les migrations
```
./manage.py migrate
```

4. Lancer les tests
```
./manage.py test
```

5. Remplir la base de données
```
./manage.py add-level -l "low"
./manage.py add-level -l "moderate"
./manage.py add-level -l "high"

# add-product -n [nutriscore] -c [catégorie]
./manage.py add-product -n "a" -c "Desserts"
```