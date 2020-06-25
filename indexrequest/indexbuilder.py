from settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_SHEETNAME
import pymongo
import jieba
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
import os
import logging

class IndexBuilder:
    def __init__(self):
        # 获取数据库光标
        client = pymongo.MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT
        )
        db = client[MONGODB_DBNAME]
        self.post = db[MONGODB_SHEETNAME]

    def build_index(self):
        jieba.setLogLevel(logging.INFO)
        analyzer = ChineseAnalyzer()
        # 创建索引模板
        schema = Schema(
            id = NUMERIC(stored=True),
            title = TEXT(stored=True, analyzer=analyzer),
            url = ID(stored=True),
            content = TEXT(stored=True, analyzer=analyzer)
        )
        # 创建索引文件，在[index/]下
        path = os.path.dirname(__file__) + "/index"
        if not os.path.exists(path):
            os.mkdir(path)
            index = create_in(path, schema)
        else:
            index = open_dir(path)
        # 构建索引，增加需要索引的内容
        writer = index.writer()
        total_row = self.post.count_documents({})
        false_row = self.post.count_documents({'indexed':False})
        indexed_row = total_row - false_row
        while True:
            row = self.post.find_one({'indexed':False})
            if row is None:
                writer.commit()
                print('\n\tindexed successfully.')
                break
            else:
                writer.add_document(
                    id = (total_row+1) if (row['id']==-1) else row['id'],
                    title = row['title'],
                    url = row['url'],
                    content = row['content']
                )
                self.post.update_one(
                    {'title':row['title']},
                    {'$set':{'indexed':True}}
                )
                writer.commit()
                writer = index.writer()
                indexed_row += 1
                print(f"\rIndexing: {'▉' * (int(indexed_row/total_row*100//2))} {indexed_row/total_row*100:.2f}%", end='')


if __name__ == '__main__':
    IndexBuilder().build_index()