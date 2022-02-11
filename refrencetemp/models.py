import datetime
import os

from decouple import config
from sqlalchemy.sql import text

from refrencetemp.database import SessionLocal


def insert_object(data=None):
    # data = { "frame_no": "The Hobbit", "video_name": "Tolkien", 'ocr_object':'umer'}
    if data is None:
        print("data is missing to inesrt")
        # return
    print(data)

    statement = text(
        """INSERT INTO freelancedb.skills
        (id, name)
        VALUES(:id, :name);"""
    )

    sess = SessionLocal()
    with sess.connection() as connection:
        with connection.begin():
            try:
                connection.execute(statement, data)
                print("please wait inserting frames")

                # return True
            except:
                print("db connection not build / insertion failed")
                # return False
