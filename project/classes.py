import re


class AutonomousSystem:

    NAME_STR = "as-name:"
    ID_STR = "aut-num:"
    IMPORT_STR = "import:"
    EXPORT_STR = "export:"
    AS_PATTERN = "AS[0-9]*"
    DATA_SEPARATOR = ":"

    def __init__(self, number, name, latitude, longitude):

        self.number = number
        self.name = name
        self.neighbours = []
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        str_list = [self.number, self.name, self.latitude, self.longitude]

        for neighbour in self.neighbours:
            str_list.append(neighbour)

        return ",".join(str_list)

    def add_neighbour(self, neighbour_id):
        self.neighbours.append(neighbour_id)

    def add_neighbours(self, neighbour_list):
        self.neighbours.extend(neighbour_list)

    @classmethod
    def from_whois_data(cls, whois_data):

        aut_id = ""
        name = ""
        latitude = "0"
        longitude = "0"
        neighbours = set()

        whois_list = whois_data.splitlines()

        for line in whois_list:

            if line.startswith(AutonomousSystem.IMPORT_STR) or line.startswith(AutonomousSystem.EXPORT_STR):
                search = re.search(AutonomousSystem.AS_PATTERN, line)
                found_id = search.group()

                neighbours.add(found_id)

            elif line.startswith(AutonomousSystem.ID_STR):
                search = re.search(AutonomousSystem.AS_PATTERN, line)
                aut_id = search.group()

            elif line.startswith(AutonomousSystem.NAME_STR):
                name = line.split(AutonomousSystem.DATA_SEPARATOR, 1)[1].strip()

        new_as = cls(aut_id, name, latitude, longitude)

        new_as.add_neighbours(neighbours)

        return new_as