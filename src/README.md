# CV Fetcher Service

A FastAPI-based microservice for parsing and storing candidate data, full-text search, and generating downloadable PDF resumes.

---

## 🚀 Features

- ✅ Parse RSS job feeds (e.g., from DOU)
- ✅ Store candidate data in PostgreSQL
- ✅ Full-text search with PostgreSQL `tsvector`
- ✅ Fallback search using `ILIKE`
- ✅ Generate PDF resume with Arial font and Cyrillic support
- ✅ Clean architecture: service, models, routing

---

## 🏗️ Project Structure

```
cv_parser/
├──venv
├── src/
│   └── cv_fetcher/
│       ├── apis/              # FastAPI endpoints
│       ├── cv_db/             # DB models and session management
│       ├── pdf_export/        # PDF generation logic
│       ├── routers/           # Router entry point
│       ├── utils/             # Logging, config helpers
│       ├── app.py             # FastAPI app instance
│       ├── __main__.py        # Entrypoint for `python -m`
│       └── config.py          # App settings
├── requirements.txt
└── README.md
```

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/SashaShapka/cv-fetcher.git

```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start PostgreSQL (or use Docker):
```bash
cd cv-fetcher
docker compose up -d
```

5. Run the app:
```bash
cd src
python -m cv_fetcher
```

---

## 🔍 Endpoints

### `POST /submit_query`

Search candidates by keywords using full-text or fallback strategy.

#### Request body:
```json
{ "query": "Python Senior" }
```

#### Response:
```json
[
{
    "id": "9d50dd12-66c5-497d-8c5c-02efc7f821fe",
    "name": "Senior Python engineer (#2971) в N-iX, Київ, Львів, Дніпро, Вінниця, Івано-Франківськ, Тернопіль, віддалено",
    "skills": "For our customer author of the most widely used solution to recover digital revenue, we are looking for a Senior Python Engineer. Over 1.000 companies rely on their platform to fight counterfeits, piracy, impersonation, and distribution abuse. Company has 270+ professionals and offices in New York, Barcelona, Beijing, and Salt Lake City. Red Points’ platform utilizes Artificial Intelligence (AI) to automatically detect and remove IP infringements online 24/7. Through automation rules or just one click on a validation card, our technology can enforce intellectual property rights and remove issues from global online marketplaces, social media networks, websites and other online channels.The roleWe are looking for a Python Engineer to get involved in our tracking technology, libraries, and hundreds of projects that use them, helping us maintain our platform, optimize it, and further improve it.Responsibilities:Your day to day will be divided between writing good Python and idiomatic code, reviewing pull requests from other team members, debugging complex problems, and also participating in decision-making processes. That is, contributing with your experience in software architecture and design.Requirements:4+ years in a Python Developer position or similarThe ability to express complex ideas in spoken and written English is crucial as our team is made up of people of 5 different nationalities and it is the language in which we communicateGood knowledge of Python, with the ability to write idiomatic and reusable code.Experience in object-oriented design, software architecture best practices and patterns, and large-scale application development with maintainability and extensibility in mind.Experience with web requests and Python request library.Experience with TDD, testing best practices and methodologies: pytest, unittest, mock and answers libraries.Experience using docker / docker-compose throughout the entire lifecycle, including development, testing, debugging, QA, CI, and deployment. Experience working in the Agile environment (we use Kanban board) Tech stack:Python, AWS, MySQL / SQLAlchemy, Snowflake / Redshift Airflow / Celery / RabbitMQ / Luigi, Redis, Scrapy, IDOL for data interfaces and schema, Sepia config systemNice to have: Understanding of the architecture of web applications (including ajax websites) and mastery of the development tools built into the browser, for reverse engineering purposes.Inclination towards code optimizations (algorithmic complexity, memory usage).Proficiency in contributing to shared code bases using git.Efficient text processing with regular expressions and XML parsing.Experience with selenium / nodejs / phantomjs / splash or any similar software for scraping or automation purposes.  We offer:Flexible working format — remote, office-based or flexibleA competitive salary and good compensation packagePersonalized career growthProfessional development tools (mentorship program, tech talks and trainings, centers of excellence, and more)Active tech communities with regular knowledge sharingEducation reimbursementMemorable anniversary presentsCorporate events and team buildingsOther location-specific benefits\n\n\n\n\n\n\n\tВідгукнутись на вакансію",
    "experience": "4 years",
    "source": "dou.ua"
  }
]
```

---

### `POST /generate-cv`

Generate and return a PDF resume.

#### Request body:
```json
{ "candidate_id": "uuid" }
```

#### Response:
Returns `resume_Senior_Python_engineer_(#2971)_в_N-iX,_Київ,_Львів,_Дніпро,_Вінниця,_Івано-Франківськ,_Тернопіль,_віддалено.pdf` file:
```
Content-Disposition: attachment; filename=resume_Senior_Developer.pdf
```

---

## 🖨️ PDF Styling

- Font: **Arial** (.ttf embedded)
- Font size: `12pt`
- Cyrillic support
- Wrapped long lines
- Bolded headers for Skills, Experience, Source
