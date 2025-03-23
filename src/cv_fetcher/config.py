from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8080



SETTINGS = Settings()

DB_NAME = "mydb"
TEST_DB_NAME = "passport_office_test"
USER = "myuser"
TEST_USER = "test_sysadmin"
PASSWORD = "mypassword"
HOST = "localhost"
PORT = 5432
LIMIT = 15
QUERY_LIMIT = 5

# DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/create_db.sh'
# TEST_DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/test_db.sh'
# DROP_DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/drop_db.sh'
# DROP_TEST_DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/test_db_drop.sh'