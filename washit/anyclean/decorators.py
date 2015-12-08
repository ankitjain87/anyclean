from anyclean import models

from django.contrib.auth.models import User
from django import http

import functools


def has_cc_permission(function):
    @functools.wraps(function)
    def wrapper(request, *args, **kw):
        try:
            user_group = [g.name for g in request.user.groups.all()]
            if "CR" in user_group:
                return function(request)
            else:
                return http.HttpResponseRedirect('/dashboard/')

        except Exception as ex:
            return http.HttpResponseServerError()

    return wrapper


def has_customer_permission(function):
    @functools.wraps(function)
    def wrapper(request, *args, **kw):
        try:
            user_group = [g.name for g in request.user.groups.all()]
            if "CR" in user_group:
                return http.HttpResponseRedirect('/ccDashboard/')
            else:
                return function(request)

        except Exception as ex:
            return http.HttpResponseServerError()

    return wrapper
