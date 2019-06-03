"""
1、访问页面时模拟网站登录验证

2、提供2个登录通道

3、指定具体页面使用特定的登录通道，登录登录后保留登录状态，切换到其他页面时检测登录状态

4、不同通道登录账号密码用文件保存，读取之后进行验证登录（后期更换为数据库读取）
"""


login_status_jingdong = False
login_status_weixin = False


def login(login_channel):
    def checklogin(func):
        def foo():
            global login_status_jingdong
            global login_status_weixin
            if login_channel == 'jingdong':
                if login_status_jingdong == False:
                    print("请输入京东账号登录")
                    f = open('jingdong.txt', 'r', encoding='utf8')
                    xtmp = eval(f.read())
                    f.close()
                    userlist = []
                    for key in xtmp:
                        name = key
                        userlist.append(name)
                    n = 0
                    while n < 4:
                        inp_user = input('输入账号:')
                        if inp_user in userlist:
                            inp_passwd = input('输入密码:')
                            if inp_passwd == xtmp[inp_user]:
                                print('登录成功')
                                login_status_jingdong = True
                                break
                            else:
                                print('账号、密码错误请重新输入')
                                n = n + 1
                                print(n)
                        else:
                            print('账号不存在！')
                    else:
                        print("密码错误次数过多！")

                    func()
                else:
                    func()
            elif login_channel == 'weixin':
                if login_status_weixin == False:
                    print("请输入微信账号登录")
                    f = open('weixin.txt', 'r', encoding='utf8')
                    xtmp = eval(f.read())
                    f.close()
                    userlist = []
                    for key in xtmp:
                        name = key
                        userlist.append(name)
                    n = 0
                    while n < 4:
                        inp_user = input('输入账号:')
                        if inp_user in userlist:
                            inp_passwd = input('输入密码:')
                            if inp_passwd == xtmp[inp_user]:
                                print('登录成功')
                                login_status_weixin = True
                                break
                            else:
                                print('账号、密码错误请重新输入')
                                n = n + 1
                                print(n)
                        else:
                            print('账号不存在！')
                    else:
                        print("密码错误次数过多！")
                    func()
                else:
                    func()

        return foo

    return checklogin


# menu={'1':'首页','2':'金融','3':'图书'}
# for i in menu:
# 	print(i,menu[i])

@login("jingdong")
def home():
    print("打印京东首页页面")


@login("weixin")
def finance():
    print("打印京东金融页面")


@login("weixin")
def book():
    print("打印京东图书页面")


while True:
    menu = {'1': '首页', '2': '金融', '3': '图书', '4': '退出'}
    for i in menu:
        print(i, menu[i])
    page = input('请输入您要访问的页面:')
    if page == '1':
        home()
    elif page == '2':
        finance()
    elif page == '3':
        book()
    elif page == '4':
        print('退出账号')
        break
    else:
        print('访问的页面不存在')


