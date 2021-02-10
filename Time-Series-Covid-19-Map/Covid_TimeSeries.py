import pandas as pd
import requests
import io
import geopandas as gpd
import matplotlib.pyplot as plt
import PIL
from PIL import Image
import pathlib

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
download = requests.get(url).content

data = pd.read_csv(io.StringIO(download.decode('utf-8')))
data = data.groupby('Country/Region').sum()
data = data.drop(columns= ['Lat', 'Long'])

world = gpd.read_file(r'./Mapping_Resource/World_Map.shp')

world.replace('Viet Nam', 'Vietnam', inplace = True)
world.replace('Brunei Darussalam', 'Brunei', inplace = True)
world.replace('Cape Verde', 'Cabo Verde', inplace = True)
world.replace('Democratic Republic of the Congo', 'Congo (Kinshasa)', inplace = True)
world.replace('Congo', 'Congo (Brazzaville)', inplace = True)
world.replace('Czech Republic', 'Czechia', inplace = True)
world.replace('Swaziland', 'Eswatini', inplace = True)
world.replace('Iran (Islamic Republic of)', 'Iran', inplace = True)
world.replace('Korea, Republic of', 'Korea, South', inplace = True)
world.replace("Lao People's Democratic Republic", 'Laos', inplace = True)
world.replace('Libyan Arab Jamahiriya', 'Libya', inplace = True)
world.replace('Republic of Moldova', 'Moldova', inplace = True)
world.replace('The former Yugoslav Republic of Macedonia', 'North Macedonia', inplace = True)
world.replace('Syrian Arab Republic', 'Syria', inplace = True)
world.replace('Taiwan', 'Taiwan*', inplace = True)
world.replace('United Republic of Tanzania', 'Tanzania', inplace = True)
world.replace('United States', 'US', inplace = True)
world.replace('Palestine', 'West Bank and Gaza', inplace = True)
world.replace('Holy See (Vatican City)', 'Holy See', inplace = True)
world.replace('Micronesia, Federated States of', 'Micronesia', inplace = True)

merged = world.join(data, on='NAME', how='right')

del url
del download
del data
del world

frames = []

def addFrames(path):
    frames.append(Image.open(path))

for dates in merged.columns.to_list()[2:len(merged.columns.to_list())]:
    path = pathlib.Path('./Covid-Time-Pictures/img-' + dates.replace("/","-") + '.png')
    if not path.exists():
        ax = merged.plot(column = dates,
                         cmap = 'YlOrRd',
                         figsize = (27,27),
                         legend = True,
                         scheme = 'user_defined',
                         classification_kwds = {
                             'bins': [10, 100, 500, 1000, 10000, 500000, 1000000, 10000000, 15000000, 20000000]},
                         edgecolor = 'black',
                         linewidth = 0.4)

        ax.set_title('Total Confirmed COVID-19 Cases on ' + dates,
                     fontdict = {'fontsize': 20},
                     pad = 12.5)

        ax.set_axis_off()

        ax.get_legend().set_bbox_to_anchor((0.18, 0.6))

        img = ax.get_figure()   
        img.savefig("./Covid-Time-Pictures/img-" + dates.replace("/","-") + ".png", 
                    format = 'png', 
                    bbox_inches='tight')
        ax.clear()
        plt.close(img)
        del ax
        del img    
    addFrames("./Covid-Time-Pictures/img-" + dates.replace("/","-") + ".png")        
    del path
del dates

del merged

frames[0].save('Dynamic-COVID-19-Map.gif',
               format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=300,
               loop=1)
del frames