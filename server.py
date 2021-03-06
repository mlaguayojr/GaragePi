"""
	Mario Luis Aguayo Jr.
	CSC 400

	Python 2.7

	RUN AS SUDO
"""

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

"""
	Connect to garagepi database
"""
def connectDB():
	host = "localhost"
	user = "root"
	pswd = "root"
	db   = "garagepi"

	import MySQLdb
	connection = MySQLdb.connect( host=host, user=user, passwd=pswd, db=db )
	
	if(connection):
		return connection
	else:
		return None

"""
	Do SQL Query

	return stuff
"""
def Query(s):
	global db
	cursor = db.cursor()
	cursor.execute(s)
	return cursor.fetchall()

"""
	Perform a SQL action (different from a query)
"""
def Action(s):
	global db
	cursor = db.cursor()
	
	if db.cursor().execute(s):
		db.commit()
		return True
	else:
		return False

"""
	Index Page

	Show Welcome """
@app.route("/")
def index(): return render_template("index.html")

"""
	Home Page
"""
@app.route("/home/")
def home(): return render_template("home/home.html")

"""
	About Page

	Show Information on:
		* System
		* Network
		* Bluetooth Info
"""
@app.route("/about/")
def about(): return render_template("about/about.html")

@app.route("/about/system/")
def about_system():
	from platform import uname
	return render_template("about/system.html",info=uname())

@app.route("/about/project/")
def about_project(): return render_template("about/project.html")

@app.route("/about/bluetooth/")
def about_bluetooth():
	# Get MAC
	from subprocess import Popen, PIPE

	p = Popen("hcitool dev", shell=True, stdout=PIPE)
	out, err = p.communicate()
	out = out.decode("utf-8")
	out = str(out).split("\n")[1:-1]
	for i in range(0,len(out)):
		out[i] = out[i].strip("\t").split("\t")[1]
	
	if len(out) == 0:
		out = None

	return render_template("about/bluetooth.html",info=out)


@app.route("/about/network/")
def about_network():

	from subprocess import Popen, PIPE

	# Get Devices
	p = Popen("ifconfig | grep 'Link encap:Ethernet' | awk '{print $1}'", shell=True, stdout=PIPE)
	out, err = p.communicate()
	out = out.decode("utf-8")
	out = str(out).split("\n")[:-1]

	l = []
	# Get Device Info
	for i in out:
		data = [i]

		# Get MAC
		p = Popen("ifconfig "+i+" | grep 'HWaddr' | awk '{print $5}'", shell=True, stdout=PIPE)
		out, err = p.communicate()
		out = out.decode("utf-8")
		data.append(out)

		# Get IPv4
		p = Popen("ifconfig "+i+" | grep 'inet addr' | awk '{print $2}'", shell=True, stdout=PIPE)
		out, err = p.communicate()
		out = out.decode("utf-8").strip()

		if len(out) != 0:
			data.append(out.strip("addr:"))

			# Get Broadcast
			p = Popen("ifconfig "+i+" | grep 'inet addr' | awk '{print $3}'", shell=True, stdout=PIPE)
			out, err = p.communicate()
			out = out.decode("utf-8")
			data.append(out.strip("Bcast:"))

			# Get Netmask
			p = Popen("ifconfig "+i+" | grep 'inet addr' | awk '{print $4}'", shell=True, stdout=PIPE)
			out, err = p.communicate()
			out = out.decode("utf-8")
			data.append(out.strip("Mask:"))

		else:
			data.append("< not in use >") #IPV4
			data.append(" ---- ") # bcast
			data.append(" ---- ") # netmask

		l.append(data)

		# Get Hostname
		p = Popen("hostname", shell=True, stdout=PIPE)
		out, err = p.communicate()
		out = str(out.decode("utf-8")).strip()

	return render_template("about/network.html",info=l,local=out)


