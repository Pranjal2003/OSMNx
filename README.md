# Urban Street Network Analysis

A web application for analyzing and visualizing street network topology and statistics of major cities worldwide using OpenStreetMap data.

## Features

### 📊 Network Statistics
Calculate comprehensive network metrics for any city:
- **Nodes & Edges**: Count of intersections and street segments
- **Street Length**: Total and average street length
- **Street Density**: Road network density per square kilometer
- **Circuity**: Measures how direct vs. winding the streets are
- **Intersection Count**: Number of street intersections

### 🗺️ Visualizations
Generate multiple types of street network visualizations:
1. **Basic Network**: Simple street map visualization
2. **Edge Centrality**: Highlights the most important roads based on network connectivity
3. **Node Centrality**: Highlights the most important intersections
4. **Street Orientation**: Polar plot showing the directional distribution of streets

## Cities Included

### German Cities
- Berlin, Germany
- Munich, Germany
- Hamburg, Germany
- Cologne, Germany
- Frankfurt, Germany
- Neubrandenburg, Germany

### Indian Cities
- Delhi, India
- Mumbai, India
- Bengaluru, India
- Varanasi, India
- Chennai, India
- Kolkata, India

## How to Use

1. **Select a City**: Choose from the dropdown menu
2. **Choose Visualization Type**: Pick from basic network, centrality views, or orientation analysis
3. **Generate Visualization**: Click to create a visual map (may take 30-60 seconds for larger cities)
4. **Get Network Statistics**: Click to calculate detailed network metrics

## Technology Stack

- **Backend**: Flask + Gunicorn
- **Data Source**: OpenStreetMap via OSMnx
- **Analysis**: NetworkX for graph algorithms
- **Visualization**: Matplotlib
- **Geospatial**: GeoPandas, Shapely

## Running Locally

The application is configured to run on port 5000:

```bash
gunicorn --bind=0.0.0.0:5000 --timeout 180 app:app
```

## Note on Performance

- First-time city requests will download data from OpenStreetMap (cached for future use)
- Larger cities (Berlin, Munich, Hamburg) take longer to process
- Visualizations are generated on-demand and may take 30-60 seconds

## Research Context

This project implements computational network analysis techniques to study urban street topology. The analysis includes:
- Centrality measures (betweenness, closeness)
- Network connectivity patterns
- Street orientation and grid patterns
- Comparative urban morphology

Based on research in urban network analysis and computational geography.
