import json

from django.http import JsonResponse, HttpResponse


class ResObj:
    __res = None

    def __init__(self, data=None, message='', code=200):
        self.__res = {
            "code": code,
            "message": message,
            "data": data
        }
        # print(json.dumps(self.__res, ensure_ascii=False))

    def json(self):
        return HttpResponse(json.dumps(self.__res, ensure_ascii=False), content_type="application/json")
