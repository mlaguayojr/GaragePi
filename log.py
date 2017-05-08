lines = open("Text.txt").readlines()[18:]

for i in range(len(lines)):
	lines[i] = lines[i].strip("\n")

codes = []
for i in range(0,len(lines),2):
	print lines[i]
	print lines[i+1]

	if lines[i+1] != "None":
		codes.append([lines[i].replace("obd.obd] Sending command: ",""),lines[i+1]])

for i in codes:
	print i
	print ""