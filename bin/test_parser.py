#!/usr/bin/env python

from project import parser

as_parser = parser.ASDataParser()

aut_systems = as_parser.retrieve_aut_sys_data()

total = 0
for asn in aut_systems:
    for attr, value in vars(aut_systems[asn]).items():
        if not value and not attr == "peers":
            total += 1
            break

print str(total) + " objects have incomplete data out of " + str(len(aut_systems))


