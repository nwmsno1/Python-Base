import time

current_user = {'user': None}


def auth(engine='file'):
    def deco(func):   # func=最初始的index和最初始的home
        def wrapper(*args, **kwargs):
            if current_user['user']:
                # 如果成立说明current_user里面已经有用户信息,说明用户已经登录过，满足条件
                # 即会执行调用index home函数
                res = func(*args, **kwargs)  # 调用最原始的index 同样也调用最原始的home,
                return res

            user = input('input your username: ').strip()
            pwd = input('input your password: ').strip()

            if engine == 'file':
                # 基于文件的认证
                if user == 'nwmsno1' and pwd == '123':
                    print('Auth successful')
                    # 记录用户登录状态
                    current_user['user'] = user
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('username or password is wrong!')
            elif engine == 'mysql':
                print('Auth base on mysql')
            elif engine == 'idap':
                print('Auth base on idap')
            else:
                print("Couldn't recognize original auth")

        return wrapper
    return deco


@auth(engine='file')
def index():
    time.sleep(1)
    print('welcome to index page')


@auth(engine='file')
def home(name):
    print('welcome %s to home page' % name)


if __name__ == '__main__':
    index()
    home('nwmsno1')
