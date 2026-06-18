import geopandas as gpd
import pandas as pd
import folium
import os
import logging

# Get the base directory (backend directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Go up one level to project root

# Ensure logs directory exists
logs_dir = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logging.basicConfig(
    filename=os.path.join(logs_dir, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generate_religion_map(df, output_dir):
    try:
        logging.info("📍 Generating religion map...")

        # Check required columns
        required_columns = {'धर्म', 'विधानसभा'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            logging.error(f"❌ DataFrame is missing required columns: {missing}")
            return

        # Load India shapefile
        shapefile_path = 'data/constituency_shapefile/india_constituencies.shp'
        if not os.path.exists(shapefile_path):
            logging.error(f"❌ Shapefile not found at: {shapefile_path}")
            return

        gdf = gpd.read_file(shapefile_path)
        logging.info("✅ Shapefile loaded.")

        constituency_name = df['विधानसभा'].iloc[0]
        logging.info(f"📍 Target Constituency: {constituency_name}")

        # Match constituency
        match = gdf[gdf['const_name'].str.contains(constituency_name, case=False, na=False)]
        if match.empty:
            logging.warning(f"❌ No match found for constituency '{constituency_name}' in shapefile.")
            return

        constituency_shape = match.iloc[0].geometry
        centroid = constituency_shape.centroid
        m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12)

        # Plot constituency boundary
        folium.GeoJson(constituency_shape, name='Constituency Boundary').add_to(m)

        # Religion data
        religion_counts = df['धर्म'].value_counts().to_dict()
        total = sum(religion_counts.values())
        popup_content = "<br>".join(
            [f"{rel}: {cnt} ({cnt * 100 / total:.1f}%)" for rel, cnt in religion_counts.items()]
        )
        logging.info(f"📊 Religion breakdown: {religion_counts}")

        # Add marker
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=popup_content,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        # Save the map
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        map_path = os.path.join(output_dir, 'religion_map.html')
        m.save(map_path)
        logging.info(f"✅ Map saved to {map_path}")

    except Exception as e:
        logging.error(f"❌ Error generating religion map: {str(e)}")
