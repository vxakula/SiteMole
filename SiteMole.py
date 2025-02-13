import argparse
import re
import requests
import socket
import subprocess
import os
from urllib.parse import urlparse
from termcolor import colored

def display_banner():
    banner = r"""
 ____  _ _       __  __       _      
/ ___|(_) |_ ___|  \/  | ___ | | ___ 
\___ \| | __/ _ \ |\/| |/ _ \| |/ _ \
 ___) | | ||  __/ |  | | (_) | |  __/
|____/|_|\__\___|_|  |_|\___/|_|\___|
                                    by ChiZu
                                    
https://github.com/vxChiZu
    """
    print(banner)

def extract_comments(target_url):
    print("\n[+] Running Comment Extractor on", target_url)
    response = requests.get(target_url)
    comments = re.findall(r'<!--(.*?)-->', response.text)
    output = "\n".join(comments)
    print(output)
    return output

def sri_checker(target_url):
    print("\n[+] Running SRI Checker on", target_url)
    domain = urlparse(target_url).netloc

    curl_command = [
        "curl", "-s", "-L",
        "--cookie", "cookies.txt",
        "--cookie-jar", "cookies.txt",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        target_url
    ]
    result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    page_source = result.stdout

    # Extract JavaScript and CSS URLs while removing duplicates using a set
    resource_links = set(re.findall(r'https://[^"\'>]+(?:\.js|\.css)', page_source, re.IGNORECASE))

    if not resource_links:
        print("\n❌ No external JavaScript or CSS resources found.")
        return "No external JavaScript or CSS resources found."

    # ✅ Print extracted URLs only ONCE
    print("\n[+] Extracted JavaScript and CSS URLs:")
    for link in resource_links:
        print(link)  # Ensure this isn't printed twice

    sri_in_use = []
    sri_not_in_use = []

    for resource_url in resource_links:
        resource_domain = urlparse(resource_url).netloc
        if resource_domain != domain:
            curl_check_command = ["curl", "-s", "-L", resource_url]
            try:
                resource_content = subprocess.run(curl_check_command, capture_output=True, text=True, encoding='utf-8', errors='ignore').stdout
                if resource_content and 'integrity="' in resource_content:
                    sri_in_use.append(resource_url)
                else:
                    sri_not_in_use.append(resource_url)
            except Exception as e:
                print(f"❌ Failed to fetch {resource_url}: {e}")

    output = ""

    if sri_in_use:
        output += "\n✅ Resources with SRI in use:\n" + "\n".join(sri_in_use)
    if sri_not_in_use:
        output += "\n❌ Resources without SRI:\n" + "\n".join(sri_not_in_use)

    print(output)
    return output


def extract_links(target_url):
    print("\n[+] Running Link Extractor on", target_url)
    response = requests.get(target_url)
    links = re.findall(r'href=["\'](.*?)["\']', response.text)
    output = "\n".join(sorted(set(links)))
    print(output)
    return output

def extract_images(target_url):
    print("\n[+] Running Image Scraper on", target_url)
    response = requests.get(target_url)
    images = re.findall(r'src=["\'](.*?\.(jpg|jpeg|png|gif|svg))["\']', response.text)
    output = "\n".join(sorted(set(img[0] for img in images)))
    print(output)
    return output

def analyze_headers(target_url):
    print("\n[+] Running HTTP Header Analysis on", target_url)
    response = requests.head(target_url)
    headers = response.headers

    # Headers categorized
    critical_headers = ["Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options", 
                         "Content-Security-Policy", "Referrer-Policy", "Permissions-Policy"]

    warning_headers = ["Feature-Policy", "X-Permitted-Cross-Domain-Policies", 
                       "Cross-Origin-Embedder-Policy", "Cross-Origin-Resource-Policy", 
                       "Cross-Origin-Opener-Policy", "Expect-CT"]

    output = []

    for header in critical_headers:
        if header in headers:
            output.append(f"{header}: {headers[header]}")
        else:
            output.append(colored(f"❌ {header} is missing!", "red"))

    for header in warning_headers:
        if header in headers:
            output.append(f"{header}: {headers[header]}")
        else:
            output.append(colored(f"⚠️ {header} is missing!", "yellow"))

    # Special case: X-XSS-Protection should be marked in red if present
    if "X-XSS-Protection" in headers:
        output.append(colored(f"❌ X-XSS-Protection found! (Deprecated, remove it!)", "red"))

    # Print results
    print("\n".join(output))
    return "\n".join(output)
    
def run_all_modules(target_url):
    """ Run all modules and save output to a file """
    print("\n[+] Running all modules and saving results to results.txt")

    results = []

    results.append("===== Comments Extractor =====")
    results.append(extract_comments(target_url))

    results.append("\n===== SRI Checker =====")
    results.append(sri_checker(target_url))

    results.append("\n===== Link Extractor =====")
    results.append(extract_links(target_url))

    results.append("\n===== Image Scraper =====")
    results.append(extract_images(target_url))

    results.append("\n===== Header Analysis =====")
    results.append(analyze_headers(target_url))

    file_path = os.path.join(os.getcwd(), "results.txt")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print(f"[+] Results saved to {file_path}")
    except Exception as e:
        print(f"❌ Failed to write results to file: {e}")

def select_module():
    """ Interactive menu if no module is provided """
    while True:
        print("\n🤔 Select a module:\n")
        print("1) Comments Extractor")
        print("2) SRI Checker")
        print("3) Link Extractor")
        print("4) Image Scraper")
        print("5) Header Analysis")
        print("9) Run All Modules and Save to File")
        print("0) Exit")

        choice = input("Choose a module (1-8): ").strip()

        modules = {
            "1": "comments",
            "2": "sri",
            "3": "links",
            "4": "images",
            "5": "headers",
            "9": "all",
            "0": "exit"
        }

        selected = modules.get(choice, None)

        if selected:
            return selected
        else:
            print("❌ Invalid choice! Please try again.")

def main():
    parser = argparse.ArgumentParser(description="SiteMole - Web Reconnaissance Tool")
    parser.add_argument("-t", "--target", help="Target URL (e.g., https://example.com)")
    parser.add_argument("-m", "--module", choices=["comments", "sri", "links", "images", "headers", "", "all"], help="Module to run")

    args = parser.parse_args()

    display_banner()

    if not args.target:
        args.target = input("Enter target URL: ").strip()

    if args.module:  
        # ✅ If -m is provided, run the module ONCE and exit
        target_url = args.target

        if args.module == "comments":
            extract_comments(target_url)
        elif args.module == "sri":
            sri_checker(target_url)
        elif args.module == "links":
            extract_links(target_url)
        elif args.module == "images":
            extract_images(target_url)
        elif args.module == "headers":
            analyze_headers(target_url)
        elif args.module == "all":
            run_all_modules(target_url)

        print("\n👋 Exiting SiteMole. Goodbye!\n")
        exit(0)  # ✅ Immediately exit the script
    else:
        # ✅ If -m is NOT provided, enter interactive mode
        while True:
            args.module = select_module()

            if args.module == "exit":
                print("👋 Exiting SiteMole. Goodbye!")
                break

            target_url = args.target

            if args.module == "comments":
                extract_comments(target_url)
            elif args.module == "sri":
                sri_checker(target_url)
            elif args.module == "links":
                extract_links(target_url)
            elif args.module == "images":
                extract_images(target_url)
            elif args.module == "headers":
                analyze_headers(target_url)
            elif args.module == "all":
                run_all_modules(target_url)

            print("\nReturning to menu...\n")
        args.module = None  # Reset module selection for interactive mode

if __name__ == "__main__":
    main()
