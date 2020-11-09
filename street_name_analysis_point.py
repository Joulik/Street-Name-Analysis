import descartes
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2 as pg2
from shapely.geometry import Point,Polygon

# Get input from user
street_name = input("Please indicate the street name you are interested in.\n")
street_name_title = street_name
street_name = "'%{}%'".format(street_name)
print('Processing, please wait')

# Connect to PosgreSQL database
conn = pg2.connect(database='Adresses-France', user='postgres',password='topSQL')

# PostgreSQL query
query = '''
  SELECT COUNT(aa.nom_comm),aa.nom_region
	FROM
		(SELECT DISTINCT(fr.nom_comm),fr.voie,fr.code_post,
        cdr.nom_region,cdr.latitude,cdr.longitude
    	FROM france AS fr
        JOIN communes_departement_region AS cdr
	  	ON fr.nom_comm=cdr.nom_commune
        AND fr.code_post=cdr.code_postal
      WHERE fr.voie LIKE {}) AS aa
	GROUP BY aa.nom_region
  ;
  '''.format(street_name)

# Create data frame resulting from PostgreSQL query
df = pd.read_sql_query(query, conn)

# Select map of France
france_map = gpd.read_file(r'C:\Users\Thirteen\Desktop\PYTHON\StreetNameAnalysisFRANCE\regions-20180101-shp\regions-20180101.shp')

# Exclude oversea regions
regions_to_exclude = ['Guadeloupe','Martinique','Guyane','La Réunion','Mayotte']
ddf = pd.merge(france_map['nom'],
               df[['count','nom_region']],
               how='outer',
               left_on='nom',
               right_on='nom_region')[['count','nom']].fillna(0)
ddf = ddf[~ddf['nom'].isin(regions_to_exclude)]

# Print counts of street name per region
print(ddf)

# Prepare map of France
france_map.set_crs(epsg=4326, inplace=True)
france_map.to_crs(epsg=3395)
france_map = france_map[~france_map['nom'].isin(regions_to_exclude)]

# Plot and save picture of geodataframe
ax = france_map.plot(column=ddf['count'], edgecolor='black', cmap='OrRd',vmin=0,legend=True)
ax.set_xticks([])
ax.set_yticks([])
plt.title(street_name_title)
file_name = '{}-density.png'.format(street_name_title)
plt.savefig(fname=file_name,bbox_inches='tight',format='png',dpi=300)
plt.show()