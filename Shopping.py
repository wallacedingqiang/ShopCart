import sqlite3
import pysnooper
import Atm


class shopping():
    def __init__(self):
        # 存放购物车列表
        self.shopping_cart = []
        # 购物总费用
        self.shopping_cost = 0
        # 数据表中所有商品信息
        self.shop_market = list()
        # 购物商城欢迎菜单
        self.welcome_menu = ""

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
    def print_goods_list(self):
        _goodlist = self.getallgoods_db()
        title = "%-12s|%-10s|%40s|%15s" % ("商品序号", "商品编号", "商品名称", "商品价格")
        print(title)
        print('%s' % '-' * 95)
        for index, info in enumerate(_goodlist, start=1):
            line = "%-12s|%-12s|%42s|%17s" % (index,info[0], info[1], info[2])
            print(line)
        print("-" * 100)

        self.add(_goodlist)


    @pysnooper.snoop()
    def add(self,goods_list):
        # 开始选择商品，添加到购物车
        choose_goods_flag = True
        while choose_goods_flag:
            repository_goods = list(goods_list)
            code = int(input("选择商品编号,加入购物车(q返回上一级): ").strip().lower())
            if code > len(repository_goods): continue
            # 返回上一级
            if code == "q":
                choose_goods_flag = False
                continue
            else:
                goodsid = repository_goods[code - 1][0]
                name = repository_goods[code - 1][1]
                price = repository_goods[code - 1][2]
                number = int(input("请输入购买数量:\n"))
                amount = price * number
                self.shopping_cart.append([goodsid, name, price, number, amount])
                self.print_shopcart_list(self.shopping_cart)
                print("已将商品加入购物车!")

                # 是否继续添加
                nextflag = False
                while not nextflag:
                    donext = input("继续购物(y) or 返回上一级(q):").strip().lower()
                    if donext == "y":
                        break
                    elif donext == "q":
                        choose_goods_flag = False
                        break
                    else:
                        continue

    @pysnooper.snoop()
    def print_shopcart_list(self,shop_list):
        print("=" * 100)
        # 如果清单不为空的时候，输出清单的内容
        if not shop_list:
            print("还未购买商品")
        else:
            title = "%-5s|%15s|%40s|%10s|%4s|%10s" % \
                    ("ID", "商品编号", "商品名称", "单价", "数量", "小计")
            print(title)
            # 记录总计的价钱
            sum = 0
            # 遍历代表购物清单的list列表
            for i, item in enumerate(shop_list):
                # 转换id为索引加1
                id = i + 1
                sum = sum + item[4]
                self.shopping_cost=sum
                line = "%-5s|%17s|%40s|%12s|%6s|%12s" % \
                       (id, item[0], item[1], item[2], item[3], item[4])
                print(line)
            print("                                                                                        总计: ", sum)
        print("=" * 100)
        # 添加购买商品，就是向代表用户购物清单的list列表中添加一项。

    def edit(self):
        id = input("请输入要修改的购物明细项的ID:\n")
        # id减1得到购物明细项的索引
        index = int(id) - 1
        # 根据索引获取某个购物明细项
        item = self.shopping_cart[index]
        # 提示输入新的购买数量
        number = input("请输入新的购买数量:\n")
        # 修改item里面的number
        item[3] = int(number)
        #修改item里面的amount
        amount = item[2] * item[3]
        item[4]=float(amount)
        self.print_shopcart_list(self.shopping_cart)

    # 删除购买的商品明细项，就是删除代表用户购物清单的list列表的一个元素。
    def delete(self):
        id = input("请输入要删除的购物明细项的ID: ")
        index = int(id) - 1
        # 直接根据索引从清单里面删除掉购物明细项
        del self.shopping_cart[index]
        self.print_shopcart_list(self.shopping_cart)


    def payfor_shopcart(self, idman):
        nowatm=Atm.AtmManager()
        user_money_tuple = nowatm.select_db(idman)
        user_money = float(user_money_tuple[0])
        print("账户余额为：", user_money)