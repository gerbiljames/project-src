from math import radians, sin, cos, asin
from numpy import matlib, ndenumerate, sqrt, absolute, where
from scipy import linalg
from mlabwrap import mlab

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

                distance -= 3 * (abs(len(aut_sys_outer.peers) - len(aut_sys_inner.peers)))

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

        kernel_matrix, radius = mlab.hyperbolic_embed(distance_matrix, nout=2)

        return kernel_matrix, radius

    def calculate_eigv(self, matrix):

        eigenvalues, eigenvectors = linalg.eigh(matrix)

        return eigenvalues, eigenvectors

    def calculate_embedding_inner_product_matrix(self, radius, eigenvectors, eigenvalues):

        return radius * eigenvectors * sqrt(absolute(eigenvalues))

    def find_hyperboloid_point_matrix(self, hyperbolic_matrix, eigenvalues):

        dimension_columns = self.find_dimension_columns(eigenvalues)

        return hyperbolic_matrix[:, dimension_columns]

    def find_dimension_columns(self, eigenvalues):

        sorted_eigenvalues = sorted(eigenvalues)

        neg0 = where(eigenvalues == sorted_eigenvalues[0])[0][0]

        pos0 = where(eigenvalues == sorted_eigenvalues[-1])[0][0]

        pos1 = where(eigenvalues == sorted_eigenvalues[-2])[0][0]

        pos2 = where(eigenvalues == sorted_eigenvalues[-3])[0][0]

        return neg0, pos0, pos1, pos2

    def convert_hyperboloid_to_ball(self, hyperboloid_matrix):

        ball_model_coords = []

        for coords in hyperboloid_matrix:

            x0 = coords[0]

            const = 1 / (x0 + 1)

            ball_model_coords.append(const * coords[1:])

        return ball_model_coords

    def convert_ball_to_klein(self, ball_matrix):

        klein_coords = []

        for coords in ball_matrix:

            klein_coords.append((2 * coords) / (1 + coords * coords))

        return klein_coords

    def convert_ball_to_upper_half(self, ball_matrix):

        upper_half_coords = []

        for coords in ball_matrix:

            new_coord = []

            norm_squared = linalg.norm(coords) ** 2

            for coord in coords[:-1]:

                new_coord.append((2 / (1 - (2 * coord) + norm_squared)) * coord)

            new_coord.append(((2 / (1 - 2 * coords[-1]) + norm_squared) * (1 - coords[-1])) + 1)

            upper_half_coords.append(new_coord)

        return upper_half_coords




