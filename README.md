# **Xtract**

A Python tool to extract JavaScript/JSON files and API endpoints from websites or JavaScript files. Xtract recursively discovers JS files, extracts potential API endpoints using regex patterns, and saves the results in a reusable format.

## **Features**
- Extract JS/JSON files from HTML pages or existing JS files.
- Identify API endpoints (e.g., `/api/users`) from JS content.
- Process single URLs, JS files, or lists of either via command-line arguments.
- Save results to files:
  - JS files as a plain list (one URL per line) for easy reuse.
  - Endpoints with a readable format.
- Interactive prompt to save JS files if no output file is specified.
- Handles errors gracefully with detailed logging.

## **Installation**

### **Prerequisites**
- Python 3.6+
- Required libraries: `requests`, `beautifulsoup4`

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/Hun33er/Xtract.git
   cd Xtract

### **Install dependencies:**
pip install -r requirements.txt

**Or manually:**

pip install requests beautifulsoup4

Ensure the script (xtract.py) is in your working directory.
Usage
Run Xtract with command-line arguments to process domains or JS files.

## **License**
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments
Built with Python, leveraging requests and BeautifulSoup.
Inspired by web scraping and security research tools.

### **Command-Line Options**

| Option              | Description                                     | Example                          |
|---------------------|-------------------------------------------------|----------------------------------|
| `-d, --domain`      | Process a single domain                         | `-d https://example.com`         |
| `-f, --file`        | Process a list of domains from a text file      | `-f domains.txt`                 |
| `-js, --javascript` | Process a single JS file URL                    | `-js https://example.com/main.js`|
| `-jss, --javascripts` | Process a list of JS URLs from a text file   | `-jss jsfiles.txt`               |
| `-o, --output`      | Output file for endpoints                       | `-o endpoints.txt`               |
| `-oj, --js-output`  | Output file for JS files                        | `-oj jsfiles.txt`                |
