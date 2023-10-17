import argparse
from datetime import datetime


# def main(args):
#     print(f"argument mode is {args.mode}")
#     print(datetime.now().strftime('%Y-%m-%d'))



# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='tmp')
#     parser.add_argument('--mode', default="dev", choices=['dev', 'pro'],help="running mode")
#     args = parser.parse_args()
#     main(args=args)



from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, func,TIMESTAMP
engine = create_engine('mysql+pymysql://rpaer:Rpaer2023!@192.168.6.253:3306/rpa_data?charset=utf8mb4')
metadata = MetaData()
new_table = Table('new_table', metadata,
    Column('id', Integer, primary_key=True),
    Column('update_at', TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
)
# 创建表
metadata.create_all(engine)

from sqlalchemy.sql import insert
def insert_data(table, data):
    """
    Inserts data into a table.
    
    :param table: The table to insert data into.
    :param data: A dictionary where the keys are the column names and the values are the data to insert.
    """
    with engine.connect() as connection:
        stmt = insert(table).values(data)
        connection.execute(stmt)
# 使用insert_data函数插入数据
insert_data(new_table, {'id': 1})