import re
import subprocess
import csv
from project import classes


class ASDataParser:

    def __init__(self):
        self.data_path = "../data/"

        self.rel_pattern = re.compile(ur'^([0-9]*)\|([0-9]*)\|(-1|0)$')

        self.whob_executable = "/usr/local/bin/whob"
        self.network_flag = "-N"
        self.org_name_pattern = re.compile(ur'^Org-Name: (.*)$', re.MULTILINE)
        self.cache_file_name = ".as_name_cache"

        self.name_cache = self.load_cache()

    def retrieve_aut_sys_data(self, relations_file="20150301.as-rel.txt"):

        aut_sys = self.parse_relations_file(relations_file)

        aut_sys = self.parse_name_data(aut_sys)

        self.write_cache()

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

    def parse_name_data(self, aut_sys_data):

        for asn in aut_sys_data:

            org_name = self.get_as_org_name(asn)

            aut_sys_data[asn].org_name = org_name

        return aut_sys_data

    def parse_location_data(self, aut_sys_data):
        pass

    def get_as_org_name(self, asn):

        if asn in self.name_cache:

            return self.name_cache[asn]

        else:

            whob_output = self.run_whob(asn)

            m = re.search(self.org_name_pattern, whob_output)

            if m:
                self.name_cache[asn] = m.group(1)
                return m.group(1)
            else:
                return "Unknown"

    def load_cache(self):

        with open(self.data_path + self.cache_file_name) as cache_file:
            reader = csv.reader(cache_file)

            cache_dict = {row[0]: row[1] for row in reader}

            return cache_dict

    def write_cache(self):
        if self.name_cache:
            with open(self.data_path + self.cache_file_name, 'w') as cache_file:
                writer = csv.writer(cache_file)

                for key, value in self.name_cache.items():

                    writer.writerow([key, value])

    def run_whob(self, asn):
        print "Running whob for: AS" + asn
        return subprocess.check_output([self.whob_executable, self.network_flag, asn])
