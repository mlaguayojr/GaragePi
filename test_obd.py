def main():
	from obd import obd
	from time import strftime
	obd.logger.setLevel(obd.logging.DEBUG)
	car = obd.OBD()
	a = car.supported_commands
	print strftime("%m-%d-%Y %I:%m")
	print car.port_name()

	for i in a:
		print car.query(i)



if __name__=="__main__":
	main()
