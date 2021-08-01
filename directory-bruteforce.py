# Directory bruteforce 2021.
##      Discovers hidden directories on domain, like DIRB
##      file_name tested with the DIRB "common.txt" wordlist
##      Highlights predefined potential hits of interest

# Todo: Add prompt for "use common.txt?"
##      Add list of interesting sites and print type "found x site"
##      Search recursive
##      Fix double print (e.g. "robots" & "robots.txt", although only "robots.txt" exists on test server).


# --- Libraries ---
import requests
from termcolor import colored

# User input
target_url = input("[+] Enter Target URL: ")
file_name = input("[+] Enter Name Of The File Containing Directories: ")

found_interests = []
interest_flag = False


# Request function, tries the URL
def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


# Find interest function, summarize
def interest(dir):
    interests = ["login", "admin", "signin", "passwords"]
    global found_interests
    global interest_flag
    if dir in interests:
        print(colored(("[!!] Found Potential Interest At Path:       " + full_url), "green"))
        found_interests.append(dir)
        interest_flag = True


file = open(file_name, "r")
for line in file:
    directory = line.strip()
    full_url = target_url + "/" + directory
    response = request(full_url)
    if response: # if there is something in response variable, do something
        interest(directory)
        if "." in directory and interest_flag is False:
            print(colored(("[*] Discovered File At Path:                 " + full_url), "yellow"))
            continue
        elif "." not in directory and interest_flag is False:
            print("[*] Discovered Directory At Path:            " + full_url)
            continue
        interest_flag = False


if found_interests != "":
    print(colored(("\n The following hits might be of particular interest: "), "green"))
    for hits in found_interests:
        print(" - " + target_url + "/" + hits)
        exit()