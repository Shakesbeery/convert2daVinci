import sys,os,base64
sys.version
'''
Based on code by: Mason Sheffield 12/29/2014

This will take a slic3r gcode file and convert it to work with the XYZ DaVinci 3d printer.

example:
	$python gcode_to_davinci.py -f ./my_file.gcode -c True -a True
'''
def main(my_file, cura_mode=False):
	print(my_file)
	#delete this text line and all text above it
	topLine = "; --- MOVE THIS SECTION TO THE TOP AND DELETE THIS LINE ---\n"
	#read original file
	with open(my_file, 'r') as f:
	    my_lines = f.readlines()
	#start writing to new list after finding line matching 'topLine' 
	trimmed_gcode = list()
	cura_header = [];
	start_line = False
	for x in my_lines:
		#Must replace all G0 instructions with G1 for DaVinci Printer
		if cura_mode and x[:3] == 'G0 ':
			x = 'G1 ' + x[3:]
		if start_line and x != '\n':
			trimmed_gcode.append(x)
		if x == top_line:
			start_line = True
		#Save the CURA header	
		if cura_mode:
			if not start_line and x != '\n':
				cura_header.append(x)
			#Move cura header under the DaVinci header
			if ';TEMPERATURES\n' == x:
				trimmed_gcode += cura_header
			
	#creat new filename with .3w extension  
	new_file =  my_file[:-5] + '3w'
	#newDebugFile = myFile[:-6] + '_debug.gcode'
	#df = open(newDebugFile,'w+')
	#df.writelines(trimmedGcode)
	#df.close()
	
	with open(new_file,'w+') as outf:
	    #encode the modified gcode file with base64 encoding
	    new_gcode_str = ''.join(trimmed_gcode)
	    base64_gcode = base64.standard_b64encode(new_gcode_str)
	    outf.writelines(base64_gcode)

	print 'Encoded Stuff \n\n'	
	print 'Success!'


if __name__ == "__main__":
	main(sys.argv[1],sys.argv[2])
	
