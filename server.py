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

	Show Welcome
"""
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
		out = Query("select Name from devices;")
		
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

@app.route("/vin/")
@app.route("/vin/<vin>")
def decode_vin(vin, methods=['GET','POST']):
	if request.method == 'POST':
		return render_template("home/VIN.html",vin=vin)
	else:
		return render_template("home/VIN.html",vin=None)

def ms(seconds):
	return int(seconds)*1000

if __name__ == "__main__":
	db = connectDB()
	app.run(host="0.0.0.0",port=5000)
