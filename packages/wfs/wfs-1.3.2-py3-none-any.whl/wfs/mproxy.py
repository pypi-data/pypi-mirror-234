from mitmproxy import ctx
from mitmproxy.addonmanager import AddonManager
from mitmproxy import http
from mitmproxy.tools.main import mitmproxy
from pathlib import Path
import os, json
import platform

mypath = Path.cwd()


# https://interapps-uat.cdgtaxi.com.sg
def getspliter(apix, method):
    spltapi = apix.split('/dcp-cms/rest/')[1]
    if '/' in spltapi and '?' not in spltapi:
        spltapi = str(spltapi).replace('/', '_')
    if '?' in spltapi:
        spltapi = str(spltapi).split('?')[0]
    return spltapi + '_' + method.lower()


class APIEndpointLogger:
    def __init__(self):
        self.api_endpoints = set()

    def request(self, flow: http.HTTPFlow) -> None:
        try:
            if flow.request.path.startswith("/dcp-cms/rest/"):
                print("API Request:" + str(flow.request.path))
                # Save the request content to a file
                fnamex = getspliter(apix=flow.request.path, method=flow.request.method)
                request_filename = mypath / 'test_data' / 'mobile' / 'pxy' / 'request'
                os.makedirs(request_filename, exist_ok=True)
                request_filename = str(request_filename / (fnamex + '.json'))
                getrequest = json.loads(flow.request.content.decode())
                with open(request_filename, 'w') as file:
                    # file.write(json.dump(getrequest))
                    json.dump(getrequest, file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            return

    def response(self, flow: http.HTTPFlow) -> None:
        try:
            if flow.request.path.startswith("/dcp-cms/rest/"):
                self.api_endpoints.add((flow.request.path, flow.response.content))
                fnamex = getspliter(apix=flow.request.path, method=flow.request.method)
                response_filename = mypath / 'test_data' / 'mobile' / 'pxy' / 'response'
                os.makedirs(response_filename, exist_ok=True)
                response_filename = str(response_filename / (fnamex + '.json'))
                getresponse = json.loads(flow.response.content.decode())
                with open(response_filename, 'w') as file:
                    # file.write(json.dump(getresponse))
                    json.dump(getresponse, file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            return


def done(self) -> None:
    print("API Endpoints:")
    for endpoint in self.api_endpoints:
        print(f"Path: {endpoint[0]}")
        print(f"Content: {endpoint[1]}")
        print("-" * 20)


addons = [
    APIEndpointLogger()
]


def start_proxy():
    mitmproxy(["-s", __file__])


if __name__ == "__main__":
    start_proxy()
