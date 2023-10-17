import re
from .tldlist import tlds

def load_tlds_from_file(filename):
    valid_tld_pattern = re.compile(r"^[a-zA-Z0-9.]+$")
    tlds = set()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                stripped_line = line.strip()
                if valid_tld_pattern.match(stripped_line):
                    tlds.add(stripped_line)
        return tlds
    except FileNotFoundError:
        print(f"File {filename} not found. Make sure the path and filename are correct.")
        return set()

def identify_domain_type(domain):
    ip_pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?::\d{1,5})?$")

    # No need to load TLDs from file anymore, directly using imported `tlds`
    
    domain_parts = domain.lower().split(".")

    # Check if domain ends with "THM"
    if domain.lower().endswith((".thm")):
        return "TRYHACKME"

    # Check if domain ends with "HTB"
    if domain.lower().endswith((".htb")):
        return "HACKTHEBOX"

    # Check if the last part of the domain is in the list of TLDs
    if ip_pattern.match(domain):
        return "IP"

    if domain_parts[-1] in tlds:  
        return "Domain"

    return "Invalid"

def clean_domain(domain):
    # Remove http://www., https://www., http://, https://
    domain = re.sub(r'^https?:\/\/(www\.)?', '', domain)
    # Remove everything after the first /
    domain = re.sub(r'\/.*', '', domain)
    return domain

def get_domain_type_messages():
    return {
        "IP": "IP address detected instead of a domain...",
        "TRYHACKME": "TRYHACKME detected instead of a domain...",
        "HACKTHEBOX": "HACKTHEBOX detected instead of a domain...",
        "Domain": "Domain detected..."
    }