import sys
f = open("conda/audiorecorderConst.sh","w+")
f.write("osascript -e '")
f.write("tell application \"Terminal\"\n")
f.write("\t\tdo script \"\"\n")
f.write("\t\tdo script \"cd ")
f.write(sys.argv[1])
f.write("/conda\" in front window\n")
f.write("\t\tdo script \"./audioRecorderConstActivator.sh\" in front window \n")
f.write("\t\tdelay 13\n")
f.write("\t\tclose front window\n")
f.write("end tell'\n")
f.close()

v = open("venv/audiorecorderConst.sh","w+")
v.write("osascript -e '")
v.write("tell application \"Terminal\"\n")
v.write("\t\tdo script \"\"\n")
v.write("\t\tdo script \"cd ")
v.write(sys.argv[1])
v.write("/venv\" in front window\n")
v.write("\t\tdo script \"./audioRecorderConstActivator.sh\" in front window \n")
v.write("\t\tdelay 13\n")
v.write("\t\tclose front window\n")
v.write("end tell'\n")
v.close()
