from fastapi import FastAPI

from cv_fetcher.cv_db.pull_data_db import parse_and_store
from cv_fetcher.cv_db.db import CandidatestDB
from cv_fetcher.routers import register_routes


app = FastAPI()
register_routes(app)

@app.on_event("startup")
def startup_load_data():
    CandidatestDB(create_all=True)
    register_routes(app)
    parse_and_store("https://jobs.dou.ua/vacancies/feeds/?category=Python")