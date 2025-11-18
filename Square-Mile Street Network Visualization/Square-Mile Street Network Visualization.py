

import osmnx as ox
from IPython.display import Image
#matplotlib inline
ox.config(log_console=True, use_cache=True)
ox.__version__


#Square-Mile Street Network Visualization/Figure Ground Diagrams


# configuring the inline image display
img_folder = 'images'
extension = 'png'
size = 240
dpi = 40

#Creatin diagrams for the cities by passing in a place name

place = 'Neubrandenburg, Germany'
fig, ax = ox.plot_figure_ground(address=place, network_type='drive', dpi=dpi)
Image('{}/{}.{}'.format(img_folder, place, extension), height=size, width=size)

place = 'Berlin, Germany'
fig, ax = ox.plot_figure_ground(address=place, network_type='drive', dpi=dpi)
Image('{}/{}.{}'.format(img_folder, place, extension), height=size, width=size)

place = 'Munich, Germany'
fig, ax = ox.plot_figure_ground(address=place, network_type='drive', dpi=dpi)
Image('{}/{}.{}'.format(img_folder, place, extension), height=size, width=size)

place = 'Frankfurt, Germany'
fig, ax = ox.plot_figure_ground(address=place, network_type='drive', dpi=dpi)
Image('{}/{}.{}'.format(img_folder, place, extension), height=size, width=size)

place = 'Hamburg, Germany'
fig, ax = ox.plot_figure_ground(address=place, network_type='drive', dpi=dpi)
Image('{}/{}.{}'.format(img_folder, place, extension), height=size, width=size)

place = 'Cologne, Germany'
fig, ax = ox.plot_figure_ground(address=place, network_type='drive', dpi=dpi)
Image('{}/{}.{}'.format(img_folder, place, extension), height=size, width=size)