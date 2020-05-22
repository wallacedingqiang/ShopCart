import menutemplate
import Atm
import ViewManage


if __name__ == '__main__':  # 主函数入口
    view= menutemplate.Menupage()
    view.WelcomeView()
    nowatm=Atm.AtmManager()

    while True:
        atm= Atm.AtmManager()
        viewcontrol=ViewManage.View()

        # 等待用户操作
        option = input("请输入您的操作：")
        if option == 'b':
            #登录
            atm.login()
        elif option=='a':
            #商城界面
            viewcontrol.shop(nowatm)
