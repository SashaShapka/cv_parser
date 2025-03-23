import contextlib
import sqlalchemy.orm
from cv_fetcher.cv_db.singelton import Singleton, get_connection_string
from cv_fetcher.config import DB_NAME
from cv_fetcher.cv_db import models
from sqlalchemy import text



class CandidatestDB(metaclass=Singleton):

    def __init__(self, timeout=60, create_all=False):

        self.is_closed = False
        self.engine = sqlalchemy.create_engine(get_connection_string(DB_NAME))
        self.engine.pool_timeout = timeout
        self.SessionLocal = sqlalchemy.orm.sessionmaker(bind=self.engine)

        if create_all:
            models.Base.metadata.create_all(self.engine)
            self.create_trigger()

    def __del__(self):
        """
        Calls the close method
        """
        try:
            self.close()
        except Exception:
            pass

    def close(self):
        """
        Closes the connections and disposes the engine
        """
        if self.is_closed or self.engine is None:
            return

        self.engine.dispose()
        self.is_closed = True

    def create_trigger(self):
        with self.engine.begin() as conn:
            conn.exec_driver_sql("""
                CREATE OR REPLACE FUNCTION update_search_vector()
                RETURNS trigger AS $$
                BEGIN
                    NEW.search_vector := 
                        CASE
                            WHEN NEW.name ~ '[a-zA-Z]' OR NEW.skills ~ '[a-zA-Z]' OR NEW.experience ~ '[a-zA-Z]' THEN
                                to_tsvector('english', COALESCE(NEW.name, '') || ' ' || COALESCE(NEW.skills, '') || ' ' || COALESCE(NEW.experience, ''))
                            ELSE
                                to_tsvector('simple', COALESCE(NEW.name, '') || ' ' || COALESCE(NEW.skills, '') || ' ' || COALESCE(NEW.experience, ''))
                        END;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """)

            conn.exec_driver_sql("""
                DROP TRIGGER IF EXISTS update_candidates_search_vector ON candidates;
            """)

            conn.exec_driver_sql("""
                CREATE TRIGGER update_candidates_search_vector
                BEFORE INSERT ON candidates
                FOR EACH ROW
                EXECUTE FUNCTION update_search_vector();
            """)

    @property
    def session(self):
        """Returns a new session instance"""
        return self.SessionLocal()

    @contextlib.contextmanager
    def session_scope(self, to_commit=True):
        """Context manager for creating and using the SQL session"""
        session = self.SessionLocal(expire_on_commit=False)
        try:
            yield session
            if to_commit:
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def save(self, obj):
        """Add one object and commit"""
        session = self.session
        try:
            session.add(obj)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add_and_commit(self, *objects):
        """Add multiple objects and commit"""
        session = self.session
        try:
            for obj in objects:
                session.add(obj)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()