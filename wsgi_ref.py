from wsgiref.simple_server import make_server

import _couch

db = None

def setup_db():
    global db
    db = _couch.get_db()

def delete_db():
    _couch.delete_db()

def insert_doc():
    global db
    payload = _couch.get_random_payload()
    doc = {'payload': payload}
    db.save(doc)

def application(environ, start_response):
    global db
    path = environ.get('PATH_INFO')
    if path == '/':
        insert_doc()
        response_body = "created:ok\n"
    if path == '/delete':
        delete_db()
        response_body = "deleted:ok\n"
    if path == '/count':
        count = db.info()['doc_count']
        response_body = "%s docs\n" % count
    status = "200 OK"
    response_headers = [("Content-Length", str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]

setup_db()
httpd = make_server('127.0.0.1', 8000, application)
httpd.serve_forever()
