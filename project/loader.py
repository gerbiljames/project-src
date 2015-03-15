from subprocess import check_output


class ASDataLoader:

    def __init__(self):
        self.whois = "/usr/bin/whois"
        self.host = "whois.radb.net"

    def querywhois(self, as_number):

        command = [self.whois, "-h", self.host, as_number]

        return check_output(command)




