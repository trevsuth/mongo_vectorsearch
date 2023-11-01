from dotenv import load_dotenv
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
load_dotenv()

#set up mongo connection and navigate to collection
uri = os.getenv('MONGO_CONNECTION_STRING')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['sample_geospatial']
wrecks = db.shipwrecks

curser = db.shipwrecks.find( { } , { 'latdec':1, 'londec':1, 'watlev' : 1, '_id' : 0 } )
list_cur = list(curser)
df = pd.DataFrame(list_cur)

geometry = [Point(xy) for xy in zip(df['londec'], df['latdec'])]
gdf = GeoDataFrame(df, geometry=geometry)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax=world.plot(figsize=(15, 15))
gdf.plot(ax=ax,
        column='watlev',
        marker='o', 
        cmap='viridis', 
        markersize=15,
        legend=True)
plt.show()