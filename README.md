# 🚀 Internship Automation using AI

An intelligent internship automation system that scrapes internships from Internshala, filters relevant opportunities, matches them against a candidate's resume using Google Gemini AI, stores results in Excel, and sends email notifications for the best matches.

---

## 📌 Project Overview

Finding internships manually every day is repetitive and time-consuming.

This project automates the entire process by:

- Scraping the latest internships
- Removing duplicates
- Filtering irrelevant roles
- Comparing internship skills with resume skills
- Using Gemini AI for semantic resume matching
- Ranking internships
- Saving results
- Sending email notifications

---

## ✨ Features

### 🔍 Internship Scraping

- Playwright based scraper
- Multi-page support
- Automatic retry
- Handles dynamic websites

---

### 🎯 Smart Filtering

- Duplicate removal
- Recent internship filtering
- Skill overlap filtering
- Quick keyword filtering
- AI title classification

---

### 🤖 AI Matching

Google Gemini is used for:

- Resume understanding
- Internship understanding
- Semantic matching
- Skill comparison
- Recommendation generation

---

### ⚡ Caching

Two caching systems reduce API usage:

- AI Match Cache
- Title Classification Cache

This greatly reduces Gemini API calls.

---

### 📧 Notifications

Automatically emails:

- Excellent Matches (90+)
- Strong Matches (75+)

If none exist:

- Top 5 internships by score

---

### 📊 Data Storage

Results are stored inside:

```
data/internships.xlsx
```

including:

- Match Score
- Skills
- Missing Skills
- Advice
- Company
- Stipend
- Apply Link

---

## 🏗 Architecture

```
Resume
   │
   ▼
Resume Parser
   │
   ▼
Internshala Scraper
   │
   ▼
Quick Filter
   │
   ▼
AI Title Classifier
   │
   ▼
Skill Overlap Filter
   │
   ▼
Gemini Resume Matcher
   │
   ▼
Cache
   │
   ▼
Excel Database
   │
   ▼
Email Notification
```

---

## 📂 Project Structure

```
Internship-Automation/

├── cache/
│   ├── ai_cache.py
│   └── title_cache.py
│
├── data/
│
├── logs/
│
├── resume/
│
├── config.py
├── config_local.py
├── career.py
├── email_sender.py
├── excel_manager.py
├── filters.py
├── logger.py
├── main.py
├── matcher.py
├── resume_engine.py
├── scraper.py
├── title_classifier.py
├── utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/nithinboddula15/Internship-Automation.git

cd Internship-Automation
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

Create

```
config_local.py
```

Example

```python
gemini_api_key="YOUR_API_KEY"
```

Update

```
config.py
```

with your:

- Resume path
- Email
- Password/App Password

---

## ▶ Usage

Run

```bash
python main.py
```

The automation will:

1. Load Resume
2. Load Previous Excel
3. Scrape Internshala
4. Remove duplicates
5. Filter internships
6. Match using AI
7. Save Excel
8. Send Email

---

## 📈 Example Output

```
Cards Seen          : 210
Duplicates          : 64
Quick Filter Reject : 98
Old Posts           : 18
Skill Reject        : 12
Cache Hits          : 25
Gemini Calls        : 16
New Internships     : 7
```

---

## 🛠 Technologies Used

- Python
- Playwright
- Google Gemini API
- Pandas
- OpenPyXL
- SMTP
- JSON
- Logging

---

## 📌 Future Improvements

- LinkedIn Support
- Indeed Support
- Wellfound Support
- PostgreSQL
- Streamlit Dashboard
- Telegram Notifications
- Resume Customization
- Cover Letter Generator
- One Click Apply
- Scheduler

---

## 🤝 Contributing

Contributions are welcome.

Feel free to fork the repository and create a pull request.

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Nithin Boddula**

B.Tech Computing & Data Science

Python • AI • Machine Learning • Automation

GitHub:
[Nithin Boddula](https://github.com/nithinboddula15)