"""
	Show Saved Devices from the garagepi.devices table.
"""
@app.route("/devices/")
def devices():
	global db

	if db != None:
		out = Query("select Name, Description from devices;")
		
		if len(out) == 0:
			out = None

		return render_template("devices/devices.html",out=out)
	else:
		db = connectDB()
		return redirect("/devices/")

"""
	Display the Device Information

	Grab the data from DB
"""
@app.route("/device/<device_name>")
def device_info(device_name):
	global db

	if "%20" in device_name:
		device_name = str(device_name).replace("%20"," ")

	if db != None:

		# Check if the name is valid
		out = Query("select count(Name) from devices where Name=\"%s\";" % device_name)[0][0]

		if str(out) == "1":

			data = Query("select * from devices where Name=\"%s\";" % device_name)[0]
			return render_template("devices/info.html",info=data)

		else:
			return "Invalid"


@app.route("/devices/<device_name>/edit/", methods=['POST'])
def device_update(device_name):
	global db

	if "%20" in device_name:
		device_name = device_name.replace("%20"," ")


	out = Query("select count(Name) from devices where Name=\"%s\";" % device_name)[0][0]

	if db != None and str(out) == "1":

		new_name = request.form['_name']
		new_mac  = request.form['_mac']
		new_desc = request.form['_desc']
		new_pin  = request.form['_pin']

		from time import strftime
		new_edit = str(strftime("%Y-%m-%d %H:%M:%S"))

		sql = "update devices set Name='{0}', MAC='{1}', Description='{2}', Edited='{3}', PIN='{4}' WHERE Name='{5}';".format(new_name, new_mac, new_desc, new_edit, new_pin, device_name)
		Action(sql)
		return redirect("/devices/",code=302)
	else:
		redirect("/devices/",code=302)

@app.route("/devices/<device_name>/edit/", methods=['GET'])
def device_actions(device_name):
	global db

	if "%20" in device_name:
		device_name = device_name.replace("%20"," ")


	out = Query("select count(Name) from devices where Name=\"%s\";" % device_name)[0][0]
	
	if db != None and str(out) == "1":

		data = Query("select Name, MAC, Description, PIN from devices where Name=\"%s\";" % device_name)[0]
		return render_template("devices/edit.html", info=data)

	else:
		return redirect("/devices/",code=302)

@app.route("/devices/<device_name>/delete/", methods=['GET'])
def device_delete(device_name):
	global db

	sql = "select count(Name) from devices where Name=\"{0}\";".format(device_name.replace("%20"," "))

	out = Query(sql)[0][0]
	
	if db != None and str(out) == "1":

		sql = "delete from devices where Name='{0}';".format(device_name)

		if(Action(sql)):
			return redirect("/devices/",code=302)
		else:
			return "sql error"

	else:
		return redirect("/devices/",code=302)

"""
	User add Car Adapter
	* Nearby
	* Manually
"""
@app.route("/devices/add/", methods=['GET'])
def device_add(action=None):

	from os import system
	from time import sleep

	system("hciconfig hci0 reset")

	# TOOK FOREVER
	# RES: https://stackoverflow.com/questions/26874829/hcitool-lescan-will-not-print-in-real-time-to-a-file
	system("hcitool -i hci0 scan > scan.txt && pkill --signal SIGINT hcitool")

	d = open("scan.txt",'r').read().split("\n")[1:-1]
	global devices
	devices = {}

	if len(d) == 0:
		devices = None

	else:
		for i in d:
			data = i.split("\t")[1:]

			try:
				data[1:] = " ".join(data[1:]).strip("/").split()
			except Exception:
				pass

			if data[0] not in devices:
				devices[data[0]] = " ".join(data[1:])
			else:
				if data[1] != "(unknown)":
					devices[data[0]] = " ".join(data[1:])

	# THIS DOES NOT WORK -- I CAN TELL YOU WHY
	# out, err = Popen("sudo hciconfig hci0 reset", shell=True, stdout=PIPE).communicate()
	# print "Reseting Bluetooth Device: {0}".format(out)

	# if err != None:
	# 	out, err = Popen("sudo service bluetooth restart", shell=True, stdout=PIPE).communicate()
	# 	print "Restart Bluetooth Service: {0}".format(out)

	# 	from time import sleep
	# 	print "Waiting 1 second"
	# 	sleep(1)

	# 	out, err = Popen("sudo hciconfig hci0 reset", shell=True, stdout=PIPE).communicate()
	# 	print "Reseting Bluetooth Device: {0}".format(out)

	return render_template("devices/add.html",devices=devices)

