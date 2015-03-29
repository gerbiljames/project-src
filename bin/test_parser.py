#!/usr/bin/env python

from project import parser

as_parser = parser.ASDataParser()

aut_systems = as_parser.retrieve_aut_sys_data("20150301.as-rel.txt")

aut_systems
