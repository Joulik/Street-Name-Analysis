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
conn = pg2.connect(database='Adresses-France', user='xxxxx',password='xxxxx')

# PostgreSQL query
query = '''
      SELECT DISTINCT(fr.nom_comm),fr.voie,fr.code_post,
        cdr.nom_region,cdr.latitude,cdr.longitude
        FROM france AS fr
        JOIN communes_departement_region AS cdr
	  ON fr.nom_comm=cdr.nom_commune AND fr.code_post=cdr.code_postal
        WHERE fr.voie LIKE {}
	  AND cdr.nom_region
	  IN ('Auvergne-Rhône-Alpes',
		'Bourgogne-Franche-Comté',
		'Bretagne',
		'Centre-Val de Loire',
		'Corse',
		'Grand Est',
		'Hauts-de-France',
		'Île-de-France',
		'Pays de la Loire',
		'Normandie',
		'Nouvelle-Aquitaine',
		'Occitanie',
        'Provence-Alpes-Côte d''Azur')
      ORDER BY cdr.nom_region
        ;
        '''.format(street_name)

# Create data frame resulting from PostgreSQL query
df = pd.read_sql_query(query, conn)

# Proceed if dataframe is not empty
if not df.empty:
	# Prepare geometry for geodataframe
	geometry = gpd.points_from_xy(df.longitude, df.latitude)
	gdf = gpd.GeoDataFrame(df, geometry=geometry)

	# Update coordinate reference system
	gdf.set_crs(epsg=4326, inplace=True)
	gdf.to_crs(epsg=3395)

	# Display ten first matches
	print('10 first hits')
	print(df[['voie','nom_comm','code_post','nom_region']].head(10))

	# Write results in csv file
	file_name = '{}.csv'.format(street_name_title)
	df[['voie','nom_comm','code_post','nom_region']].to_csv(file_name)

	# Display the total number of matches
	print("{} hits for that street name".format(len(gdf.index)))

	# Prepare map of France
	france_map = gpd.read_file(r'C:\Users\Thirteen\Desktop\PYTHON\StreetNameAnalysisFRANCE\regions-20180101-shp\regions-20180101.shp')

	# Update coordinate reference system
	france_map.set_crs(epsg=4326, inplace=True)
	france_map.to_crs(epsg=3395)

	# Exclude overseas regions
	regions_to_exclude = ['Guadeloupe','Martinique','Guyane','La Réunion','Mayotte']
	france_map = france_map[~france_map['nom'].isin(regions_to_exclude)]

	# Plot and save picture of geodataframe in PNG file
	ax = france_map.plot(color='white', edgecolor='black')
	ax.set_xticks([])
	ax.set_yticks([])
	gdf.plot(ax=ax, color='red', markersize=5)
	plt.title(street_name_title)	
	file_name = '{}-point.png'.format(street_name_title)
	plt.savefig(fname=file_name,bbox_inches='tight',format='png',dpi=300)
	plt.show()
# In case no result is found
else:
	print('No result found for your request')
