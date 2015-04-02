#!/usr/bin/env python

from project import parser

as_parser = parser.ASDataParser()

aut_systems = as_parser.retrieve_aut_sys_data("20150301.as-rel.txt")

total = 0
for asn in aut_systems:
    if aut_systems[asn].org_name == "":
        print ("OH NO:" + asn)
        total += 1

print total
print len(aut_systems)