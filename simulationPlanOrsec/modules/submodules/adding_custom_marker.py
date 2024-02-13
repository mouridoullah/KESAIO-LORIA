import folium
def add_custom_marker(lon, lat, custom_icon, m, tooltip):
    # Crée un marqueur avec l'icône personnalisée et le tooltip spécifiés
    marker = folium.Marker((lat, lon), icon=custom_icon, tooltip=tooltip)
    marker.add_to(m)