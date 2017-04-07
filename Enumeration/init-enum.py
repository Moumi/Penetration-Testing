#!/usr/bin/python
# Python script with the abilities to do a stander/detailed scan on TCP/UDP
# Usage:
#   python inital-enum.py 127.0.0.1
#       This will perform an nmap scan on TCP Ports
#       Afterwards, ports can be provided to run Nikto on
#       Next, ports can be provided for dirb

import sys
try:
    import subprocess as sub
    compatmode = 0 # newer version of python, no need for compatibility mode
except ImportError:
    import os # older version of python, need to use os instead
    compatmode = 1

# ==== VARIABLES ====
ip_address 		= ""
port_nrs 		= ""
# ==== VARIABLES ====

# title / formatting
bigline = "================================================================================================="
smlline = "-------------------------------------------------------------------------------------------------"

print bigline
print "ENUMERATOR - BY MOUMI"
print bigline

def run_command(command, results):
	if compatmode == 0: # newer version of python, use preferred subprocess
        out, error = sub.Popen([cmd], stdout=sub.PIPE, stderr=sub.PIPE, shell=True).communicate()
        results += out.split('\n')
    else: # older version of python, use os.popen
        echo_stdout = os.popen(cmd, 'r')
        results += echo_stdout.read().split('\n')

    results += "\n\n\n"
    return results

# print results for each previously executed command, no return value
def printResults(cmdDict):
    for item in cmdDict:
        msg = cmdDict[item]["msg"]
        results = cmdDict[item]["results"]
        print "[+] " + msg
        for result in results:
            if result.strip() != "":
                print "    " + result.strip()
    print
    return

def writeResults(msg, results):
    f = open(out_file, "a");
    f.write("[+] " + str(len(results)-1) + " " + msg)
    for result in results:
        if result.strip() != "":
            f.write("    " + result.strip())
    f.close()
    return

# ----------------------- NMAP ------------------------
nmap_result = []
def run_nmap_scan():
	print "[*] GETTING NMAP SCAN RESULTS...\n"

	# Get IP addresses
	ip_addresses = raw_input("Please enter the IP address: ")
	nmap_report_file = ip_address.split(".")[3] + "_nmap_tcp.txt"
	print "\t[-] Entered IP addresses: " + ip_address

	# Run Nmap scan against host
	nmap_cmd = "nmap -sA " + ip_address
	run_command(nmap_cmd, nmap_result)

	# Save output
	writeResults("Nmap Scan on host " + ip_address, nmap_result)
    print "\t[+] Finished Nmap Scan. Report saved as:" + nmap_report_file
    return nmap_result
# ----------------------- NMAP ------------------------

# ----------------------- NIKTO -----------------------
nikto_result = []
def run_nikto_scan(ip_address):
	print "[*] GETTING NIKTO SCAN RESULTS...\n"

	# Get Ports to scan
	port_nrs = raw_input("Please provide the port numbers containing a web server from the Nmap scan: ")
	nikto_report_file = ip_address.split(".")[3] + "_nikto_" + port_nrs.replace(",", "-") + '.txt'
	print "\t[-] Entered Port numbers: " + port_nrs

	# Run Nikto scan with assigned port numbers
	nikto_cmd = "nikto -h " + ip_address + " -p " + port_nrs
	run_command(nikto_cmd, nikto_result)

	# Save output
	writeResults("Nikto Scan on host " + ip_address + " - " + port_nrs, nikto_result)
	print "\t[+] Finished Nikto Scan. Report saved as:" + nikto_report_file
	return nikto_result
# ----------------------- NIKTO -----------------------

# ----------------------- DIRB ------------------------
dirb_result = []
def run_dirb_scan(ip_address, port_nrs):
	print "[*] GETTING DIRB SCAN RESULTS...\n"

	# Get Ports to scan
	port_nrs = raw_input("Please provide the port numbers containing a web server from the Nmap/Nikto scan: ")
	dirb_report_file = ip_address.split(".")[3] + "_dirb_" + port_nrs.replace(",", "-") + '.txt'
	print "\t[-] Entered Port numbers: " + port_nrs

	# Run Dirb scan with assigned port numbers
	dirb_cmd = ""
	dirb_cmd_base = "dirb http://" + ip_address

	# Check if SSL port (443)
	for port in port_nrs.split(","):
		if port == '443' or port == 443 or port == "443":
			dirb_cmd = dirb_cmd_base.replace("http", "https")
		else:
			dirb_cmd = dirb_cmd_base + ":" + port + "/"

		run_command(dirb_cmd, dirb_result)

	# Save output
	writeResults("Dirb Scan on host " + ip_address + " - " + port_nrs, dirb_result)
	print "\t[+] Finished Dirb Scan. Report saved as:" + dirb_report_file
	return nikto_result
# ----------------------- DIRB ------------------------

# [1] Run Nmap Scan
run_nmap_scan()

# [2] Run Nikto Scan
run_nikto = raw_input("Do you want to run Nikto (yes/no)? ")
if run_nikto == "yes":
    run_nikto_scan(ip_address)

# [3] Run Dirb Scan
run_dirb = raw_input("Do you want to run Dirb (yes/no)? ")
if run_dirb == "yes":
    run_dirb_scan(ip_address)

print
print "Finished"
print bigline
