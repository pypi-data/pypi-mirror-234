import functools
from typing import (Callable, Optional, Awaitable)

from tornado.web import RequestHandler


# def interceptor(func):
#     def wrapper(*args, **kwargs):
#         # 在调用原始函数之前执行操作
#         print('before calling %s' % func.__name__)
#
#         # 调用原始函数
#         result = func(*args, **kwargs)
#
#         # 在调用原始函数之后执行操作
#         print('after calling %s' % func.__name__)
#
#         # 返回原始函数的结果
#         return result
#
#     return wrapper



def interceptor( method: Callable[..., Optional[Awaitable[None]]] ) -> Callable[..., Optional[Awaitable[None]]]:
    """Decorate methods with this to require that the user be logged in.
    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """

    @functools.wraps(method)
    def wrapper(  # type: ignore
            self: RequestHandler, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        try:
            print(method,self.__class__,args,kwargs,method.__annotations__.get('return'))
            if method.__annotations__.get('return') and 'OUT-OF-WSLIMITS' in method.__annotations__.get('return') and method.__annotations__.get('return')['OUT-OF-WSLIMITS'] == "TRUE":
                return method(self, *args, **kwargs)
            elif method.__annotations__.get('return') and kwargs.get("ws_uid"):
                header = self.request.headers
                if header.get("user_ws_role").upper() in method.__annotations__.get('return')['ROLE'] and header.get("snb_user_grade").upper() in method.__annotations__.get('return')['GRADE']:
                    return method(self, *args, **kwargs)
                else:
                    self.write("""{"code": 403, "data": {}, "msg": "无权限操作，请联系管理员！！"}""")
                    return None
            else:
                return method(self, *args, **kwargs)
        except Exception as e:
            self.write("""{"code": 400, "data": {}, "msg": "内部发生错误,请联系管理员！！"""+str(e)+""" "}""")
            return None
    return wrapper
