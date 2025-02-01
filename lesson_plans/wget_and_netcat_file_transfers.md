<h2>FILE TRANSFER WITH WGET and NETCAT</h2>

![howToTransferStuff](https://github.com/user-attachments/assets/71819fe0-cdba-4605-8724-ddfdbfd2fd6f)

</br> ---
</br>2 computers in this scenario
</br>I have a terminal on a target computer and I want to get files from that computer.
</br>If I am on FTP, I can GET filename
</br>> get potato.txt
</br>If I have another terminal, I need to do something tricky to relay the file...
</br>
</br>Via the Python http server method
</br>(this is being run on the target machine)
</br>Python2 syntax -  `python -m SimpleHTTPServer 1812`
</br>Python3 syntax -`python3 -m http.server 1812`
</br>`Serving HTTP on 0.0.0.0 port 1812 (http://0.0.0.0:1812/) ...`
</br>(as usual, the port, 1812, is arbitrary)
</br>
</br>get single file (this is being run in an attack machine terminal)
</br>`wget http://10.10.253.61:1812/potato.txt`
</br>
</br>Getting a bunch of files
</br>then download it all with a wget request from another terminal
</br>`wget -r http://10.10.253.61:1812`
</br>
</br>By default, `wget` creates a directory named after the domain or IP address from which the files are being downloaded.
</br>-P  allows an output path, can create a new dir to set things to
</br>
</br>`wget -r -P /path/to/output/directory http://10.10.253.61:1812
</br>
</br>Using netcat for
</br>Transferring files from one machine to another (assuming we want all contents of Target_directory)
</br>
</br>assuming the target directory is /assets/images
</br>(on the target machine)
```sh
cd /assets/images
tar -czf - * | nc -l -p 1984
```
- `tar -czf - *`: This command creates a tarball of the directory contents and sends it to standard output. | connects...
- `nc -l -p 1984: This starts` netcat in listening mode on port 1984. This lets it "serve" things like the http server

</br>(Atk machine)
```sh 
nc 10.10.253.61 1984 | tar -xzf -`
```
- `nc 10.10.253.61 1984: connect to the target 
- machine's `netcat` server on port 1984.
- `tar -xzf -`: This extracts the tarball received from the `netcat` connection.
- The `-z` option in `tar` is for gzip compression. You can omit the `z` in both `tar` commands, but for big files this will make the transfer longer, so it's pretty standard to shrink the filesize down

</br> read tarball on a single line, checking contents (in a ctf, this is faster to see if it's a flag or something)

``` sh
tar -O -xzf archive.tar.gz myNote.txt
```
- `-O`: (the number, not the letter) Extract files to standard output (stdout).
- This will display myNote.txt in the command line

</br>Read what's in the tarball (actually getting the file):

```sh
tar -tzf archive.tar.gz
```

- `-t`: List the contents of the tarball.
- `-z`: Use gzip compression (if the tarball is compressed with gzip).
- `-f`: Specify the tarball file.

### 2. Extract a Specific File from the Tarball

</br>To extract just the `myNote.txt` file from the tarball:
```sh
tar -xzf archive.tar.gz myNote.txt
```

- `-x`: Extract files from the tarball.
- `-z`: Use gzip compression.
- `-f`: Specify the tarball file.
