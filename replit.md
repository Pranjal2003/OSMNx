# Urban Street Network Analysis

## Overview
This project performs computational network analysis on street networks of major cities worldwide using OpenStreetMap data. It visualizes and analyzes the topology and statistics of urban road networks.

## Purpose
- Analyze street network topology of major cities in Germany and India
- Generate various visualizations including basic networks, edge/node centrality, and orientation patterns
- Calculate network statistics such as node count, edge count, street length, and circuity

## Current State
Web application running on Flask that provides interactive visualization and analysis of city street networks.

## Recent Changes (November 18, 2025)
- Set up Flask web application for interactive network analysis
- Created web interface with city selection and multiple visualization types
- Integrated OSMnx library for street network data retrieval
- Added network statistics calculation endpoint
- Configured for Replit deployment

## Project Architecture

### Main Components
- **app.py**: Flask web server with visualization and statistics endpoints
- **templates/index.html**: Web interface for city selection and visualization
- **City Analysis Scripts**: Individual Python scripts for each city (Berlin, Munich, etc.)
- **Cache Directory**: Stores OSMnx cached network data

### Key Technologies
- **OSMnx**: Retrieves street network data from OpenStreetMap
- **NetworkX**: Graph analysis and centrality calculations
- **Matplotlib**: Visualization generation
- **Flask**: Web framework
- **GeoPandas**: Geospatial data handling

### Visualization Types
1. Basic Network: Simple street network visualization
2. Edge Centrality: Highlights important roads based on closeness centrality
3. Node Centrality: Highlights important intersections
4. Street Orientation: Polar plot showing directional distribution of streets

## Cities Analyzed

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

## Network Statistics Calculated
- Node count (intersections)
- Edge count (street segments)
- Total street length
- Average street length
- Intersection count
- Average node degree
- Circuity (deviation from straight-line distance)
