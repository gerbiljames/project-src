#!/usr/bin/env python

from project import parser, embedder
import numpy

as_parser = parser.ASDataParser()

aut_sys_data = as_parser.retrieve_aut_sys_data()

aut_sys_data = as_parser.generate_graph_subset(aut_sys_data)

as_embedder = embedder.HyperbolicEmbedder()

asn_ordered_list = as_embedder.generate_ordered_asn_list(aut_sys_data)

distance_matrix = as_embedder.generate_distance_matrix(aut_sys_data, asn_ordered_list)

non_zero_elements = 0
elements = 0

for element in numpy.nditer(distance_matrix):
    elements += 1
    if element:
        non_zero_elements += 1

print "There are " + str(non_zero_elements) + " non-zero elements of " + str(elements) + " total in the distance matrix."
