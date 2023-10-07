import math

import overpy
from geopy import distance

from sport_activities_features import ElevationIdentification


class OverpyNodesReader:

    """Class for working with Overpass nodes (Overpy.node).
    The purpose is to generate a dictionary object similar to those
    generated by TCXFile and GPXFile classes.\n
    Args:
        open_elevation_api (str):
            location of the Open Elevation Api.
    """

    def __init__(
        self,
        open_elevation_api:
            str = 'https://api.open-elevation.com/api/v1/lookup?',
    ) -> None:
        """Initialisation method for OverpyNodesReader.\n
        Args:
            open_elevation_api (str):
                address of Open Elevation API, if a lot of altitudes
                are needed, self hosting is prefferable.
        """
        self.open_elevation_api = open_elevation_api

    def __map_payload(self, node: tuple) -> dict:
        """Method that converts touple into JSON like object
        for equerying the Open Elevation API.\n
        Args:
            position (tuple):
                tuple of latitude and longitude
        Returns:
            JSON like object {
                'latitude': float(position[0]),
                'longitude': float(position[1]),
            }.
        """
        return {
            'latitude': float(node.lat),
            'longitude': float(node.lon),
        }

    def read_nodes(
        self,
        nodes: overpy.Node,
        cumulative_distances: bool = True,
    ) -> dict:
        """Method for reading overpy.Node nodes and generating a
        TCXFile/GPXFile like dictionary of objects.\n
        Args:
            nodes (list):
                list of overpy.Node objects
            cumulative_distances (bool):
                If set to True, distance equals previous point
                distance + distance between the nodes,
                else tells actual distance between two points.

        Returns: dictionary of nodes.
            {
                'activity_type': str,
                'positions': [...],
                'altitudes': [...],
                'distances': [...],
                'total_distance': float
            }
        """
        activity_type = 'Overpy nodes'

        positions = []
        altitudes = []
        distances = []
        total_distance = None

        nodes = list(map(self.__map_payload, nodes))
        elevation_identification = ElevationIdentification(
            open_elevation_api=self.open_elevation_api,
            positions=nodes,
        )
        altitudes = elevation_identification.fetch_elevation_data(
            payload_formatting=False,
        )

        node: overpy.node
        prevNode = nodes[0]

        for i in range(len(nodes)):
            node = nodes[i]
            positions.append((node['latitude'], node['longitude']))
            if i != 0:
                flat_distance = distance.distance(
                    (node['latitude'], node['longitude']),
                    (prevNode['latitude'], prevNode['longitude']),
                ).meters
                euclidean_distance = math.sqrt(
                    flat_distance ** 2
                    + abs(altitudes[i] - altitudes[i - 1]) ** 2,
                )
                if cumulative_distances:
                    distances.append(euclidean_distance+distances[-1])
                else:
                    distances.append(euclidean_distance)
            else:
                distances.append(0)
            prevNode = node
        try:
            if cumulative_distances:
                total_distance = distances[-1]
            else:
                total_distance = sum(distances)
        except BaseException:
            total_distance = None

        interpreted_way = {
            'activity_type': activity_type,
            'positions': positions,
            'altitudes': altitudes,
            'distances': distances,
            'total_distance': total_distance,
        }

        return interpreted_way
