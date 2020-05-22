import Atm
import menutemplate
import pysnooper
import Shopping


class View(object):


    def shop(self,atmobj):
        shopcart=Shopping.shopping()
        while True:
           view = menutemplate.Menupage()
           view.shopping()
           try:
               Num = int(input('请输入您本次的操作序号:\n'))
           except (IOError, ValueError):
               print('------------------------------')
               print('输入错误,请重新输入.')
               continue

           if Num == 1:
              shopcart.print_goods_list()

           elif Num==2:
               shopcart.edit()

           elif Num==3:
               shopcart.delete()

           elif Num == 4:
               # 查看购物车
               shopcart.print_shopcart_list(shopcart.shopping_cart)
               print("当前购物车共有 {0} 件商品,合计 {1} 元 !".format(len(shopcart.shopping_cart),shopcart.shopping_cost))
               continue

           elif Num==5:
                shopcart.payfor_shopcart(atmobj.idman)


           else:
               print('------------------------------')
               print('输入错误,请重新输入.')
               continue
           print('------------------------------')



    @pysnooper.snoop()
    def after_logging(self, idman):
        atm= Atm.AtmManager()
        while True:
           view = menutemplate.Menupage()
           view.FunctionView()
           try:
               select = int(input('请输入您本次的操作序号:\n'))
           except (IOError, ValueError):
               print('------------------------------')
               print('输入错误,请重新输入.')
               continue


           if select == 1:
               atm.CreatUser()

           elif select == 2:
               atm.select_db(idman)

           elif select == 3:
               user_money = float((input('请输入您取出的金额:\n')))
               atm.withdraw(user_money,idman)

           elif select == 4:
               user_money = float(input('请输入您存入的金额:\n'))
               atm.wallet(user_money,idman)

           elif select==5:
               other_ID = input('请输入对方账号:\n')
               turn_money = float(input('请输入转账金额:\n'))
               atm.transfer_accounts(idman,other_ID,turn_money)

           elif select==0:
                break


           else:
               print('------------------------------')
               print('输入错误,请重新输入.')
               continue
           print('------------------------------')