Onjectif :
Pour le projet nous avons décidé de réaliser une application permettant de comparer les statistiques de plusieurs
pilotes de formule 1.
Outils utilisés :
Pour cela nous avons utilisé Docker pour mettre dans des conteneurs notre base de donnée et notre application
Ainsi que MongoDB pour stocker les données à propos des pilotes

Prérequis :
Les prérequis sont d'avoir Docker, Python et MongoDB d'installés
Ensuite il faut executer les commandes pour build et run les conteneurs de la base de donnée et de l'application
ainsi que de les mettre sur le même réseau :
On créé d'abbord le réseau :
docker network create my_network
On build ensuite l'image de MongoDB :
docker build -t my_mongodb_image .
On run le conteneur :
docker run -d --name mongodb --network my_network -p 27017:27017 mongo
On peut ensuite lancer la spider depuis le fichier de f1_spider.py :
scrapy crawl f1
On build de la même façon pour l'application :
docker build -t dashboard_image .
Run :
docker run -d --name dashboard_app --network my_network -p 8050:8050 dashboard_image
Il ne reste plus qu'à se connecter à : http://localhost:8050 pour arriver sur l'application

Dans ce projet, nous utilisons un réseau Docker personnalisé pour que dashboard_app puisse communiquer avec mongodb.

Le réseau my_network permet aux conteneurs de se voir par leurs noms DNS.
MongoDB et dashboard_app doivent être connectés à ce même réseau.

Pourquoi Dash ?
Utilisation simple sans avoir besoin d'un front-end complexe, compatible avec Pandas, Plotly et MongoDB.
Réactivité : Les graphiques sont mis à jour en fonction des sélections de l'utilisateur.
Nous récupérons les données depuis MongoDB via pymongo et génèrons des graphiques interactifs comparant les 
statistiques des pilotes.

Pourquoi MongoDB ?
Flexibilité des données, intégration avec Python : pymongo permet de récupérer et manipuler les données facilement.
Nous alimentons MongoDB avec les données des pilotes via Scrapy.
Dash récupère les données dynamiquement pour les afficher sous forme de graphiques.

Nous avons rencontré des problèmes :
Récupération des données sur le site via Scrapy : nous avons dû changer de site car le premier était trop 
difficile à scraper, sur le 2ème il était parfois difficile de prendre seulement les données qui nous interessaient
Cela mène au plus gros problème qui est la gestion des données et leur attribution, comme elles n'étaient pas 
toutes pareilles pour chque pilote, cela a causé des soucis lors de la réalisation des graphiques.
Enfin la connexion de l'app sur docker avec la création du réseau et de l'image spécifique.

Axes d'amélioratio :
Finalement nous n'avons pas réussi à avoir résultat attendu sur un graphique a cause de la manière dont étaient 
scrappées les données et d'un manque de temps pour recommencer sur un autre site ou d'une autre manière
Mettre en place d'autres graphiques de comparaison sur les autres données que nous avions à notre disposition