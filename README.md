# Street-Name-Analysis
Where in France are located streets with a given name? 
======================================================

This project has two scripts

1.street_name_analysis_point.py

The user is asked for a street name. The script returns the number of streets having this name in France in a CSV file and shows them as red dots on a map.

A PostgreSQL database with two tables is used. The first table is referred to as france in the SQL query and can be downloaded  from https://www.data.gouv.fr/en/datasets/base-d-adresses-nationale-ouverte-bano/
The other table is referred to as communes-departements-regions and can be downloaded from https://www.data.gouv.fr/en/datasets/communes-de-france-base-des-codes-postaux/

A typical result is shown below.

![Map with dots for Debussy](https://raw.githubusercontent.com/Joulik/Street-Name-Analysis/master/Debussy-point.png)

2.street_name_analysis_density.py

The user is asked for a street name. The script returns the total number of streets with this street name per region and shows the result on a map. A typical result is shown below.

![Result on console](https://raw.githubusercontent.com/Joulik/Street-Name-Analysis/master/ConsoleDensity.png)

![Density map for Debussy](https://raw.githubusercontent.com/Joulik/Street-Name-Analysis/master/Debussy-density.png)

External packages required
--------------------------
-descartes

-geopandas

-matplotlib.pyplot

-pandas

-psycopg2

-shapely.geometry
