Below is the GitHub README for Xtract, written with proper Markdown formatting (e.g., bold headers, code blocks, tables) so that it renders correctly when copied and pasted into GitHub.
markdown
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
   git clone https://github.com/yourusername/Xtract.git
   cd Xtract
Install dependencies:
bash
pip install -r requirements.txt
Or manually:
bash
pip install requests beautifulsoup4
Ensure the script (xtract.py) is in your working directory.
Usage
Run Xtract with command-line arguments to process domains or JS files.
Command-Line Options
Option
Description
Example
-d, --domain
Process a single domain
-d https://example.com
-f, --file
Process a list of domains from a text file
-f domains.txt
-js, --javascript
Process a single JS file URL
-js https://example.com/main.js
-jss, --javascripts
Process a list of JS URLs from a text file
-jss jsfiles.txt
-o, --output
Output file for endpoints
-o endpoints.txt
-oj, --js-output
Output file for JS files
-oj jsfiles.txt
Examples
Extract from a single domain:
bash
python xtract.py -d https://example.com -oj jsfiles.txt -o endpoints.txt
Saves JS files to jsfiles.txt and endpoints to endpoints.txt.
Process a list of domains:
bash
python xtract.py -f domains.txt
domains.txt should contain one URL per line (e.g., https://example.com).
Analyze a single JS file:
bash
python xtract.py -js https://example.com/scripts/main.js
Process a list of JS files:
bash
python xtract.py -jss jsfiles.txt
jsfiles.txt should contain one JS URL per line.
Interactive mode:
bash
python xtract.py -d https://example.com
Prints results and prompts to save JS files.
Output Format
Console:
Found JavaScript/JSON Files:
- https://example.com/scripts/main.js
- https://example.com/scripts/extra.js
Found Endpoints:
- https://example.com/api/users
JS File Output (e.g., jsfiles.txt):
https://example.com/scripts/main.js
https://example.com/scripts/extra.js
Endpoint File Output (e.g., endpoints.txt):
Found Endpoints:
- https://example.com/api/users
How It Works
Initialization: Sets up a requests session with a browser-like User-Agent.
JS Extraction: Parses HTML for <script src="..."> tags or scans JS files for references.
Endpoint Extraction: Uses regex to find patterns like /api/... in JS content.
Recursion: Continuously processes newly discovered JS files until none remain.
Results: Saves JS files as a plain list and endpoints with formatting.
Requirements File
Create a requirements.txt with:
requests
beautifulsoup4
Contributing
Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments
Built with Python, leveraging requests and BeautifulSoup.
Inspired by web scraping and security research tools.

---

### How It Renders on GitHub
- **`# Xtract`**: Bold, large header.
- **`## Features`**: Bold, slightly smaller headers for sections.
- Code blocks (```bash``` and ```): Properly formatted commands and file content.
- Table (`| Option | Description | Example |`): Neatly aligned command-line options.
- Lists (`-`): Bulleted items for features and steps.

### Instructions
1. Save this as `README.md` in your repository root.
2. Replace `yourusername` in the `git clone` URL with your actual GitHub username.
3. If you use a different script name (not `xtract.py`), update the references accordingly.

This will display beautifully on GitHub with all formatting intact. Let me know if you need adjustments!