@app.route("/devices/add/<mac>",methods=["GET","POST"])
def device_add_scan(mac):
	try:
		global devices
		out = [mac, devices[mac]]

		if request.method == "GET":
			return render_template("devices/add_scan.html",info=out)
		
		elif request.method == "POST":

			_name = request.form['_name']
			_mac  = request.form['_mac']
			_desc = request.form['_desc']
			_pin  = request.form['_pin']

			if _mac != mac:
				return redirect("/devices/",code=302)

			from time import strftime
			_created = str(strftime("%Y-%m-%d %H:%M:%S"))

			sql = "select count(MAC) from devices where MAC=\"{0}\";".format(_mac)

			if(Query(sql)[0][0] == 0):
				print "checked for similar device"

				sql = "insert into devices(Name, MAC, Description, Created, Edited, PIN) VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{3}\", \"{4}\");".format(_name, _mac, _desc, _created, _pin)

				if(Action(sql)):
					return redirect("/devices",code=302)
				else:
					return "INSERT ERROR"

			else:
				return render_template("error/dev_exist.html",timeout=ms(5), msg="This device is already saved! Returning to Devices in 5 seconds ...",redirect="/devices/")
		else:
			return page_not_found(404)

	except:
		return redirect("/devices/",code=302)

@app.errorhandler(404)
def page_not_found(error):
	return render_template("error/404.html",timeout=ms(3), msg="Does not exist! Going Home in 3 seconds...",redirect="/home/")

def ms(seconds):
	return int(seconds)*1000

@app.route("/vin/")
def get_vin():
	return render_template("home/VIN.html",vin=None)

@app.route("/vin/info/",methods=["POST"])
def decode_vin():
	if request.method != "POST":
		return redirect("/home/")

	_vin = request.form['vin'].split()

	if len(_vin) != 17:
		return redirect("/vin/")

	_built	= str(_vin[0])
	_manuf	= str(_vin[1:3])
	_brand	= str(_vin[3:8])
	_code 	= str(_vin[8])
	_year	= str(_vin[9])
	_plant	= str(_vin[10])
	_serial = str(_vin[11:])


	valid_models = {
		'A': ["1980","2010"],
		'B': ["1981","2011"],
		'C': ["1982","2012"],
		'D': ["1983","2013"],
		'E': ["1984","2014"],
		'F': ["1985","2015"],
		'G': ["1986","2016"],
		"H": ["1987","2017"],
		"J": ["1988"],
		"K": ["1989"],
		"L": ["1990"],
		"M": ["1991"],
		"N": ["1992"],
		"P": ["1993"],
		"R": ["1994"],
		"S": ["1995"],
		"T": ["1996"],
		"V": ["1997"],
		"W": ["1998"],
		"X": ["1999"],
		"Y": ["2000"],
		"1": ["2001"],
		"2": ["2002"],
		"3": ["2003"],
		"4": ["2004"],
		"5": ["2005"],
		"6": ["2006"],
		"7": ["2007"],
		"8": ["2008"],
		"9": ["2009"]
	}

	valid_countries = {
		'1': "United States",
		'4': "United States",
		'5': "United States",
		'2': "Canada",
		"3A": 'Mexico',
		"37": 'Mexico',
		"J": 'Japan',
		'VF': 'France',
		"VR": 'France',
		"9": "Brazil",
		"WA": 'West Germany',
		"W0": 'West Germany',
		"S": "Great Britain"
	}


	return render_template("home/VIN.html",vin=_vin)

