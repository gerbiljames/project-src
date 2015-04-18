from math import radians, sin, cos, sqrt, asin
from numpy import matlib
import matlab_wrapper


class HyperbolicEmbedder:

    def __init__(self):

        self.earth_radius = 6371

    def generate_ordered_asn_list(self, aut_sys_data):

        return [asn for asn in aut_sys_data]

    def generate_distance_matrix(self, aut_sys_data, asn_ordered_list):

        dim = (len(aut_sys_data), len(aut_sys_data))

        distance_matrix = matlib.zeros(dim)

        for index_outer, asn_outer in enumerate(asn_ordered_list):

            aut_sys_outer = aut_sys_data[asn_outer]

            for index_inner, asn_inner in enumerate(asn_ordered_list):

                aut_sys_inner = aut_sys_data[asn_inner]

                distance = self.haversine((aut_sys_outer.latitude, aut_sys_outer.longitude), (aut_sys_inner.latitude, aut_sys_inner.longitude))

                distance_matrix[index_outer, index_inner] = distance

                distance_matrix[index_inner, index_outer] = distance

        return distance_matrix

    def haversine(self, latlong0, latlong1):

        dlat = radians(latlong1[0] - latlong0[0])
        dlong = radians(latlong1[1] - latlong0[1])
        lat0 = radians(latlong0[0])
        lat1 = radians(latlong1[0])

        a = sin(dlat/2)**2 + cos(lat0)*cos(lat1)*sin(dlong/2)**2
        c = 2*asin(sqrt(a))

        return self.earth_radius * c

    def hyperbolic_embed(self, distance_matrix):

        matlab = matlab_wrapper.MatlabSession()

        matlab.put("D", distance_matrix)

        matlab.eval("[Z, r] = hyperbolic_embed(D)")

        kernel_matrix = matlab.get("Z")

        radius = matlab.get("r")

        return kernel_matrix, radius