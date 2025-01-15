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
