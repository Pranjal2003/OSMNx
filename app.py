from flask import Flask, render_template, request, jsonify
import osmnx as ox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import networkx as nx
import pandas as pd
import numpy as np
import io
import base64
from pathlib import Path

app = Flask(__name__)

ox.settings.log_console = False
ox.settings.use_cache = True

CITIES = [
    'Berlin, Germany',
    'Munich, Germany',
    'Hamburg, Germany',
    'Cologne, Germany',
    'Frankfurt, Germany',
    'Neubrandenburg, Germany',
    'Delhi, India',
    'Mumbai, India',
    'Bengaluru, India',
    'Varanasi, India',
    'Chennai, India',
    'Kolkata, India'
]

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

def generate_graph_visualization(place, viz_type='basic'):
    """Generate various visualizations of city street networks"""
    try:
        print(f"Fetching network data for {place}...")
        road = ox.graph_from_place(place, network_type='drive')
        print(f"Network data fetched successfully. Processing {len(road.nodes)} nodes...")
        
        fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
        
        if viz_type == 'basic':
            ox.plot_graph(road, ax=ax, node_size=0, edge_color='black', 
                         edge_linewidth=0.5, bgcolor='white')
            
        elif viz_type == 'edge_centrality':
            edge_centrality = nx.closeness_centrality(nx.line_graph(road))
            ev = [edge_centrality[edge + (0,)] for edge in road.edges()]
            norm = colors.Normalize(vmin=min(ev)*0.8, vmax=max(ev))
            cmap_obj = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
            ec = [cmap_obj.to_rgba(cl) for cl in ev]
            ox.plot_graph(road, ax=ax, bgcolor='black', node_size=0,
                         edge_color=ec, edge_linewidth=2, edge_alpha=1)
            
        elif viz_type == 'node_centrality':
            node_centrality = nx.closeness_centrality(road)
            df = pd.DataFrame(data=pd.Series(node_centrality).sort_values(), columns=['cc'])
            df['colors'] = ox.plot.get_colors(n=len(df), cmap='inferno', start=0.2)
            df = df.reindex(road.nodes())
            nc = df['colors'].tolist()
            ox.plot_graph(road, ax=ax, bgcolor='k', node_size=15, node_color=nc, 
                         node_edgecolor='none', node_zorder=2,
                         edge_color='#555555', edge_linewidth=1.5, edge_alpha=1)
            
        elif viz_type == 'orientation':
            road = ox.add_edge_bearings(road)
            bearings = pd.Series([data['bearing'] for u, v, k, data in road.edges(keys=True, data=True)])
            
            n = 30
            count, division = np.histogram(bearings, bins=[ang*360/n for ang in range(0,n+1)])
            division = division[0:-1]
            width = 2 * np.pi/n
            
            ax = plt.subplot(111, projection='polar')
            ax.set_theta_zero_location('N')
            ax.set_theta_direction('clockwise')
            bars = ax.bar(division * np.pi/180 - width * 0.5, count, width=width, bottom=0.0)
            ax.set_title(f'{place} Street Network Orientation', y=1.1, fontsize=16)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close(fig)
        
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return img_base64
        
    except Exception as e:
        print(f"Error generating visualization: {e}")
        return None

def get_network_stats(place):
    """Calculate basic network statistics"""
    try:
        print(f"Fetching network data for {place}...")
        road = ox.graph_from_place(place, network_type='drive')
        print(f"Network data fetched. Calculating statistics...")
        road_proj = ox.project_graph(road)
        nodes_proj = ox.graph_to_gdfs(road_proj, edges=False)
        graph_area_m = nodes_proj.unary_union.convex_hull.area
        
        stats = ox.basic_stats(road_proj, area=graph_area_m)
        
        formatted_stats = {
            'Nodes': stats.get('n', 'N/A'),
            'Edges': stats.get('m', 'N/A'),
            'Total Street Length (km)': f"{stats.get('street_length_total', 0) / 1000:.2f}" if 'street_length_total' in stats else 'N/A',
            'Average Street Length (m)': f"{stats.get('street_length_avg', 0):.2f}" if 'street_length_avg' in stats else 'N/A',
            'Intersection Count': stats.get('intersection_count', 'N/A'),
            'Street Density (km/km²)': f"{stats.get('street_density_km', 0):.2f}" if 'street_density_km' in stats else 'N/A',
            'Average Circuity': f"{stats.get('circuity_avg', 0):.3f}" if 'circuity_avg' in stats else 'N/A',
            'Self-Loop Count': stats.get('self_loop_proportion', 'N/A'),
        }
        
        return formatted_stats
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return {'Error': str(e)}

@app.route('/')
def index():
    return render_template('index.html', cities=CITIES)

@app.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    place = data.get('city')
    viz_type = data.get('viz_type', 'basic')
    
    if place not in CITIES:
        return jsonify({'error': 'Invalid city'}), 400
    
    img_data = generate_graph_visualization(place, viz_type)
    
    if img_data:
        return jsonify({'image': img_data})
    else:
        return jsonify({'error': 'Failed to generate visualization'}), 500

@app.route('/stats', methods=['POST'])
def stats():
    data = request.json
    place = data.get('city')
    
    if place not in CITIES:
        return jsonify({'error': 'Invalid city'}), 400
    
    stats_data = get_network_stats(place)
    return jsonify(stats_data)

if __name__ == '__main__':
    Path('static/generated').mkdir(parents=True, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=False)
