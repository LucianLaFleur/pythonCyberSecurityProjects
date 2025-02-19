basic scanning to see what ports are alive

nmap -sT -p- -T4 10.10.91.118 -v
```
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
443/tcp   open  https
51337/tcp open  unknown
```

! 51337 is suspicious...

scanning for basic scripts against found ports on T4 timing
nmap -sT  -A -T4 10.10.91.118 -v

```
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http     Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
443/tcp open  ssl/http Apache httpd 2.4.41
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: 403 Forbidden
| ssl-cert: Subject: commonName=grep.thm/organizationName=SearchME/stateOrProvinceName=Some-State/countryName=US
| Issuer: commonName=grep.thm/organizationName=SearchME/stateOrProvinceName=Some-State/countryName=US
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-06-14T13:03:09
| Not valid after:  2024-06-13T13:03:09
| MD5:   7295 8ef0 7c16 221c 3b0a 40ee 913c 766c
|_SHA-1: 38c2 3ba3 34b1 851a f1d4 ee0a 37bd 701a 830c 7dd8
| tls-alpn: 
|_  http/1.1
```

we see the common name in the ssl certificate
`commonName=grep.thm`

when we see an ssl certificate in the nmap advanced scan, what do we look for?
Find more info about the ssl certificate itself through the browser
...

find the organization name "SearchME" among the cert details

`nano /etc/hosts`
edit the dns resolution using the ip of the target and the name we found associated with the ssl certificate, namely, grep.thm


putting `grep.thm` in the URL bar, this allows the ssl cert to resolve, since it can find the associated name with the server as indicated in out modified /etc/hosts file. 
We still have to "accept risks and continue" since it's a self-signed cert, so the browser thinks that's suspicious. However, we have access to the formerly 403'd page, giving us some kind of index page. 

(would run gobuster but the simple syntax can't connect with this structure...)

just looking around in the source code, the login and register pages are in php. 

Furthermore, the code in  the registration page indicates a js file
`https://grep.thm/public/html/register.php`
Following the pathing, double-dot is up one directory, so instead of html, it should be /js/register.js. The full target path should be 
`https://grep.thm/public/js/register.js` 

raw register.js code for reference:
```
function register() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var email = document.getElementById('email').value;
    var name = document.getElementById('name').value;
    fetch('../../api/register.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Thm-Api-Key': 'e8d25b4208b80008a9e15c8698640e85'
      },
      body: JSON.stringify({
        username: username,
        password: password,
        email: email,
        name: name,
      }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        alert('Registration successful! Please login.');
        window.location.href = 'login.php';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }
```

Here we find an API key...
e8d25b4208b80008a9e15c8698640e85
but it is not the answer

open burpsuite. Since we're dealing with an https setup, make sure the foxyproxy layer understands this by going into proxies and changing the type to https

foxyproxy isn't playing nice, so In burpsuite I open burp's browser on the proxy tab. This requires me to go into burp's settings > burp's browser > allow burp without a sandbox. Then I can open up purp's browser with the button inside the burpsuite window and get a chromium window

the registry thing says our api key is invalid or expired...

`ffe60ecaa8bba2f12b43d1a4b15b8f39`

THM{4ec9806d7e1350270dc402ba870ccebb}

inspecting paths to stuff called on the page, similar to earlier...
`https://grep.thm/public/js/dashboard.js`

```
fetch('../../api/posts.php')
.then(response => response.json())
.then(data => {
  if (data.error) {
    alert(data.error);
  } else {
    var postsDiv = document.getElementById('posts');
    data.forEach(post => {
      var postDiv = document.createElement('div');
      postDiv.classList.add('post');
      postDiv.innerHTML = `<h3>${post.title}</h3><p>${post.content}</p><hr>`;
      postsDiv.appendChild(postDiv);
    });
  }
})
.catch((error) => {
  console.error('Error:', error);
});
```


in addition to "dashboard" there was an upload.php file in the supersecuredeveloper github repo.

...
later, look at https://<ip>:51337
go into the certificate info like before, and we find a different name on the certificate. 
We need to add this leakchecker.grep.thm to the /etc/hosts as well


make a php reverse shell.
using the pentest monkey template for php reverse shell

2 hex = 1 ascii, so if it's looking for magic bytes at the start and we can juggle 4 bytes of data to the side, then it should be fine

hexedit to overwrite the ascii char data, making our bootleg magic bytes customized at the start


ref magic bytes we need
ffd8ffe0

bunch of uploads are getting an error about not being able to launch the daemon for the php rev shell... reference for this annoying address sinc eI ened to keep re-doing uploads
`https://grep.thm/public/html/upload.php`
connection still refused

enumerate on subdirectories, recursively within the https://grep.thm/public/html/ directory
gobuster dir -u https://grep.thm:51337 -w /usr/share/dirb/wordlists/big.txt -r -t 40

after an upload, the files will be listed here:
https://grep.thm/api/uploads
if it's in php format, clicking on it should launch it, allowing you to catch a reverse shell on a netcat listener
if you get a "failed to daemonise" error, check that the php revshell has the attack-machine IP listed in the ip address


(1, 'test', '$2y$10$dE6VAdZJCN4repNAFdsO2ePDr3StRdOhUJ1O/41XVQg91qBEBQU3G', 'test@grep.thm', 'Test User', 'user'),
(2, 'admin', '$2y$10$3V62f66VxzdTzqXF4WHJI.Mpgcaj3WxwYsh7YDPyv1xIPss4qCT9C', 'admin@searchme2023cms.grep.thm', 'Admin User', 'admin');
