def main():
	from obd import obd
	from time import strftime
	from sys import exit

	obd.logger.setLevel(obd.logging.DEBUG)
	car = obd.OBD()

	while(car.is_connected()):
		r = car.query(obd.commands.FUEL_LEVEL)
		addPercentage(strftime("%Y-%m-%d %I:%m:%S"), "Fuel Level", float(r.value))
		
		r = car.query(obd.commands.ABSOLUTE_LOAD)
		addPercentage(strftime("%Y-%m-%d %I:%m:%S"), "Absolute Load", float(r.value))
		
		r = car.query(obd.commands.SPEED)
		addSpeed(strftime("%Y-%m-%d %I:%m:%S"), "Vehicle Speed", str(r.value.to('mph')) )

		r = car.query(obd.commands.AMBIANT_AIR_TEMP)
		addTemperature(strftime("%Y-%m-%d %I:%m:%S"), "Ambiant Air Temp", str(r.value.magnitude) )
		
		r = car.query(obd.commands.INTAKE_TEMP)
		addTemperature(strftime("%Y-%m-%d %I:%m:%S"), "Intake Air Temp", str(r.value.magnitude) )

def Action(s):
	global connection
	cursor = connection.cursor()
	
	if connection.cursor().execute(s):
		connection.commit()
		return True
	else:
		return False

def addPercentage(dt, description, value):
	sql = "INSERT INTO percentages (Time, Description, Value) VALUES ('%s','%s','%s');" % (dt, description, value)
	if Action(sql):
		print "('%s','%s','%s') --> Inserted" % (dt, description, value)

def addSpeed(dt, description, value):
	sql = "INSERT INTO speeds (Time, Description, Value) VALUES ('%s','%s','%s');" % (dt, description, value)
	if Action(sql):
		print "('%s','%s','%s') --> Inserted" % (dt, description, value)

def addTemperature(dt, description, value):
	sql = "INSERT INTO temperatures (Time, Description, Value) VALUES ('%s','%s','%s');" % (dt, description, value)
	if Action(sql):
		print "('%s','%s','%s') --> Inserted" % (dt, description, value)

def connectDB():
	host = "localhost"
	user = "root"
	pswd = "root"
	db   = "garagepi"

	import MySQLdb
	global connection
	connection = MySQLdb.connect( host=host, user=user, passwd=pswd, db=db )

if __name__=="__main__":
	connectDB()
	main()
