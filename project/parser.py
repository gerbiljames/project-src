import re
from project import classes


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

        # TODO: parse location data

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

    def parse_location_data(self, aut_sys_data):
        pass
