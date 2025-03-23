from typing import List

from fastapi import APIRouter

from cv_fetcher.apis.api_schemas.schemas import QueryRequest, QueryResponse

router = APIRouter()

def register_routes(app):
    app.include_router(router)


from cv_fetcher.apis.apis import submit_query, generate_cv

router.add_api_route("/submit_query", submit_query, methods=["POST"], response_model=List[QueryResponse])
router.add_api_route("/genrate-cv", generate_cv, methods=["POST"])
