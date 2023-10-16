def validate_request(func):
    def wrapper(*args, **kwargs):
        # 执行校验逻辑，可以是任何你需要的操作
        print("args:", args)
        print("kwargs:", kwargs)
        print("进行请求校验")

        # 执行被装饰的函数
        return func(*args, **kwargs)

    return wrapper


# 示例函数1，需要进行请求校验
@validate_request
def function1(token, b):
    print("执行函数1")


# 示例函数2，也需要进行请求校验
@validate_request
def function2():
    print("执行函数2")


# 调用函数1
function1("qq", 'ggg')

# 调用函数2
function2()
