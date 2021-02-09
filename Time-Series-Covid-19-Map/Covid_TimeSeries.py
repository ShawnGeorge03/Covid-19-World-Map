import pandas as pd
import requests
import io
import geopandas as gpd
import matplotlib.pyplot as plt
import PIL
from PIL import Image

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
download = requests.get(url).content
data = pd.read_csv(io.StringIO(download.decode('utf-8')))

data = data.groupby('Country/Region').sum()
data = data.drop(columns= ['Lat', 'Long'])
data

world = gpd.read_file(r'./Mapping_Resource\World_Map.shp')
world

def checkIfExists():
    for index, row in data.iterrows():
        if index not in world['NAME'].to_list():
            print(index + ' is not in the list of countries of the shapefile')
        else:
            pass
checkIfExists()

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

checkIfExists()

merged = world.join(data, on='NAME', how='right')
merged

del url
del download
del data
del world
del checkIfExists

img_frames = []
for dates in merged.columns.to_list()[2: len(merged.columns.to_list())]:
    ax = merged.plot(column = dates,
                     cmap = 'YlOrRd',
                     figsize = (27,27),
                     legend = True,
                     scheme = 'user_defined',
                     classification_kwds = {'bins': [10, 20, 50, 100, 500, 1000, 5000, 10000, 500000, 1000000]},
                     edgecolor = 'black',
                     linewidth = 0.4)

    ax.set_title('Total Confirmed COVID-19 Cases on ' + dates,
                fontdict = {'fontsize': 20},
                pad = 12.5)

    ax.set_axis_off()

    ax.get_legend().set_bbox_to_anchor((0.18, 0.6))
    
    img = ax.get_figure()    
    f = io.BytesIO()
    img.savefig(f, format = 'png', bbox_inches='tight')
    
    ax.clear()
    plt.close(img)
   
    f.seek(0)
    img_frames.append(PIL.Image.open(f))
    
del merged


img_frames[0].save('Dynamic-COVID-19-Map.gif', 
                   format= 'GIF',
                   append_images = img_frames[1:],
                   save_all = True,
                  duration = 300,
                  loop = 1)
f.close()

del img_frames