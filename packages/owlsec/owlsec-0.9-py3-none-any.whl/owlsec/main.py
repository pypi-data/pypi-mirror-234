import argparse
from .scripts.pentesting.passive_subdomains import get_subdomains_and_urls
from .scripts.pentesting.find_software import run_httpx_for_domain
from .scripts.pentesting.common_files import get_file_details
from .scripts.pentesting.common_login_forms import get_burp_responses
from .scripts.pentesting.common_ports import port_scan
from .scripts.pentesting.SSL_check import SSLChecker
from .scripts.input_handling.input_filtering import identify_domain_type, clean_domain, get_domain_type_messages
from .scripts.ascii_art import print_ascii_art

def print_interesting_urls_and_subdomains(domain):
    sorted_subdomains, interesting_urls = get_subdomains_and_urls(domain)
    
    if interesting_urls:
        print("\nInteresting URLs:")
        print("-----------------")
        for interesting_url in interesting_urls:
            print(interesting_url)
    else:
        print("\nNo interesting URLs scraped from the archive.")
    
    if sorted_subdomains:
        print("\nFound Subdomains:")
        print("-----------------")
        for subdomain_found in sorted_subdomains:
            print(subdomain_found)
    else:
        print("\nNo subdomains found from the archive.")
    
    return sorted_subdomains

def print_port_scan_results(domain):
    tcp_ports, udp_ports = port_scan(domain)
    print(f"\nOpen TCP ports: {', '.join(map(str, tcp_ports))}")
    print(f"Open UDP ports: {', '.join(map(str, udp_ports))}")
    return tcp_ports
    
def print_httpx_results(domain):
    result = run_httpx_for_domain(domain)
    print("\nHTTPX Result:")
    print("=============")
    print(result['raw_output'])
    
    # Check conditions
    is_alive = "[FAILED]" not in result['raw_output']
    has_cloudflare = "cloudflare" in result['raw_output'].lower()

    # Print detected keywords only if they exist
    detected_keywords = ", ".join(result['detected_keywords'])
    if detected_keywords.strip():
        print("\nDetected Keywords:")
        print("==================")
        print(detected_keywords)

    # Return dictionary with results
    return {
        "is_alive": is_alive,
        "has_cloudflare": has_cloudflare
    }

def print_file_details(domain):
    details = get_file_details(domain)
    print("\nCommon Files & Directories:")
    print("---------------------------")
    for detail in details:
        print(detail)

def print_login_forms(domain):
    responses = get_burp_responses(domain)
    print("\nLogin Forms:")
    print("------------")
    for action_key, details in responses.items():
        print(f"\nAction URL: {action_key}")
        print(f"Form Parameters: {details['form_parameters']}")
        print(f"Status: {details['possible_login_form']}")
        if details['request']:
            print("Request:")
            print(details['request'])
        print("-" * 40)

def check_and_print_ssl_status(domain):
    checker = SSLChecker()
    results, summary = checker.show_result(domain)
    
    def print_results(results, summary):
        valid_results_exist = any(isinstance(context, dict) for _, context in results)

        if valid_results_exist:
            print("\nSSL Certificate Details:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        for host, context in results:
            if isinstance(context, dict):
                print(f"Details for: {host}")
                print("-" * (len(host) + 14))  # Dynamic underlining based on host length
                
                for key, value in context[host].items():

                    # Highlight expired certificates with "!!!"
                    if key == 'cert_exp' and value:
                        print("  !!! CERTIFICATE EXPIRED !!!")

                    # Highlight warning for certificates near expiry
                    if key == 'valid_days_to_expire' and value <= 15:
                        print("  !!! CERTIFICATE EXPIRING SOON !!!")

                    # Pretty printing for long lists like cert_sans
                    if key == 'cert_sans' and len(str(value)) > 100:
                        print(f"  {key.capitalize().replace('_', ' ')}:")
                        for item in value.split(';'):
                            print(f"    - {item.strip()}")
                    else:
                        print(f"  {key.capitalize().replace('_', ' ')}: {value}")
                print("\n")  # Add a newline between different host results
            else:
                # Handle error messages in a user-friendly way
                if "Temporary failure in name resolution" in context:
                    pass
                    #print(f"\nError for {host}: Unable to resolve the domain name. The domain may be down or nonexistent.\n")
                else:
                    pass
                    #print(f"\nError for {host}: {context}\n")

    if not results and not summary:
        print("\nUnable to retrieve SSL status.")
    else:
        has_valid_results = any(isinstance(context, dict) for _, context in results)
        print_results(results, summary)

def main(domain, domain_type):

    httpx_result = {}  # Initialize to avoid potential NameError

    if domain_type == "Domain":
        print(f"Retrieving subdomains and interesting archive URLs for: {domain}...")
        sorted_subdomains = print_interesting_urls_and_subdomains(domain)
        # If no subdomains are found, use the main domain as a subdomain
        if not sorted_subdomains:
            sorted_subdomains = [domain]
        for subdomain in sorted_subdomains:
            print(f"\nChecking if {subdomain} has cloudflare...")
            httpx_result = print_httpx_results(subdomain)
    elif domain_type == "IP":
        sorted_subdomains = [domain]
        subdomain = domain  # Define subdomain in this scope
            
    if httpx_result.get("is_alive") and not httpx_result.get("has_cloudflare") or domain_type == "IP":
        print(f"Port scanning {subdomain} as it has no cloudflare...")
        tcp_ports = print_port_scan_results(subdomain)
        
        for tcp_port in tcp_ports:
            ip_port = f"{subdomain}:{tcp_port}"
            print(f"Checking for alternative webservers from the ports found on {subdomain}...")
            httpx_alive = print_httpx_results(ip_port)
            # IF the result from HTTPx doesn't contain [FAILED]
            if httpx_alive["is_alive"]:
                print(f"Checking for common files on each webserver identified {ip_port}...")
                print_file_details(ip_port)
                print(f"Checking for login forms on each webserver identified {ip_port}...")
                print_login_forms(ip_port)
    else:
        print(f"\nSkipping all subdomains for port scanning, alternative webserver identification, directory checking and login form finding due to either cloudflare or being offline")
    check_and_print_ssl_status(domain)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run pentesting tasks on the target domain or IP.')
    parser.add_argument('-d', '--domain', type=str, help='Target domain')
    return parser.parse_args()


def run():
        # Call the function to display the ASCII art
    print_ascii_art()
    print("Project still in development...")
    
    args = parse_arguments()
    
    if args.domain:
        domain = args.domain
    else:
        domain = input(f"HOOOO is your target?: ")
    
    domain_type = identify_domain_type(domain)
    domain_type_messages = get_domain_type_messages()
    
    if domain_type in domain_type_messages:
        print(domain_type_messages[domain_type])
        if domain_type == "Domain":
            cleaned_domain = clean_domain(domain)
            main(cleaned_domain, domain_type)
        elif domain_type == "IP":
            print("IP Address detected.")
            main(domain, domain_type)
        elif domain_type == "TRYHACKME":
            print("TryHackMe TLD (.thm) detected. Not implemented yet.")
        elif domain_type == "HACKTHEBOX":
            print("HackTheBox TLD (.htb) detected. Not implemented yet.")
    elif domain_type == "Invalid":
        print("Invalid domain or IP detected.... Try again.")

if __name__ == "__main__":
    run()