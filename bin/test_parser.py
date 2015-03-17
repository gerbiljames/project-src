from project import parser

as_parser = parser.ASDataParser()

aut_systems = as_parser.parse_file("20150301.as-rel.txt")

aut_systems
