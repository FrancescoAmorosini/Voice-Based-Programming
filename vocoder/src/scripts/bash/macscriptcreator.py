import sys
f = open("conda/audiorecorderConst.sh","w+")
f.write("osascript -e '")
f.write("tell application \"Terminal\"\n")
f.write("\t\tdo script \"\"\n")
f.write("\t\tdo script \"cd ")
f.write(sys.argv[1])
f.write("/conda \" in front window\n")
f.write("\t\tdo script \"./audioRecorderConstActivator.sh\" in front window \n")
f.write("\t\tdelay 20\n")
f.write("\t\tclose front window\n")
f.write("end tell'\n")


