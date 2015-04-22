#!/usr/bin/env python

from project import parser, embedder

as_parser = parser.ASDataParser()

aut_sys_data = as_parser.retrieve_aut_sys_data()

aut_sys_data = as_parser.generate_graph_subset(aut_sys_data)

as_embedder = embedder.HyperbolicEmbedder()

asn_ordered_list = as_embedder.generate_ordered_asn_list(aut_sys_data)

distance_matrix = as_embedder.generate_distance_matrix(aut_sys_data, asn_ordered_list)

hyperbolic_distances, radius = as_embedder.hyperbolic_embed(distance_matrix)

eigenvalues, eigenvectors = as_embedder.calculate_eigv(hyperbolic_distances)

hyperbolic_matrix = as_embedder.calculate_embedding_matrix(radius, eigenvectors, eigenvalues)

hyperbolic_points = as_embedder.find_hyperbolic_point_matrix(hyperbolic_matrix, eigenvalues)

