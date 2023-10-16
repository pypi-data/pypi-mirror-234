import os
import psycopg2
import configparser
from sqlalchemy import create_engine

class Config:
    def __init__(self, database,host,user,password,port,schemas):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.schemas = schemas
        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}/{self.database}')

    def commit(self,query):
        connection = psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password, port=self.port)
        cur = connection.cursor()

        cur.execute(query)
        connection.commit()
        
        if connection:
            connection.close()

    def commit_many(self, query, values):
        connection = psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password, port=self.port)
        cur = connection.cursor()

        # Execute the query with multiple values
        cur.executemany(query, values)

        # Commit the changes
        connection.commit()

        # Close the cursor
        cur.close()
    
    def fetchall(self, query):
        connection = psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password, port=self.port)
        cur = connection.cursor()

        cur.execute(query)
        connection.commit()
        
        data = cur.fetchall()
        
        if connection:
            connection.close()

        return data

    def fetchone(self, query):
        connection = psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password, port=self.port)
        cur = connection.cursor()

        cur.execute(query)
        connection.commit()
        
        data = cur.fetchone()
        
        if connection:
            connection.close()

        return data
    
    def fetchmany(self, query):
        connection = psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password, port=self.port)
        cur = connection.cursor()

        cur.execute(query)
        connection.commit()
        
        data = cur.fetchmany()
        
        if connection:
            connection.close()

        return data