@app.route("/reports/view/")
def show_reports():
	from os import listdir
	return render_template("report/view.html",reports=listdir("saved_reports"))

@app.route("/reports/idle/")
def new_idle_report():
	devices = Query("select Name from devices;")[0]
	return render_template("report/idle.html",devices=devices)

@app.route("/reports/idle/<device>/")
def get_obd_data(device):
	return "Pulling data from {0}".format(device)

@app.route("/reports/view/<file>")
def load_report(file):
	from os.path import exists
	
	if exists("saved_reports/"+file):
		
		data = open("saved_reports/"+file).read().strip()

		if not isinstance(eval(data),dict):
			return render_template("error/report_bad.html",timeout=ms(5), msg="{0} is corrupt. Returning to home".format(file),redirect="/home/")
		else:
			return redirect("saved_reports/"+file)

	else:
		return render_template("error/report_bad.html",timeout=ms(5), msg="{0} is corrupt. Returning to home".format(file),redirect="/home/")

@app.route("/reports/")
def report_page():	return render_template("report/main.html")


"""
	After selecting a device that is connected.
	The program queries and collects the data to a live view.
	The user then has the following options:
		- save report
		- refresh
"""
@app.route("/reports/new/<mac>/")
def report_new(mac, methods=['GET']):

	dev_name = Query("select Name from devices where MAC=\"{0}\";".format(mac))
	if len(dev_name) == 1:
		dev_name = dev_name[0][0]
		url = "/reports/new/%s/" % mac

		from time import strftime
		start = strftime("%m-%d-%Y %H:%m")

		from obd import obd
		obd.logger.setLevel(obd.logging.DEBUG)
		car = obd.OBD()
		results = []

		if car.is_connected():

			for i in car.supported_commands:
				results.append([ str(i), car.query(i).value ])

			car.close()
		else:
			results = None

		return render_template("report/new.html",device=dev_name, mac=mac, time=start, data=results, url=url)
	else:
		return redirect("devices/")

"""
	View all saved reports
"""
@app.route("/reports/view/")
def report_view():
	from os import listdir

	reports = listdir("saved_reports")
	return render_template("report/list.html", reports=reports)

"""
	View all collected data

	limited to what is present in the db
"""
@app.route("/data/")
def data_show():
	global db

	# Get tables
	sql = "SHOW TABLES;"
	tables = Query(sql)
	valid = []
	for i in tables:
		valid.append(i[0])

	valid.remove("devices")
	return render_template("data/list.html",tables=valid)

@app.route("/data/<tbl>/")
def data_show_table(tbl):
	tables = Query("SHOW TABLES;")
	valid = []

	for i in tables:
		valid.append(i[0])

	valid.remove("devices")

	if tbl not in valid:
		return redirect("/home/")
	else:
		return redirect("/data/%s/show/" % tbl)

@app.route("/data/<tbl>/show/")
def show_table_data(tbl):
	sql = "Select distinct Description from %s;" % tbl
	data = Query(sql)
	options = []

	for i in data:
		options.append(i[0])

	return render_template("/data/options.html",table=tbl, data=options)

@app.route("/data/<tbl>/show/options/<feature>/")
def show_table_data_values(tbl, feature):

	if "%20" in feature:
		feature = feature.replace("%20"," ")

	sql = "Select Time, Value from %s where Description = '%s' order by Time;" % (tbl, feature)
	v = Query(sql)
	data = []
	i = 1
	for j in v:
		data.append([i, j[1]])
		i+=1
		
	return render_template("/data/graph.html",data=data,feature=feature)

if __name__ == "__main__":
	global db
	db = connectDB()
	app.run(host="0.0.0.0",port=5000)
