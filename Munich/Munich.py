#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 15:46:27 2021

@author: rugi2
"""

import matplotlib.cm as cm
import matplotlib.colors as colors
import networkx as nx

from pprint import pprint


import osmnx as ox
ox.config(log_console=True, use_cache=True)
ox.__version__


# create a graph of a place's drivable street network then plot it
road = ox.graph_from_place('Munich, Germany', network_type='drive')
fig, ax = ox.plot_graph(road)

prj_road = ox.project_graph(road)


# project graph then calculate its nodes' convex hull area
road_proj = ox.project_graph(road)
nodes_proj = ox.graph_to_gdfs(road_proj, edges=False)
graph_area_m = nodes_proj.unary_union.convex_hull.area
graph_area_m


# save the network model to disk as a shapefile and graphml
ox.save_graph_shapefile(road_proj, filepath = r'/Users/rugi2/Documents/RUGI/OSMNX Project/Munich Data')


# calculate and print basic network stats
stats = ox.basic_stats(road_proj, area=graph_area_m, clean_intersects=True,circuity_dist='euclidean')
pprint(stats)




#calculate and visualize edge centrality
# edge closeness centrality: convert graph to a line graph so edges become nodes and vice versa
edge_centrality = nx.closeness_centrality(nx.line_graph(road))


# make a list of graph edge centrality values
ev = [edge_centrality[edge + (0,)] for edge in road.edges()]
# create a color scale converted to list of colors for graph edges
norm = colors.Normalize(vmin=min(ev)*0.8, vmax=max(ev))
cmap = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
ec = [cmap.to_rgba(cl) for cl in ev]
# color the edges in the original graph by closeness centrality in line graph
fig, ax = ox.plot_graph(road, bgcolor='black', node_size=0,
edge_color=ec, edge_linewidth=2, edge_alpha=1)



#CALCULATE AND VISUALISE NODE CENTRALITY
node_centrality = nx.closeness_centrality(road)

# plot it
import pandas as pd
df = pd.DataFrame(data=pd.Series(node_centrality).sort_values(), columns=['cc'])
df['colors'] = ox.plot.get_colors(n=len(df), cmap='inferno', start=0.2)
df = df.reindex(road.nodes())
nc = df['colors'].tolist()
fig, ax = ox.plot_graph(road, bgcolor='k', node_size=15, node_color=nc, node_edgecolor='none', node_zorder=2,
                        edge_color='#555555', edge_linewidth=1.5, edge_alpha=1)







#SREET NETWORK EDGE ORIENTATION/BEARING
import matplotlib.pyplot as plt

# calculate edge bearings and visualize their frequency
import pandas as pd
road = ox.add_edge_bearings(road)
bearings = pd.Series([data['bearing'] for u, v, k, data in road.edges(keys=True, data=True)])
ax = bearings.hist(bins=30, zorder=2, alpha=0.8)
xlim = ax.set_xlim(0, 360)
ax.set_title('Munich Street Network Orientation')
plt.show()

# polar plot
import numpy as np
n = 30
count, division = np.histogram(bearings, bins=[ang*360/n for ang in range(0,n+1)])
division = division[0:-1]
width =  2 * np.pi/n
ax = plt.subplot(111, projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction('clockwise')
bars = ax.bar(division * np.pi/180 - width * 0.5 , count, width=width, bottom=0.0)
ax.set_title('Munich Street Network Orientation', y=1.1)
plt.show()