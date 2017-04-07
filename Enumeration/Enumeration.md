# Enumeration

## Initial enumeration
A script has been written and provided in this same directory which enables you to perform nmap, nikto and dirb against an IP address.
The ports for nikto and dirb are provided by the user, based on the nmap scan.
The user can also choose to not run nikto and/or dirb.
All reports from the tools are being saved in the current directory the script is run from.

Example of running the tool:

    *python init-enum.py <IP_ADDRESS>*
      --> Runs nmap scan with -sA flag

    Do you want to run Nikto (yes/no)?
      yes
      Please provide the port numbers containing a web server from the Nmap scan:
        80,5000
        --> Runs Nikto against ports provided by the user (80,5000)

    Do you want to run Dirb (yes/no)?
      yes
      Please provide the port numbers containing a web server from the Nmap/Nikto scan:
        80,443
        --> Runs dirb against ports provided by the user again (80,443)
