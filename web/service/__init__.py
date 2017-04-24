import math


def gps_distance(lat1, lng1, lat2, lng2):
    return math.acos(
        math.cos(math.radians(lat1)) * math.cos(math.radians(lng1)) * math.cos(math.radians(lat2)) * math.cos(
            math.radians(lng2)) + math.cos(math.radians(lat1)) * math.sin(math.radians(lng1)) * math.cos(
            math.radians(lat2)) * math.sin(math.radians(lng2)) + math.sin(math.radians(lat1)) * math.sin(
            math.radians(lat2))) * 6372.795
