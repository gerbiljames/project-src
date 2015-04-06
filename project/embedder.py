from math import sqrt
from numpy import matlib


class HyperbolicEmbedder:

    def __init__(self):

        pass

    def generate_ordered_asn_list(self, aut_sys_data):

        return [asn for asn in aut_sys_data]

    def generate_distance_matrix(self, aut_sys_data, asn_ordered_list):

        dim = (len(aut_sys_data), len(aut_sys_data))

        distance_matrix = matlib.zeros(dim)

        for index, asn in enumerate(asn_ordered_list):

            aut_sys_object = aut_sys_data[asn]

            if aut_sys_object.peers:

                for peering in aut_sys_object.peers:

                    peer_asn = peering.peer_asn

                    if peer_asn in asn_ordered_list:

                        peer_index = asn_ordered_list.index(peer_asn)

                        peer_aut_sys_object = aut_sys_data[peer_asn]

                        distance = self.calculate_euclidean_distance((aut_sys_object.latitude, aut_sys_object.longitude), (peer_aut_sys_object.latitude, peer_aut_sys_object.longitude))

                        distance_matrix[index, peer_index] = distance

                        distance_matrix[peer_index, index] = distance

        return distance_matrix

    def calculate_euclidean_distance(self, xy1, xy2):

        return sqrt(((xy2[0] - xy1[0]) ** 2) + ((xy2[1] - xy1[1]) ** 2))