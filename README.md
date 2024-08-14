# OC_Projet12
Openclassrooms - Projet 12 : Développez une architecture back-end sécurisée avec Python et SQL

commande docker : 
`docker run --name some-mysql -e MYSQL_ROOT_PASSWORD={YOUR_ROOT_PASSWORD} -d mysql:latest`

# Installation
Installation des requirements  
`pipenv install`

Création des tables  
`pipenv run alembic upgrade head`

# Développement 

`alembic revision --autogenerate -m "{MIGRATION DESCRIPTION}"`