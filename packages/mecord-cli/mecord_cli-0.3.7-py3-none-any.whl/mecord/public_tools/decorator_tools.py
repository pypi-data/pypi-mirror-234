
def singleton(cls):
    """
    单例模式装饰器
    :param cls: 目标类
    :return:
    """
    instances = dict()

    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrap
