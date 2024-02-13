import math
def intermediate_point(point1, point2, distance):
    lat1 = math.radians(float(point1[0]))
    lon1 = math.radians(float(point1[1]))
    lat2 = math.radians(float(point2[0]))
    lon2 = math.radians(float(point2[1]))

    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1

    a = math.sin(delta_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    # dist = 6371000 * c  

    azimuth = math.atan2(math.sin(delta_lon) * math.cos(lat2), math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))

    intermediate_lat = math.asin(math.sin(lat1) * math.cos(distance / 6371000) +
                                 math.cos(lat1) * math.sin(distance / 6371000) * math.cos(azimuth))
    intermediate_lon = lon1 + math.atan2(math.sin(azimuth) * math.sin(distance / 6371000) * math.cos(lat1),
                                         math.cos(distance / 6371000) - math.sin(lat1) * math.sin(intermediate_lat))

    intermediate_lat = math.degrees(intermediate_lat)
    intermediate_lon = math.degrees(intermediate_lon)

    return intermediate_lat, intermediate_lon