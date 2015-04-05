#!/usr/bin/env python

from project import parser

as_parser = parser.ASDataParser()

aut_systems = as_parser.retrieve_aut_sys_data()

total = 0
for asn in aut_systems:
    if aut_systems[asn].ip is None:
        print ("OH NO:" + asn)
        total += 1

print total
print len(aut_systems)