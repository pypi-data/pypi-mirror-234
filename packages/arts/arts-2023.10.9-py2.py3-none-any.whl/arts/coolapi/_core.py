'''
Copyright 2023 lcctoor.com

Author Information:
Author's Name: 许灿标
Author's Nickname: lcctoor.com
Author's Domain: lcctoor.com
Author's Email: lcctoor@outlook.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
For the detailed terms and conditions, refer to the Apache License, Version 2.0 at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from tornado.web import RequestHandler as torHandler
from tornado.web import Application


class handler(torHandler):
    urls = ['/']

    async def get(self):
        return self.write('Hello Get')
    
    async def post(self):
        return self.write('Hello Post')
    
    def get_body(self): return self.request.body
    def get_ip(self): return self.request.remote_ip

    def set_access_control_allow_origin(self, origin="*"): self.set_header("Access-Control-Allow-Origin", origin)

def optimizeHandler(h:handler):
    class new_handler(h):
        if h.get is not handler.get:
            async def get(self:handler, *vs, **kvs):
                self.set_header("Access-Control-Allow-Origin", "*")  # 允许跨域
                return await h.get(self, *vs, **kvs)
            
        if h.post is not handler.post:
            async def post(self:handler, *vs, **kvs):
                self.set_header("Access-Control-Allow-Origin", "*")  # 允许跨域
                return await h.post(self, *vs, **kvs)
    return new_handler
    

def optimizeUrl(url):
    return url

def creat_server(handlers=[], port=80, static_path=None, debug=False, address=None, **args):
    results = {}
    for h in handlers:
        results |= dict.fromkeys(h.urls, optimizeHandler(h))
    http_server = Application(
        handlers = list(results.items()),
        static_path = static_path,
        debug = debug,
        address = address,
        **args
    )
    http_server.listen(port)
    return http_server