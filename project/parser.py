import re
from project import classes


class ASDataParser:

    def __init__(self):
        self.data_path = "../data/"
        self.rel_pattern = re.compile(ur'^([0-9]*)\|([0-9]*)\|(-1|0)$')

    def retrieve_aut_sys_data(self, relations_file="20150301.as-rel.txt"):

        aut_sys = self.parse_relations_file(relations_file)

        # TODO: parse name data

        # TODO: parse location data

        return aut_sys

    def parse_relations_file(self, filename):

        aut_systems = dict()

        with open(self.data_path + filename) as data:
            for line in data:
                m = re.match(self.rel_pattern, line)
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

        data.close()
        return aut_systems

    def parse_name_data(self, aut_sys_data):
        pass

    def parse_location_data(self, aut_sys_data):
        pass