import logging
import re

import jieba
from whoosh import sorting
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser


class Query:
    def __init__(self, mydir=None):
        jieba.setLogLevel(logging.INFO)
        if mydir is None:
            self.index = open_dir('./index')
        else:
            self.index = open_dir(mydir)
        self.searcher = self.index.searcher()

    def search(self, parameter):
        # 提取查询字段，创建检索器
        keys = parameter['keys']
        parser = None
        if len(keys) == 1:
            parser = QueryParser(keys[0], schema=self.index.schema)
        elif len(keys) > 1:
            parser = MultifieldParser(keys, schema=self.index.schema)
        # 搜索参数（排序、分页）
        # score = sorting.ScoreFacet() # 相关度
        id = sorting.FieldFacet('id', reverse=False) # 标题字段
        _limit = None # 分页限制
        if 'page' in parameter and 'pagesize' in parameter:
            page = parameter['page']
            pagesize = parameter['pagesize']
            if page > 0 and pagesize != 0:
                _limit = page * pagesize
        # 执行搜索
        query = parser.parse(parameter['keywords'])
        result = self.searcher.search(
            query,
            limit=_limit,
            sortedby=[id]
        )
        # 返回结果
        res = list()
        for hit in result:
            res.append({
                'title': hit['title'],
                'url': hit['url'],
                'content':  re.sub(r'<[^>]+>', ' | ', hit.highlights('content'), re.S)
            })
        return res

    def standard_search(self, query):
        parameter = {
            'keys': ['title', 'content'],
            'keywords': query,
            'page': 10,
            'pagesize': 10
        }
        return self.search(parameter)

    def regex_extract(self, query):
        result = self.standard_search(query)
        adjPattern = re.compile(r'([\u4e00-\u9fa5]{2})的 \| ' + query, re.S)
        posPattern = re.compile(r'([\u4e00-\u9fa5]{2})(上|之上|内)', re.S)
        agePattern = re.compile(r'([\u4e00-\u9fa5]{2})岁', re.S)
        timePattern = re.compile(r'([\u4e00-\u9fa5]{2})时', re.S)
        res = list()
        for r in result:
            adjs = adjPattern.findall(r['content'])
            poss = posPattern.findall(r['content'])
            ages = agePattern.findall(r['content'])
            times = timePattern.findall(r['content'])
            res.append({
                'adjs': adjs,
                'poss': poss,
                'ages': ages,
                'times': times,
                'wdN': r['content'].count(query)
            })
        return res

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.searcher.close()


if __name__ == '__main__':
    res = Query().standard_search('厉害')
    for i in res:
        print(i)