import random
import sqlite3


# 随机生成卡号
def createCardId():
    while True:
        str = ""
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        return str



# 验证密码,循环三次没有正确就输出错误
def checkPassword(realPasswd):
            for i in range(3):
                temPasswd = input("请确认密码：")
                if temPasswd == realPasswd:
                    return True
            return False


'''检查账户是否合规的类'''
def validate_logon(idman, password):
        '''查询该账户的所有信息,核对密码是否正确'''
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        check = conn.execute("SELECT PASSWORD FROM USERS WHERE idman = {}".format(idman))  # 核对账户密码是否正确
        for i in check:
            print(i[0])
            if i[0] == str(password):
                conn.commit()
                conn.close()
                return True
            else:
                conn.commit()
                conn.close()
                return False

def checking_ID(idman):
        '''检查该ID是否存在,如已存在返回False,否则返回True'''
        conn = sqlite3.connect('atm.db')  # 创建一个数据库链接
        check = conn.execute("SELECT idman FROM USERS WHERE idman = {}".format(idman))  # 查询数据库中的ID是否存在
        for i in check:
            if i[0] == idman:
                conn.commit()
                conn.close()
                return False
            else:
                conn.commit()
                conn.close()
                return True
        else:
            return True