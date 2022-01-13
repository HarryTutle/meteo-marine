# meteo_marine_traitement

Ce module permet à partir des données en libre accès de meteo france sur les bouées, bouées dérivantes et navires de passage disponibles de faire du machine learning. Il traite les données puis en sort 2 array; l'un servira de dataset et l'autre de cible (résultats attendus) pour faire de l'apprentissage supervisé. Le module est calibré pour traiter seulement les données de la bouée Gascogne (numéro : ) et de la bouée Brittany au large de Brest (numéro :).

Il comporte des fonctions et surtout une classe appelée Meteo_Marine_Classeur qui permet de calibrer notre dataset comme on veut avec les paramètres suivants :

- jours:(défaut=1) indique le nombre de jours que l'on veut par échantillon.Si on augmente ce nombre, on augmente les dimensions du dataset mais on réduit le nombre d'échantillons également.

- var_corbeille:(défaut=liste vide) dans cette liste on peut mettre les variables que l'on souhaite supprimer. On baisse le nombre de dimensions, au risque de louper des trucs. Les variables que l'on peut virer: latitude, longitude, temps, pression, force, direction, humidité, point_rosée, température. La variable temps correspond à quel mois la mesure a été prise (va de 1 à 12).

- vue:(défaut=12) règle l'amplitude horaire de la prévision. Par défaut on va avoir une prévision à 12 heures. Ce paramètre est limité par le paramètre jours; par exemple si on a jours=1, on ne pourra pas avoir vue>=24 heures. En revanche avec le paramètre jours=2, vue ne pourra alors pas être supérieur à 47.

- cible: (défaut='direction') règle quelle variable on veut prédire. ça peut-être: force, direction, humidité, pression, température, point_rosée.


Le programme 'voir un peu' indique comment importer les données et utiliser ce module. Ligne 24, on utilise glob pour importer les données stockées dans un fichier du pc. On indique le chemin pour ce fichier et le tour est joué ! Ensuite via du regex on peut se limiter à quelques fichiers si on le souhaite.


 
