class Card(object):
    def __init__(self,idcard,cardpassword,cardmoney):  #idcard信用卡号
        self.idcard=idcard
        self.cardpassword=cardpassword
        self.cardmoney=cardmoney
        self.cardlock=False    #是否被锁定


