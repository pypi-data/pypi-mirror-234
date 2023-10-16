# OS-Maker

You need linux, nasm and genisoimage, after running AssemblyToC.convert_to_header(origin, destination) 
import the header normally from the destination, the AssemblyToC.convert_to_script(origin, destination) is the 
same thing of the AssemblyToC.convert_to_header(origin, destination) but is not header, its C script, 
run omc and the ISO destination with the python script and the python script
folder and the script name without extensions example: 'omc myos.iso myos_script.py . myos_script', and all will be
runned in a function called main() and the OS will be x86