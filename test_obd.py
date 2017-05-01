def main():
	from obd import obd
	from time import strftime
	obd.logger.setLevel(obd.logging.DEBUG)
	car = obd.OBD()
	a = car.supported_commands
	print strftime("%m-%d-%Y %I:%m")
	print car.port_name()

	commands = {}

	# Convert to dictionary
	for c in a:
		data = str(c).split(": ")
		commands[data[0]] = data[1]
	print commands['025A']

if __name__=="__main__":
	main()
