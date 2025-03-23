import re

from fastapi import HTTPException
from starlette.responses import StreamingResponse
from urllib.parse import quote
from cv_fetcher.apis.api_schemas.schemas import QueryRequest, GenerateCvRequest
from cv_fetcher.apis.chain import FullTextSearch, IlikeTextSearch
from cv_fetcher.pdf_export.pdf_export import PdfGenerator
from cv_fetcher.cv_db.db import CandidatestDB
from cv_fetcher.cv_db.models import Candidates


async def submit_query(request: QueryRequest):
    db = CandidatestDB().session_scope
    cleaned_query = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', request.query)
    split_query = [word for word in cleaned_query.split() if len(word) > 1]

    if not split_query:
        raise HTTPException(status_code=400, detail="Query must contain words longer than one letter")

    full_text_search = FullTextSearch()
    ilike_text_search = IlikeTextSearch()
    full_text_search.set_next(ilike_text_search)
    res = full_text_search.check(db=db, split_query=split_query)
    return res

async def generate_cv(request: GenerateCvRequest):
    db = CandidatestDB().session_scope

    with db() as session:
        candidate = session.query(Candidates).filter_by(id=request.candidate_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

    buffer = PdfGenerator.generate(candidate)
    filename = f"resume_{candidate.name.replace(' ', '_')}.pdf"
    encoded_filename = quote(filename)

    return StreamingResponse(buffer, media_type="application/pdf",  headers={
    "Content-Disposition": f"attachment; filename=resume.pdf; filename*=UTF-8''{encoded_filename}"
    })
