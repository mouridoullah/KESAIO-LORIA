def extract_coordinates(point_string):
    # Sépare la chaîne en x et y, puis convertit en float
    x, y = point_string.replace("Point(", "").replace(")", "").split()
    return float(x), float(y)