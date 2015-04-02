import re
import subprocess
import csv
from project import classes


class ASDataParser:

    def __init__(self):
        self.data_path = "../data/"

        self.rel_pattern = re.compile(ur'^([0-9]*)\|([0-9]*)\|(-1|0)$')

        self.name_pattern = re.compile(ur'([0-9]+)\s(.*)')

    def retrieve_aut_sys_data(self, relations_file="20150301.as-rel.txt", name_file="20150402.as-name.txt"):

        aut_sys = self.parse_relations_file(relations_file)

        aut_sys = self.parse_name_file(aut_sys, name_file)

        # TODO: parse location data

        return aut_sys

    def parse_relations_file(self, filename):

        aut_systems = dict()

        with open(self.data_path + filename) as data:
            for line in data:
                m = re.search(self.rel_pattern, line)
                if m:
                    asn = m.group(1)
                    peer_asn = m.group(2)
                    rel_type = m.group(3)

                    if asn in aut_systems:
                        aut_systems.get(asn).add_peering(classes.Peering(peer_asn, rel_type))
                    else:
                        new_aut_sys = classes.AutonomousSystem(asn, "", 0, 0)
                        new_aut_sys.add_peering(classes.Peering(peer_asn, rel_type))
                        aut_systems[asn] = new_aut_sys

        return aut_systems

    def parse_name_file(self, aut_sys_data, name_file):

        with open(self.data_path + name_file) as data:
            for line in data:
                m = re.search(self.name_pattern, line)
                if m:
                    asn = m.group(1)
                    org_name = m.group(2)

                    if asn in aut_sys_data:
                        aut_sys_data[asn].org_name = org_name

        return aut_sys_data

    def parse_location_data(self, aut_sys_data):
        pass
