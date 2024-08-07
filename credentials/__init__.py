import os

from l402.server.macaroons import MacaroonService, SqliteMacaroonService

def get_macaroon_service(db_type='sqlite') -> MacaroonService:
    if db_type == 'sqlite':
        return SqliteMacaroonService('data/credentials.db')
    
    elif db_type == 'postgresql':
        # import here to avoid psycopg2 dependency when using sqlite
        from l402.server.macaroons import PostgreSQLMacaroonService
        return PostgreSQLMacaroonService(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
    else:
        raise ValueError(f"Unsupported database type: {db_type}")