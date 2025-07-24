
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from logging import getLogger
from .schemas import Base

class Postgres:
    def __init__(
        self,
        username: str,
        database_name: str,
        password: str,
        host: str,
        port: int
    ) -> None:
        database_url = self.create_database_url(
            username, database_name,
            password, host, port
        )
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=900,
            pool_timeout=5,
            echo_pool=None,
            echo=None
        )
        self.sessionmaker = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )
        Base.metadata.create_all(bind=self.engine)
        self.logger = getLogger('postgres')
        self.ignored_exceptions = ('HTTPException', 'StarletteHTTPException')

    @staticmethod
    def create_database_url(
        username: str,
        database_name: str,
        password: str,
        host: str,
        port: int
    ) -> str:
        safe_username = quote_plus(username)
        safe_password = quote_plus(password)
        safe_database_name = quote_plus(database_name)
        return f'postgresql://{safe_username}:{safe_password}@{host}:{port}/{safe_database_name}'

    @contextmanager
    def session(self):
        session = self.sessionmaker(bind=self.engine)
        try:
            yield session
        except Exception as e:
            exception_name = e.__class__.__name__

            if exception_name in self.ignored_exceptions:
                raise e

            self.logger.fatal(f'Transaction failed: {e}', exc_info=e)
            self.logger.fatal('Performing rollback...')
            session.rollback()
            raise
        finally:
            session.close()

    def ping(self) -> bool:
        try:
            with self.session() as session:
                session.execute('SELECT 1')
            return True
        except Exception as e:
            self.logger.error(f'Ping failed: {e}', exc_info=e)
            return False
