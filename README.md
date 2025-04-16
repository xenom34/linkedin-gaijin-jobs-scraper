# LinkedIn Gaijin Jobs Scraper

An intelligent tool for finding foreign-friendly job listings on LinkedIn in Japan.

## 📋 Description

This project automatically collects job listings from LinkedIn and analyzes their compatibility with foreign workers in Japan. The tool uses advanced text analysis to detect job listings that don't require Japanese language skills, offer visa support, and provide an international work environment.

## ✨ Features

- **Automated scraping** of job listings from LinkedIn
- **Intelligent analysis** to evaluate if a job is suitable for foreigners:
  - Detection of Japanese language requirements
  - Evaluation of international work environment
  - Analysis of expat benefits (visa, housing, etc.)
  - Review of leave policies
  - Detection of language used in the listing
- **Report generation** in multiple formats:
  - CSV export with all data
  - Formatted and filterable Excel export
  - Interactive HTML report with visualizations
- **Detailed logging** for debugging and process tracking
- **Flexible parameters** via command-line arguments
- **Multilingual support** (English and French)

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- Firefox browser (used by Selenium)

### Installation Steps

1. Clone this repository:
```bash
git clone https://github.com/your-username/linkedin-gaijin-jobs-scraper.git
cd linkedin-gaijin-jobs-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file at the root of the project with your LinkedIn credentials:
```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

## 🚀 Usage

### Running the Main Script

```bash
python linkedin_scraper.py
```

The script will:
1. Log in to LinkedIn with your credentials
2. Search for jobs according to the configured criteria
3. Analyze each job to determine if it is suitable for foreigners
4. Export the results in different formats

### Command Line Options

You can customize the execution with the following options:

```bash
python linkedin_scraper.py --pages 10 --keywords "Data Engineer,Machine Learning,AI" --location "Osaka, Japan" --language en
```

| Option | Description | Default Value |
|--------|-------------|-------------------|
| `--pages` | Number of pages to scrape | 5 |
| `--keywords` | Search keywords (comma-separated) | Technical Consultant,Software Consultant,Professional Services |
| `--location` | Search location | Tokyo, Japan |
| `--language`, `-l` | Application language (en: English, fr: French) | en |

### Advanced Customization

For more advanced modifications, you can directly edit the source code. The main configuration functions are located in the `main()` function of the `linkedin_scraper.py` file.

## 📊 Results

The results are exported to the `exports/` folder in different formats:

- **CSV**: Raw data for analysis
- **Excel**: Formatted table with conditional formatting
- **HTML**: Interactive report with charts and filters

Each job contains the following information:
- Job title
- Company
- Location
- Job URL
- "Gaijin-friendly" compatibility score
- Detailed scores by category
- Detected leave days
- Expatriate benefits

## 🧩 Project Structure

- `linkedin_scraper.py`: Main script for scraping and analysis
- `linkedin_export.py`: Module for exporting data in different formats
- `requirements.txt`: List of dependencies
- `exports/`: Folder containing exported files

## ⚙️ How It Works

The analysis of job listings is based on a multi-criteria scoring system:

1. **Analysis of Japanese language requirements** (detects mentions of JLPT, "native level", etc.)
2. **Evaluation of international environment** (mentions of international team, working language, etc.)
3. **Analysis of expatriate benefits** (visa, housing, etc.)
4. **Review of leave policies** (leave days, flexibility, etc.)
5. **Detection of language** used in the listing (an English listing is generally more suitable)

Each criterion contributes to an overall score that determines if the job is "gaijin-friendly".

## 🛡️ Legal Disclaimer

This project is designed for educational and personal purposes only. The use of this script must comply with LinkedIn's terms of use. Excessive use may result in limitations on your LinkedIn account. Use responsibly by respecting reasonable time delays between requests.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 