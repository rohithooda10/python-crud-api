from tornado import ioloop, web
from tornado.escape import json_decode
import json
import threading
from dataclasses import dataclass, field

# in-memory database
items = []
lock = threading.Lock()

@dataclass
class Response:
    data: dict = field(default_factory=dict)
    status: str = 500
    errormessage: str = ""

class BaseHandler(web.RequestHandler):
    def write_json(self, response):
        self.set_header("Content-Type","application/json")
        self.write(json.dumps(response.__dict__))

class CreateItemHandler(BaseHandler):
    def post(self):
        with lock:
            global items
            response = Response()
            request_body = json_decode(self.request.body)
            items.append(request_body)
            response.status = 200
            response.data = None
            self.write_json(response)

class GetAllItemHandler(BaseHandler):
    def get(self):
        with lock:
            global items
            response = Response()
            response.data = items
            response.status = 200
            self.write_json(response)

class ItemHandler(BaseHandler):
    def get(self, id):
        with lock:
            global items
            response = Response()
            id = int(id)
            for item in items:
                if item["id"] == id:
                    response.data = item
                    break
            response.status = 200
            self.write_json(response)

    def patch(self, id):
        with lock:
            global items
            response = Response()
            id = int(id)
            item_index = -1
            request_body = json_decode(self.request.body)
            for index, item in enumerate(items):
                if item["id"] == id:
                    item_index = index
                    break
            if item_index == -1:
                response.status = 404
                response.errormessage = "item not found"
                self.write_json(response)
            
            items[item_index] =  request_body
            response.status = 200
            self.write_json(response)

    def delete(self, id):
        with lock:
            global items
            id = int(id)
            response = Response()
            for item in items:
                if item["id"] == id:
                    items.remove(item)
                    response.status = 200
                    response.errormessage = "item deleted"
                    self.write_json(response)
            
            response.status = 404
            response.errormessage = "item not found"
            self.write_json(response)

def make_app():
    return web.Application([
        (r'/api/v1/item', CreateItemHandler),
        (r'/api/v1/items', GetAllItemHandler),
        (r'/api/v1/item/(\d+)', ItemHandler)
    ])
if __name__=="__main__":
    app = make_app()
    app.listen(8080)
    print("Server is running on http://127.0.0.1:8080")
    ioloop.IOLoop.current().start()

        