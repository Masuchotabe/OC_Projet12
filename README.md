# OC_Projet12
Openclassrooms - Projet 12 : Développez une architecture back-end sécurisée avec Python et SQL

commande docker : 
`docker run --name some-mysql -e MYSQL_ROOT_PASSWORD={YOUR_ROOT_PASSWORD} -d mysql:latest`

# Installation
Installation des requirements  
`pipenv install`
 
Create `.env` file from `.env.template` and set the different variables.  

Création des tables  
`pipenv run alembic upgrade head`

# Développement 

`alembic revision --autogenerate -m "{MIGRATION DESCRIPTION}"`

# Utilisation

Se déplacer dans le répertoire src. 
```shell
cd /src
```

Se connecter  
`python main.py user-login`

## LINUX 

Vous recevrez un token si vos identifiants sont corrects. 
Stocker votre token dans une variable : 
```shell
# linux
mon_token=<VOTRE TOKEN>
```
```shell
# windows (cmd)
set mon_token=<VOTRE TOKEN>
```

Ensuite, appelez une commande de la manière suivante pour utiliser votre token : 
```shell
# linux
python main.py create-user $mon_token
```
```shell
# windows
python main.py create-user %mon_token%
```



### To improve 
- improve customer selection for contract creation 