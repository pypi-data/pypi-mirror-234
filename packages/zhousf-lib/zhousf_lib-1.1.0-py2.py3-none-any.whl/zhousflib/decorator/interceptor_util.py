# -*- coding:utf-8 -*-
# Author:      zhousf
# File:        interceptor_util.py
# Description:  AOP拦截器
import functools


def intercept(before=None, after=None):
    """
    拦截器
    :param before: 过滤器
    :param after: 过滤器
    def before(*args):
        if args[0] == "0":
            return True, '拦截'
        return False, '不拦截'
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*chain, **kw):
            if before is not None:
                result_before = before(chain)
                if isinstance(result_before, tuple):
                    need_intercept, msg = result_before
                else:
                    need_intercept = result_before
                    msg = "interceptor"
                if need_intercept:
                    return msg
                result = func(msg, **kw)
            else:
                result = func(chain, **kw)
            return result if after is None else after(result)
        return wrapper

    return decorator

