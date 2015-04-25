#!/usr/bin/env python

from project import parser, embedder, visualiser

print "Parsing AS Data..."

as_parser = parser.ASDataParser()

aut_sys_data = as_parser.retrieve_aut_sys_data()

aut_sys_data = as_parser.generate_graph_subset(aut_sys_data, depth=3, current_system_asn="1")

print "Embedding " + str(len(aut_sys_data)) + " ASes..."

as_embedder = embedder.HyperbolicEmbedder()

asn_ordered_list = as_embedder.generate_ordered_asn_list(aut_sys_data)

distance_matrix = as_embedder.generate_distance_matrix(aut_sys_data, asn_ordered_list)

hyperbolic_distances, radius = as_embedder.hyperbolic_embed(distance_matrix)

eigenvalues, eigenvectors = as_embedder.calculate_eigv(hyperbolic_distances)

inner_product_matrix = as_embedder.calculate_embedding_inner_product_matrix(radius, eigenvectors, eigenvalues)

hyperboloid_points = as_embedder.find_hyperboloid_point_matrix(inner_product_matrix, eigenvalues)

ball_matrix = as_embedder.convert_to_ball_model(hyperboloid_points)

print "Visualising Data..."

euclid_visualiser = visualiser.EuclideanVisualiser()

euclid_visualiser.visualise(ball_matrix, asn_ordered_list, aut_sys_data)