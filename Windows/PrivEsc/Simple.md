# Simple privilege escalation techniques

## getsystem
When you have a meterpreter-session, you can attempt the following command:

    getsystem

This uses the kitrap0d exploit

## Local Exploit Suggester
With a meterpreter-session, you can run the following command to get possibile exploits which may lead to privilege escalation:

    post/multi/recon/local_exploit_suggester

## Psexec
With the psexec-tool *two* things can be done. However, **admin** credentials or access is needed for this to work:
1. From metasploit, pass-the-hash, of which a password or the hash (NTLM) is passed.  
        use exploit/windows/smb/psexec
2. As an admin user, run the following command to get SYSTEM privileges:
        psexec.exe -s cmd.exe
