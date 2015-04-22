from math import radians, sin, cos, asin
from numpy import matlib, ndenumerate, diag, sqrt, absolute, where
from scipy import linalg
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

    def normalise_distance_matrix(self, distance_matrix):

        total_distance = 0

        for distance in distance_matrix.flat:

            total_distance += distance

        mean_distance = total_distance / distance_matrix.size

        for (x, y), distance in ndenumerate(distance_matrix):

            distance_matrix[x, y] = distance / mean_distance

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

        matlab.eval("[Z, r] = hyperbolic_embed(D);")

        kernel_matrix = matlab.get("Z")

        radius = matlab.get("r")

        return kernel_matrix, radius

    def calculate_eigv(self, matrix):

        eigenvalues, eigenvectors = linalg.eigh(matrix)

        return eigenvalues, eigenvectors

    def calculate_embedding_matrix(self, radius, eigenvectors, eigenvalues):

        return radius * eigenvectors * sqrt(absolute(eigenvalues))

    def find_hyperbolic_point_matrix(self, hyperbolic_matrix, eigenvalues):

        dimension_columns = self.find_dimension_columns(eigenvalues)

        return hyperbolic_matrix[:, dimension_columns]

    def find_dimension_columns(self, eigenvalues):

        sorted_eigenvalues = sorted(eigenvalues)

        neg0 = where(eigenvalues == sorted_eigenvalues[0])[0][0]

        pos0 = where(eigenvalues == sorted_eigenvalues[-1])[0][0]

        pos1 = where(eigenvalues == sorted_eigenvalues[-2])[0][0]

        pos2 = where(eigenvalues == sorted_eigenvalues[-3])[0][0]

        return pos0, pos1, pos2, neg0
