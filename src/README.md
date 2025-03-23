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
- ✅ Fully containerized (Docker)

---

## 🏗️ Project Structure

```
cv_parser/
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
git clone https://github.com/your-org/cv-fetcher.git
cd cv-fetcher
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
docker compose up -d db
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
    "id": "uuid",
    "name": "Senior Python Developer",
    "skills": "...",
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
Returns `application/pdf` file:
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

---

## 🐳 Docker

```bash
docker build -t cv-fetcher .
docker run -p 8000:8000 cv-fetcher
```

---

## 🧪 Testing

```bash
pytest
```

---

## 📄 License

MIT © Your Name