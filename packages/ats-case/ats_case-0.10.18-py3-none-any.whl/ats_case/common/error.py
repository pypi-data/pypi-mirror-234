class APIError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "APIError - API服务接口[{}], 连接失败.".format(repr(self.value))


class MeterOperationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "MeterOperationError - 电表操作失败, {}.".format(repr(self.value))


class ClientError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "ClientReturnError - 客户端返回结果为空. {}".format(repr(self.value))

# MeterTimeoutError 电表连接超时
# 服务接口错误  电表错误  客户端错误 加密机错误
# 连接错误 代码错误 操作错误 
