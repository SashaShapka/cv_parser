from abc import ABC, abstractmethod
from langdetect import detect
from sqlalchemy import text, select, and_
from cv_fetcher.config import QUERY_LIMIT
from cv_fetcher.cv_db.models import Candidates
from cv_fetcher.utils.logging import get_logger

logger = get_logger(__name__)



class MyCustomEmptyError(Exception):
    pass

class Check(ABC):
    @abstractmethod
    def set_next(self, check):
        pass

    @abstractmethod
    def check(self, db=None, split_query=None):
        pass



class AbstractCheck(Check):
    _next_check = None

    def set_next(self, check: Check):
        self._next_check = check
        return check

    @abstractmethod
    def check(self, db=None, split_query=None):
        if self._next_check:
            return self._next_check.check(db=db, split_query=split_query)


class FullTextSearch(AbstractCheck):
    def check(self, db=None, split_query=None):
        try:
            logger.info("Try to get with full test search")
            if not split_query:
                return []
            params = {}
            conditions = []

            for i, word in enumerate(split_query):
                try:
                    lang = detect(word)
                except Exception:
                    lang = 'en'

                lang_conf = 'simple' if lang == 'uk' else 'english'
                param_name = f"word{i}"
                condition = text(f"search_vector @@ to_tsquery('{lang_conf}', :{param_name})")
                conditions.append(condition)
                params[param_name] = word


            query = (
                select(
                    Candidates.id,
                    Candidates.name,
                    Candidates.skills,
                    Candidates.experience,
                    Candidates.source
                ).where(and_(*conditions))
                .limit(QUERY_LIMIT)
            )

            with db() as session:
                # result = session.execute(query, params).mappings().all()
                result = []
                if not result:
                    raise MyCustomEmptyError("Empty")
                logger.info("Full test search has completed")
                return result


        except Exception as e:
            if isinstance(e, MyCustomEmptyError):
                logger.info(f" FullTextSearch SQL execution failed: {e} go to Ilike search")
                return super().check(db=db, split_query=split_query)


class IlikeTextSearch(AbstractCheck):
    def check(self, db=None, split_query=None):
        try:
            logger.info("Try to get with ilike search")
            if not split_query:
                return []

            conditions = [
                Candidates.name.ilike(f"%{word}%") |
                Candidates.skills.ilike(f"%{word}%") |
                Candidates.experience.ilike(f"%{word}%")
                for word in split_query
            ]

            query = (
                select(
                    Candidates.id,
                    Candidates.name,
                    Candidates.skills,
                    Candidates.experience,
                    Candidates.source
                )
                .where(and_(*conditions))
                .limit(QUERY_LIMIT)
            )

            with db() as session:
                result = session.execute(query).mappings().all()
                if not result:
                    raise MyCustomEmptyError("Empty")
                logger.info("Ilike search has completed")
                return result
        except Exception as e:
            if isinstance(e, MyCustomEmptyError):
                logger.info(f" Ilike SQL execution failed: {e}")
                return []
