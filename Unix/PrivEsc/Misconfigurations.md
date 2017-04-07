# Common Misconfigurations

## User home permissions
Some users might have scripts or backup files in their home folders containing sensitive information. It should be checked if the home directories can be read by the current user.

## SETGID and SETUID binaries
If a file has a SUID bit and is owned by root, this can be leveraged to gain root privileges. For example, if the SUID binary is running a non-absolute path to a tool, which can then be misuses by creating a symlink through changing the PATH-variable.  

One can find files with a SUID bit using:

    find / -user root -perm -4000 -print 2>/dev/null    # SUID bit
    find / -user root -perm -2000 -print 2>/dev/null    # SGID bit

## World Readable/Writable
This type of misconfiguration may aid the attacker to gain access to files and/or directories which contain sensitive information. He may even alter the data. These type of world-readable -or writable files/directories can be found using:  

    find / -perm -2 ! -type l -ls

##
