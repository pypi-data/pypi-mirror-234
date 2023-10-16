
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

PROVIDER = "mssql"
DB_API = "pyodbc"
USERNAME = "msat7201"
PASSWORD = "Among7201"
HOST = "118.168.138.36"
PORT = 1433
DATABASE = "test"
DRIVER = "ODBC Driver 17 for SQL Server"
TRUST_SERVER_CERTIFICATE = "yes"


engine = create_engine(
    URL.create(
        f"{PROVIDER}+{DB_API}",
        username=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE,
        query={
            "driver": DRIVER,
            "TrustServerCertificate": TRUST_SERVER_CERTIFICATE,
        },
    )
)
