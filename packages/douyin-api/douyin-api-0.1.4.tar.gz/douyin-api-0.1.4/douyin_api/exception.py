# __all__ = [
#     # warnings
#     # exceptions
#     'DouYinException',
#     'NeedLoginException',
# ]


class DouYinException(Exception):
    pass


class NeedLoginException(DouYinException):
    def __init__(self, what):
        """
        使用某方法需要登录而当前客户端未登录

        :param str|unicode what: 当前试图调用的方法名
        """
        self.what = what

    def __repr__(self):
        return '需要登录才能使用 [{self.what}] 方法。'.format(self=self)

    __str__ = __repr__


class NeedAccessTokenException(DouYinException):

    def __repr__(self):
        return '需要用户 access-token 才能使用这个接口！'.format(self=self)

    __str__ = __repr__


class LoginError(DouYinException):
    """
    所有登录中发生的错误
    """
