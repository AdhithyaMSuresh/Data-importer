import psycopg2
import logging

class Database:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS public.phone (
            phoneid TEXT PRIMARY KEY,
            phone_name TEXT,
            phone_data JSONB
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def insert_phone_data(self, phone_id, phone_name, phone_data):
        query = """
        INSERT INTO public.phone (phoneid, phone_name, phone_data)
        VALUES (%s, %s, %s)
        ON CONFLICT (phoneid) DO NOTHING;
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (phone_id, phone_name, phone_data))
            self.conn.commit()
