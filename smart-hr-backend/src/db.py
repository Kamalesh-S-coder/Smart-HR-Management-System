import os
from prisma import Prisma
from dotenv import load_dotenv

load_dotenv() 

def get_db():
    # We are forcing Python to look at the exact file Prisma CLI created
    return Prisma(datasource={'url': 'file:./prisma/dev.db'})