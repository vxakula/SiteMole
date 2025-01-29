# SiteMole
Tool to make the life of web-pentesters a little easier.


SiteMole is a Python-based web reconnaissance tool designed to assist security professionals and enthusiasts in gathering information about a target website. The tool provides various modules to extract valuable insights, including comments, links, images, HTTP headers, and more.

## Features

- **Comment Extractor:** Extracts HTML comments from the target webpage.

- **Subresource Integrity (SRI) Checker:** Checks if external JavaScript files use integrity attributes.

- **Link Extractor:** Collects all links found on the page.

- **Image Scraper:** Gathers all image URLs (JPG, PNG, GIF, SVG) from the target.

- **HTTP Header Analyzer:** Retrieves and displays HTTP headers from the server.

- **DNS Lookup:** Resolves the target domain to its IP address.

## Installation

Ensure you have Python 3 installed along with the required dependencies:
```
pip install requests
```

## Usage

Clone the repository:
```
git clone https://github.com/vxChiZu/SiteMole.git
cd SiteMole
```
Run the script:
```
python SiteMole.py
```
Enter the target URL when prompted.

Select a module from the menu to run the desired scan.

Example Output
```
Enter the target URL (e.g., https://example.com): https://example.com
Results saved to: SiteMole_https_example_com_20240119_153000_output.txt

Choose a module to run:
1) Comment Extractor
2) SRI Checker
3) Link Extractor
4) Image Scraper
5) HTTP Header Analyzer
6) DNS Lookup
7) Exit
```
## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with your improvements.

## Disclaimer

**Use this tool for ethical and lawful purposes only. The author takes no responsibility for any misuse or illegal activities carried out using SiteMole.**

