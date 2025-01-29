import re
import requests
import socket
from urllib.parse import urlparse
from datetime import datetime

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


def get_target_url():
    target_url = input("Enter the target URL (e.g., https://example.com): ").strip()
    if not target_url:
        print("Error: No URL provided. Exiting.")
        exit(1)
    return target_url

def clean_url(target_url):
    return re.sub(r'[^a-zA-Z0-9]', '_', target_url)

def save_results(filename, data):
    with open(filename, 'a') as f:
        f.write(data + '\n')

def extract_comments(target_url, output_file):
    print("\n[+] Running Comment Extractor on", target_url)
    response = requests.get(target_url)
    comments = re.findall(r'<!--(.*?)-->', response.text)
    results = '\n'.join(comments)
    print(results)
    save_results(output_file, results)

def sri_checker(target_url, output_file):
    print("\n[+] Running SRI Checker on", target_url)
    domain = urlparse(target_url).netloc
    response = requests.get(target_url)
    js_links = re.findall(r'src=["\'](https://.*?\.js)["\']', response.text)
    for js_url in js_links:
        if domain not in js_url:
            response_js = requests.get(js_url)
            if 'integrity="' in response_js.text:
                result = f"{js_url} - SRI: In use"
            else:
                result = f"{js_url} - SRI: Not in use"
            print(result)
            save_results(output_file, result)

def extract_links(target_url, output_file):
    print("\n[+] Running Link Extractor on", target_url)
    response = requests.get(target_url)
    links = re.findall(r'href=["\'](.*?)["\']', response.text)
    results = '\n'.join(sorted(set(links)))
    print(results)
    save_results(output_file, results)

def extract_images(target_url, output_file):
    print("\n[+] Running Image Scraper on", target_url)
    response = requests.get(target_url)
    images = re.findall(r'src=["\'](.*?\.(jpg|jpeg|png|gif|svg))["\']', response.text)
    results = '\n'.join(sorted(set(img[0] for img in images)))
    print(results)
    save_results(output_file, results)

def analyze_headers(target_url, output_file):
    print("\n[+] Running HTTP Header Analysis on", target_url)
    response = requests.head(target_url)
    headers = response.headers
    results = '\n'.join(f"{key}: {value}" for key, value in headers.items())
    print(results)
    save_results(output_file, results)

def dns_lookup(target_url, output_file):
    print("\n[+] Running DNS Lookup on", target_url)
    domain = urlparse(target_url).netloc
    ip_address = socket.gethostbyname(domain)
    print(f"{domain} resolves to {ip_address}")
    save_results(output_file, f"{domain} resolves to {ip_address}")

def main():
    display_banner()
    target_url = get_target_url()
    output_file = f"webXscan_{clean_url(target_url)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_output.txt"
    print("Results saved to:", output_file)

    print("\nChoose a module to run:")
    print("1) Comment Extractor")
    print("2) SRI Checker")
    print("3) Link Extractor")
    print("4) Image Scraper")
    print("5) HTTP Header Analyzer")
    print("6) DNS Lookup")
    print("7) Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == '1':
        extract_comments(target_url, output_file)
    elif choice == '2':
        sri_checker(target_url, output_file)
    elif choice == '3':
        extract_links(target_url, output_file)
    elif choice == '4':
        extract_images(target_url, output_file)
    elif choice == '5':
        analyze_headers(target_url, output_file)
    elif choice == '6':
        dns_lookup(target_url, output_file)
    elif choice == '7':
        print("Exiting WebXScan. Goodbye!")
        exit(0)
    else:
        print("Invalid choice. Please run the script again and select a valid option.")
        exit(1)

if __name__ == "__main__":
    main()