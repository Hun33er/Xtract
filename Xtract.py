import requests
import re
from urllib.parse import urljoin, urlparse
import os
from bs4 import BeautifulSoup
import argparse
from typing import Set, List, Dict

class JSEndpointExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.processed_urls = set()
        self.js_files = set()
        self.endpoints = set()

    def is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def extract_js_from_html(self, url: str) -> Set[str]:
        """Extract JS file URLs from HTML content"""
        js_urls = set()
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup.find_all('script', src=True):
                js_url = urljoin(url, script['src'])
                if js_url.endswith(('.js', '.json')) and self.is_valid_url(js_url):
                    try:
                        js_response = self.session.head(js_url, timeout=5)
                        if js_response.status_code == 200:
                            js_urls.add(js_url)
                        else:
                            print(f"Filtered out {js_url} (Status: {js_response.status_code})")
                    except requests.RequestException:
                        print(f"Filtered out {js_url} (Inaccessible)")
        except Exception as e:
            print(f"Error fetching HTML from {url}: {str(e)}")
        return js_urls

    def extract_endpoints_from_js(self, content: str, base_url: str) -> Set[str]:
        """Extract API endpoints from JS content"""
        endpoints = set()
        patterns = [
            r'["\'](/[a-zA-Z0-9_/-]+)["\']',
            r'url:\s*["\'](/[a-zA-Z0-9_/-]+)["\']',
            r'fetch\(["\'](/[a-zA-Z0-9_/-]+)["\']',
            r'axios\.[a-z]+\(["\'](/[a-zA-Z0-9_/-]+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                endpoint = match.strip("'\"")
                full_url = urljoin(base_url, endpoint)
                endpoints.add(full_url)
        return endpoints

    def extract_js_references(self, content: str, base_url: str) -> Set[str]:
        """Extract references to other JS files from JS content"""
        js_urls = set()
        patterns = [
            r'["\']([a-zA-Z0-9_/.-]+\.js)["\']',
            r'["\']([a-zA-Z0-9_/.-]+\.json)["\']',
            r'src=["\']([a-zA-Z0-9_/.-]+\.js)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                full_url = urljoin(base_url, match)
                if self.is_valid_url(full_url):
                    try:
                        js_response = self.session.head(full_url, timeout=5)
                        if js_response.status_code == 200:
                            js_urls.add(full_url)
                        else:
                            print(f"Filtered out {full_url} (Status: {js_response.status_code})")
                    except requests.RequestException:
                        print(f"Filtered out {full_url} (Inaccessible)")
        return js_urls

    def process_js_file(self, js_url: str):
        """Process a single JS file and extract endpoints and additional JS references"""
        if js_url in self.processed_urls:
            return
        
        self.processed_urls.add(js_url)
        try:
            response = self.session.get(js_url, timeout=10)
            if response.status_code == 200:
                content = response.text
                new_endpoints = self.extract_endpoints_from_js(content, js_url)
                self.endpoints.update(new_endpoints)
                
                new_js_urls = self.extract_js_references(content, js_url)
                self.js_files.update(new_js_urls)
            else:
                print(f"Filtered out {js_url} (Status: {response.status_code})")
                self.js_files.discard(js_url)
        except Exception as e:
            print(f"Error processing JS file {js_url}: {str(e)}")
            self.js_files.discard(js_url)

    def process_domain(self, url: str):
        """Process a single domain with exhaustive JS file checking"""
        if not self.is_valid_url(url):
            print(f"Invalid URL: {url}")
            return

        print(f"Processing domain: {url}")
        initial_js_files = self.extract_js_from_html(url)
        self.js_files.update(initial_js_files)

        while True:
            unprocessed_js = self.js_files - self.processed_urls
            if not unprocessed_js:
                break
            
            for js_file in unprocessed_js.copy():
                self.process_js_file(js_file)
            
            print(f"Found {len(self.js_files - self.processed_urls)} new JS files to process")

    def process_js_list(self, js_file_path: str):
        """Process a list of JS files from a text file with exhaustive checking"""
        if not os.path.exists(js_file_path):
            print(f"Error: File '{js_file_path}' not found")
            return

        with open(js_file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]

        for url in urls:
            if not self.is_valid_url(url):
                print(f"Invalid URL: {url}")
                continue
            try:
                response = self.session.head(url, timeout=5)
                if response.status_code == 200:
                    self.js_files.add(url)
                else:
                    print(f"Filtered out {url} (Status: {response.status_code})")
            except requests.RequestException:
                print(f"Filtered out {url} (Inaccessible)")

        while True:
            unprocessed_js = self.js_files - self.processed_urls
            if not unprocessed_js:
                break
            
            for js_file in unprocessed_js.copy():
                self.process_js_file(js_file)
            
            print(f"Found {len(self.js_files - self.processed_urls)} new JS files to process")

    def process_input(self, input_data: str, is_js_file: bool = False, is_js_list: bool = False):
        """Process either a single URL/file or a text file containing URLs"""
        if is_js_list:
            self.process_js_list(input_data)
        elif os.path.isfile(input_data) and not is_js_file:
            with open(input_data, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
            for url in urls:
                if not self.is_valid_url(url):
                    print(f"Invalid URL: {url}")
                    continue
                self.process_domain(url)
        else:
            url = input_data
            if not self.is_valid_url(url):
                print(f"Invalid URL: {url}")
                return
                
            if is_js_file:
                print(f"Processing JS file: {url}")
                try:
                    response = self.session.head(url, timeout=5)
                    if response.status_code == 200:
                        self.js_files.add(url)
                        self.process_js_file(url)
                    else:
                        print(f"Filtered out {url} (Status: {response.status_code})")
                except requests.RequestException:
                    print(f"Filtered out {url} (Inaccessible)")
            else:
                self.process_domain(url)

    def get_results(self) -> Dict:
        """Return the collected JS files and endpoints"""
        return {
            'js_files': sorted(list(self.js_files)),
            'endpoints': sorted(list(self.endpoints))
        }

def save_results(results: Dict, js_output: str = None, endpoint_output: str = None):
    """Save JS files and endpoints to separate files if specified, with prompt for JS if not provided"""
    # For console display, keep the dashes
    js_output_lines_display = ["Found JavaScript/JSON Files:"]
    js_output_lines_display.extend(f"- {js_file}" for js_file in results['js_files'])
    
    # For file saving, remove the dashes
    js_output_lines_file = [js_file for js_file in results['js_files']]
    
    if js_output:
        try:
            with open(js_output, 'w') as f:
                f.write('\n'.join(js_output_lines_file))  # Save without dashes
            print(f"JavaScript files saved to {js_output}")
        except Exception as e:
            print(f"Error saving JS files to {js_output}: {str(e)}")
    else:
        print('\n'.join(js_output_lines_display))  # Display with dashes
        if results['js_files']:
            while True:
                save_js = input("Do you want to save the extracted JS files? (yes/no): ").lower().strip()
                if save_js in ('yes', 'y'):
                    js_file_name = input("Enter the filename to save JS files: ").strip()
                    try:
                        with open(js_file_name, 'w') as f:
                            f.write('\n'.join(js_output_lines_file))  # Save without dashes
                        print(f"JavaScript files saved to {js_file_name}")
                        break
                    except Exception as e:
                        print(f"Error saving JS files to {js_file_name}: {str(e)}")
                elif save_js in ('no', 'n'):
                    break
                else:
                    print("Please enter 'yes' or 'no'")

    # Endpoints can keep the dashes (not used as input)
    endpoint_output_lines = ["Found Endpoints:"]
    endpoint_output_lines.extend(f"- {endpoint}" for endpoint in results['endpoints'])
    
    if endpoint_output:
        try:
            with open(endpoint_output, 'w') as f:
                f.write('\n'.join(endpoint_output_lines))
            print(f"Endpoints saved to {endpoint_output}")
        except Exception as e:
            print(f"Error saving endpoints to {endpoint_output}: {str(e)}")
    else:
        print('\n'.join(endpoint_output_lines))

def main():
    parser = argparse.ArgumentParser(
        description="Extract JS files and endpoints from websites or JS files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-d', '--domain',
        type=str,
        help='Single domain to process (e.g., https://example.com)'
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Text file containing list of domains to process'
    )
    parser.add_argument(
        '-js', '--javascript',
        type=str,
        help='Single JavaScript file URL to process'
    )
    parser.add_argument(
        '-jss', '--javascripts',
        type=str,
        help='Text file containing list of JavaScript file URLs to process'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file to save endpoints'
    )
    parser.add_argument(
        '-oj', '--js-output',
        type=str,
        help='Output file to save JS files'
    )
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    extractor = JSEndpointExtractor()
    
    if args.domain:
        print(f"Processing single domain: {args.domain}")
        extractor.process_input(args.domain)
        results = extractor.get_results()
        save_results(results, args.js_output, args.output)
        
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found")
            return
        print(f"Processing domains from file: {args.file}")
        extractor.process_input(args.file)
        results = extractor.get_results()
        save_results(results, args.js_output, args.output)
        
    elif args.javascript:
        print(f"Processing single JS file: {args.javascript}")
        extractor.process_input(args.javascript, is_js_file=True)
        results = extractor.get_results()
        save_results(results, args.js_output, args.output)
        
    elif args.javascripts:
        print(f"Processing JS files from file: {args.javascripts}")
        extractor.process_input(args.javascripts, is_js_file=True, is_js_list=True)
        results = extractor.get_results()
        save_results(results, args.js_output, args.output)

if __name__ == "__main__":
    main()