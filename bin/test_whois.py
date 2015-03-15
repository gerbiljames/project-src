import project

as_loader = project.loader.ASDataLoader()

data = as_loader.querywhois("AS6730")

aut_sys = project.classes.AutonomousSystem.from_whois_data(data)

print aut_sys

