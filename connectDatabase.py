#!/usr/bin/python
import psycopg2
from config import config


class Connect:


    global cur


    def __init__(self):

        conn = None
        try:
            params = config()

            conn = psycopg2.connect(**params)

            self.cur = conn.cursor

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        print('Conexão finalizada!')

        del self