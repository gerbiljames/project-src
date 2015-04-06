#!/usr/bin/env python

from project import parser

as_parser = parser.ASDataParser()

aut_systems = as_parser.retrieve_aut_sys_data()

print len(aut_systems)


