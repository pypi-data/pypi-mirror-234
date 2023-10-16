import json


def escape(data):
    if "<" in data or ">" in data:
        return data.replace('<', '&lt;').replace('>', '&gt;')
    return data

def set_default(obj):
    if not isinstance(obj, (list, dict)):
        return escape(str(obj))


class Process:
    def __init__(self):
        self.query_info = None
        self.error_info = None

    def data_process(self, q_data, e_data):
        if q_data.query:
            query = json.dumps(q_data.query, indent=4, ensure_ascii=False, default=set_default)
            query = escape(query)
        else:
            query = None
        if q_data.resp_headers:
            resp_headers = json.dumps(q_data.resp_headers, indent=4, ensure_ascii=False, default=set_default)
            resp_headers = escape(resp_headers)
        else:
            resp_headers = None
        if q_data.resp_cookies:
            resp_cookies = json.dumps(q_data.resp_cookies, indent=4, ensure_ascii=False, default=set_default)
            resp_cookies = escape(resp_cookies)
        else:
            resp_cookies = None
        if q_data.response:
            if isinstance(q_data.response, str):
                response = escape(q_data.response)
            else:
                response = json.dumps(q_data.response, indent=4, ensure_ascii=False, default=set_default)
                response = escape(response)
        else:
            response = None
        status_code = q_data.status_code
        self.query_info = dict(query=query, resp_headers=resp_headers, resp_cookies=resp_cookies, response=response, status_code=status_code)
        if e_data:
            if isinstance(e_data.msg_dict, str):
                msg_dict = escape(e_data.msg_dict)
            else:
                msg_dict = json.dumps(e_data.msg_dict, indent=4, ensure_ascii=False, default=set_default)
                msg_dict = escape(msg_dict)
            typed = e_data.typed
            self.error_info = dict(msg_dict=msg_dict, typed=typed)
