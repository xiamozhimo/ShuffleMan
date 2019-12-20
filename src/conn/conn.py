'''
Created on Sep 25, 2019

@author: tfu
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def createSession():
    engine = create_engine('mysql+mysqlconnector://tfu@azdbtony:##password##@azdbtony.mysql.database.azure.com:3306/pymyshuffler')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
