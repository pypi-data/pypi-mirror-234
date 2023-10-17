"""
Created on 2022-05-20
@author:刘飞
@description:用户验证装饰器，为单个请求方式做验证
"""
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request

from xj_user.services.user_service import UserService
from ..utils.custom_response import util_response


def user_authentication_wrapper(func):
    """
    用户认证装饰器，如果有Authorization则检查用户的有效性，如没有则认为用户以游客访问
    """

    def wrapper(instance, arg_request=None, *args, request=None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param request APIView实例会传入请求包
        @param request APIView实例会传入请求包
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        # print(instance, arg_request, request, args, kwargs)
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request is None:
            return func(instance * args, request=request, user_info={}, **kwargs, )
        # token = request.META.get('HTTP_AUTHORIZATION', None)
        token = request.headers.get('Authorization', None)
        # print("> user_authentication_wrapper token:", token, type(token))

        # 如果没有传token则可视为以游客身份访问
        if not token or str(token) == 'null' or str(token).strip().upper() == "BEARER":
            return func(instance, request=request, user_info=None, *args, **kwargs)

        user_serv, error_text = UserService.check_token(token)
        # print("> user_authentication_wrapper user_serv, error_text:", user_serv, error_text)
        if error_text:
            # raise exceptions.AuthenticationFailed(error_text)
            return util_response(err=6001, msg=error_text)
            # raise exceptions.AuthenticationFailed(error_text)

        request.user = user_serv
        result = func(instance, *args, request=request, user_info=user_serv, **kwargs)
        return result

    return wrapper


def user_authentication_force_wrapper(func):
    """
    用户认证装饰器，如果有Authorization则检查用户的有效性，如没有则认为用户以游客访问
    """

    def wrapper(instance, arg_request=None, *args, request=None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param request APIView实例会传入请求包
        @param request APIView实例会传入请求包
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request is None:
            return func(instance * args, request=request, user_info={}, **kwargs, )
        # token = request.META.get('HTTP_AUTHORIZATION', None) # 请求头不能将HTTP 及 _ 携带进请求头中，这样会导致系统识别失败
        token = request.headers.get('Authorization', None)

        # 如果没有传token则可视为以游客身份访问
        if not token or str(token) == 'null' or str(token).strip().upper() == "BEARER":
            return util_response(err=6001, msg="该用户未登录")

        user_serv, error_text = UserService.check_token(token)
        if error_text:
            return util_response(err=6001, msg=error_text)

        request.user = user_serv
        result = func(instance, *args, request=request, user_info=user_serv, **kwargs)
        return result

    return wrapper
