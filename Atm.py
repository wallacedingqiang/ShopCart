import sqlite3
import common
import card
import Users
import pysnooper
import menutemplate
import ViewManage


class AtmManager():

    def __init__(self):
        self.idman = ""  # 登录的用户卡号

    @pysnooper.snoop()
    def login(self):
        """登录功能"""
        viewcontrol= ViewManage.View()
        self.idman=input("请输入身份证号:")
        password=input('请输入密码:')
        if common.validate_logon(self.idman, password):  # 检查账户密码是否一致
           print("欢迎您，%s用户" % (self.idman))
           viewcontrol.after_logging(self.idman)  # 跳转用户功能界面
        else:
            print("用户名密码错误")

    @pysnooper.snoop()
    #创建用户
    def CreatUser(self):
        name=input("请输入姓名")
        idman=input("请输入身份证号")
        phone=input("请输入电话号码")
        premoney=int(input("请输入预存金额"))
        if premoney<0:
            print("输入预存金额有误，开户失败")
            return -1
        password=input("请输入密码")
        #生成卡号
        cardId=common.createCardId()

        #存放数据库
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        cmd = "INSERT INTO USERS (NAME,PASSWORD,idman,phone,cardid,MONEY) VALUES ('{}',\"{}\",\"{}\",{},\"{}\",{})".format(name,password,idman,phone,cardId,premoney) # 将用户输入的信息写入数据库
        conn.execute(cmd)  # 写入数据到数据库
        conn.commit()  # 提交
        conn.close()  # 关闭数据库链接
        print("开户成功，请牢记卡号(%s)" %cardId)


    @pysnooper.snoop()
    def select_db(self,idman):
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        cmdselect = "SELECT MONEY FROM USERS WHERE idman = {}".format(idman)
        message = conn.execute(cmdselect)  # 查询该用户信息的SQL语句
        for i in message:
            print('你余额为:{}'.format(float(i[0])))
            conn.commit()
            conn.close()
            return i
        else:
            return '没有此用户的信息...'

    @pysnooper.snoop()
    def withdraw(self, user_money,idman):
        '''取钱'''
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        before_money = self.select_db(idman)  # 取钱之前的余额
        conn.execute(
            "UPDATE USERS SET MONEY = \"{}\" WHERE idman = {}".format(float(before_money[0]) - float(user_money), idman))  # 执行取钱的SQL操作
        print('取出{}元,还剩{}元.'.format(float(user_money),float(before_money[0]) - float(user_money)))  # 打印出 取出的金额和余下的金额
        conn.commit()
        conn.close()

    @pysnooper.snoop()
    def wallet(self, user_money,idman):
        '''存钱'''
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        before_money = self.select_db(idman)  # 存钱之前的余额
        cmdwallet="UPDATE USERS SET MONEY = {} WHERE idman = {}".format(float(before_money[0]) + float(user_money), idman)
        conn.execute(cmdwallet)  # 执行存钱的操作
        print('存入{}元,现在{}元.'.format(float(user_money), float(before_money[0]) + float(user_money)))  # 打印出存钱后的余额
        conn.commit()
        conn.close()

    @pysnooper.snoop()
    def select_other_db(self, other_ID):
        '''查询该账户的所有信息'''
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        message = conn.execute("SELECT MONEY FROM USERS WHERE idman = {}".format(other_ID))  # 查询指定id的余额信息.
        for i in message:
            print('转给他人余额为:{}'.format(i))
            conn.commit()
            conn.close()
            return i
        else:
            return '没有此用户的信息...'

    @pysnooper.snoop()
    def transfer_accounts(self, idman,other_ID, turn_money):
        '''转账'''
        if idman == other_ID:
            print('不能给自己转账')
            return None
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        user_money=self.select_db(idman)
        cmdtransfer1="UPDATE USERS SET MONEY = \"{}\" WHERE idman = {}".format(user_money[0] - float(turn_money), idman)
        conn.execute(cmdtransfer1)  # 执行己方的转账操作
        other_money = self.select_other_db(other_ID)  # 对方转账之前的余额
        cmdtransfer2="UPDATE USERS SET MONEY = \"{}\" WHERE idman = {}".format(other_money[0] + float(turn_money), other_ID)
        conn.execute(cmdtransfer2)  # 执行对方的转账操作
        print('自己转出:{},还剩{}'.format(float(turn_money), float(user_money[0]) - float(turn_money)))  # 打印出己方的余额
        print('对方转入:{},还剩{}'.format(float(turn_money),float(other_money[0]) + float(turn_money)))  # 打印出对方的余额
        conn.commit()
        conn.close()