
class AutonomousSystem:

    def __init__(self, asn, name, latitude, longitude):

        self.asn = asn
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.peers = []

    def __str__(self):
        str_list = [self.asn, self.name, self.latitude, self.longitude]

        for peer in self.peers:
            str_list.append(peer.peer_asn)

        return ",".join(str_list)

    def add_peering(self, peering):

        self.peers.append(peering)


class Peering:

    def __init__(self, peer_asn, rel_type):

        self.peer_asn = peer_asn
        self.rel_type = rel_type

