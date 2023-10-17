import requests
import json
import moyanlib.Error as Error


class request:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"}
        self.method = "GET"

    def init(self, headers, type):
        self.headers = headers
        self.method = type

    def send(self, config:dict):
        method = config.get("method", self.method)
        headers = config.get("headers", self.headers)
        # print(headers)
        url = config.get("url", "")
        data = config.get("data", {})
        try:
            req = requests.request(
                method=method, url=url, headers=headers, data=data)
        except requests.exceptions.ConnectionError as e:
            raise Error.http_ConnectionError(e)
        except requests.exceptions.Timeout as e:
            raise Error.http_TimeoutError(e)
        except requests.exceptions.InvalidHeader as e:
            raise Error.http_InvalidHeaderError(e)
        except requests.exceptions.InvalidURL as e:
            raise Error.http_InvalidURLError(e)

        else:
            return req

    def get(self, url, data=None, headers=None):
        config = {
            "method": "GET",
            "url": url,
            "data": data,
            "headers": headers

        }
        return self.send(config)

    def post(self, url, data=None, headers=None):
        config = {
            "method": "POST",
            "url": url,
            "data": data,
            "headers": self.headers
        }
        return self.send(config)

    def upload(self, url, data=None, headers=None, key="file", path=None):

        # 打开文件，并使用 'rb' 模式(二进制模式)读取文件内容
        with open(path, 'rb') as file:
            # 构建文件数据
            files = {key: file}

            # 发送 POST 请求，包含文件数据
            response = requests.post(
                url, files=files, data=data, headers=headers)

            # 返回响应数据
            return response

    def get_json(self, url, params=None, headers=None):
        response = self.get(url, params=params, headers=headers)
        try:
            json_data = response.json()
            return json_data
        except json.JSONDecodeError:
            return None

    def post_json(self, url, json_data=None, headers=None):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        else:
            headers["Content-Type"] = "application/json"
        data = json.dumps(json_data)
        response = self.post(url, data=data, headers=headers)
        try:
            json_response = response.json()
            return json_response
        except json.JSONDecodeError:
            return None

    def put_json(self, url, json_data=None, headers=None):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        else:
            headers["Content-Type"] = "application/json"
        data = json.dumps(json_data)
        response = self.put(url, data=data, headers=headers)
        try:
            json_response = response.json()
            return json_response
        except json.JSONDecodeError:
            return None

    def head(self, url, headers=None):
        config = {
            "method": "HEAD",
            "url": url,
            "headers": headers
        }
        return self.send(config)

    def options(self, url, headers=None):
        config = {
            "method": "OPTIONS",
            "url": url,
            "headers": headers
        }
        return self.send(config)

    def trace(self, url, headers=None):
        config = {
            "method": "TRACE",
            "url": url,
            "headers": headers
        }
        return self.send(config)

    def put(self, url, data=None, headers=None):
        config = {
            "method": "PUT",
            "url": url,
            "data": data,
            "headers": headers
        }
        return self.send(config)

    def delete(self, url, data=None, headers=None):
        config = {
            "method": "DELETE",
            "url": url,
            "data": data,
            "headers": headers
        }
        return self.send(config)

    def patch(self, url, data=None, headers=None):
        config = {
            "method": "PATCH",
            "url": url,
            "data": data,
            "headers": headers
        }
        return self.send(config)
