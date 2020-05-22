import sqlite3
import pysnooper


class GoodsManager(object):
    def __init__(self,id,name,price):
        self.id=id
        self.name=name
        self.price=price


    @pysnooper.snoop()
    def getallgoods_db(self):
            '''查询所有商品'''
            conn = sqlite3.connect('atm.db')
            cmd = "select ID,name,price from goods"
            message = conn.execute(cmd)
            good_list = list()
            for info in message:
                good_list.append(info)
            conn.commit()
            conn.close()
            return good_list

    @pysnooper.snoop()
    def print_goods_list(self,goods_list):
        _goodlist = goods_list
        title = "%-12s|%-10s|%40s|%15s" % ("商品序号", "商品编号", "商品名称", "商品价格")
        print(title)
        print('%s' % '-' * 95)

        for index, info in enumerate(_goodlist, start=1):
            line = "%-12s|%-12s|%42s|%17s" % (index,info[0], info[1], info[2])
            print(line)
        print("-" * 100)
