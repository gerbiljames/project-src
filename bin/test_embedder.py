#!/usr/bin/env python

from project import parser, embedder

as_parser = parser.ASDataParser()

aut_sys_data = as_parser.retrieve_aut_sys_data()

aut_sys_data = as_parser.generate_graph_subset(aut_sys_data)

as_embedder = embedder.HyperbolicEmbedder()

asn_ordered_list = as_embedder.generate_ordered_asn_list(aut_sys_data)

distance_matrix = as_embedder.generate_distance_matrix(aut_sys_data, asn_ordered_list)

return_value = as_embedder.hyperbolic_embed(distance_matrix)

print(return_value[1])

print(return_value[0])
