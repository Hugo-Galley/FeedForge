import logging
import os

import pymysql
from EasyWorkEnv import Config
import colorlog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configFiles.models import Base

CONFIG = Config("variables.json")


def config_bdd():
    connection = pymysql.connect(
        host=CONFIG.Bdd.Host,
        user=CONFIG.Bdd.User,
        password=CONFIG.Bdd.Password,
        port=int(CONFIG.Bdd.Port),
        charset="utf8mb4"
    )
    
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{CONFIG.Bdd.Database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()  
    
    connection.close()

    engine = create_engine(
        f"mysql+pymysql://{CONFIG.Bdd.User}:{CONFIG.Bdd.Password}@{CONFIG.Bdd.Host}:{CONFIG.Bdd.Port}/{CONFIG.Bdd.Database}?charset=utf8mb4"
    )
    
    Base.metadata.create_all(bind=engine)
    
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    return db


db = config_bdd()

def setup_log():

    os.makedirs("log", exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
    )

    file_handler = logging.FileHandler(CONFIG.Log.FileDestination, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.propagate = False

    uvicorn_acces_logger = logging.getLogger("uvicorn_acces")
    uvicorn_acces_logger.setLevel(logging.INFO)

    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)