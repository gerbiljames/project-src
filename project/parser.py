import re
from project import classes
import pyasn
import random
from geoip import geolite2


class ASDataParser:

    def __init__(self):
        self.data_path = "../data/"

        self.orgcode_pattern = re.compile(ur'^([0-9]+)\|([0-9]*)\|(.*)\|(.+)\|(.+)$')

        self.orgname_pattern = re.compile(ur'^(.+)\|([0-9]*)\|(.*)\|([A-Z]*)\|(.+)$')

        self.rel_pattern = re.compile(ur'^([0-9]+)\|([0-9]+)\|(-1|0)$')

    def retrieve_aut_sys_data(self):

        aut_sys_list = self.parse_org_code_file()

        aut_sys_list = self.parse_org_name_file(aut_sys_list)

        aut_sys_list = self.parse_relations_file(aut_sys_list)

        aut_sys_list = self.parse_ip_data(aut_sys_list)

        aut_sys_list = self.parse_location_data(aut_sys_list)

        return aut_sys_list

    def parse_org_code_file(self, orgcode_file="20150101.as-orgcodes.txt"):

        aut_sys_list = dict()

        with open(self.data_path + orgcode_file) as data:
            for line in data:
                m = re.search(self.orgcode_pattern, line)
                if m:
                    asn = m.group(1)
                    org_code = m.group(4)

                    aut_sys = classes.AutonomousSystem(asn, org_code)
                    aut_sys_list[asn] = aut_sys

        return aut_sys_list

    def parse_org_name_file(self, aut_sys_list, org_name_file="20150101.as-orgnames.txt"):

        org_name_list = dict()

        with open(self.data_path + org_name_file) as data:
            for line in data:
                m = re.search(self.orgname_pattern, line)
                if m:
                    org_code = m.group(1)
                    org_name = m.group(3)
                    org_name_list[org_code] = org_name

        for asn in aut_sys_list:
            org_code = aut_sys_list[asn].org_code

            if org_code in org_name_list:
                aut_sys_list[asn].org_name = org_name_list[org_code]

        return aut_sys_list

    def parse_relations_file(self, aut_sys_list, rel_file="20150301.as-rel.txt"):

        with open(self.data_path + rel_file) as data:
            for line in data:
                m = re.search(self.rel_pattern, line)
                if m:
                    asn = m.group(1)
                    peer_asn = m.group(2)
                    rel_type = m.group(3)

                    if asn in aut_sys_list:
                        aut_sys_list.get(asn).add_peering(classes.Peering(peer_asn, rel_type))

        return aut_sys_list

    def parse_ip_data(self, aut_sys_data, ipasn_file="20150405.ipasn.db"):

        asndb = pyasn.pyasn(self.data_path + ipasn_file)

        for asn in aut_sys_data:

            prefixes = asndb.get_as_prefixes(asn)

            if prefixes:

                prefix = random.sample(prefixes, 1)[0]

                ip = prefix.split("/")[0]

                aut_sys_data[asn].ip = ip

        return aut_sys_data

    def parse_location_data(self, aut_sys_data):

        for asn in aut_sys_data:

            if aut_sys_data[asn].ip:

                match = geolite2.lookup(aut_sys_data[asn].ip)

                if match:

                    if match.location:
                        loc = match.location

                        aut_sys_data[asn].latitude = loc[0]

                        aut_sys_data[asn].longitude = loc[1]

        return aut_sys_data
