import pandas as pd
from sqlalchemy import create_engine
import config

engine = create_engine(f'mysql+pymysql://{config.login}@localhost/bdasignment1')


def get_random_reviews(limit):
    results = pd.read_sql_query('CALL get_random_reviews(' + str(limit) + ')', con=engine)
    return pd.DataFrame(results, columns=['review', 'total_words', 'positive'])


def get_reviews(limit):
    results = pd.read_sql_query('CALL get_reviews(' + str(limit) + ')', con=engine)
    return pd.DataFrame(results, columns=['review', 'total_words', 'positive'])
