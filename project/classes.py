
class AutonomousSystem:

    def __init__(self, asn, code):

        self.asn = asn
        self.org_code = code
        self.org_name = None
        self.ip = None
        self.latitude = None
        self.longitude = None
        self.peers = []

    def add_peering(self, peering):

        self.peers.append(peering)

    def add_peerings(self, peerings):
        for peering in peerings:

            self.add_peering(peering)


class Peering:

    def __init__(self, peer_asn, rel_type):

        self.peer_asn = peer_asn
        self.rel_type = rel_type