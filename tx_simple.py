from twisted.web import server
from twisted.internet import reactor
from twisted.web.resource import Resource

import _couch

class Root(Resource):
    isLeaf = False
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def insert_doc(self):
        payload = _couch.get_random_payload()
        doc = {'payload': payload}
        self.db.save(doc)


class Create(Root):
    def render_GET(self, request):
        # blocking
        self.insert_doc()
        return "created:ok\n"

class Delete(Root):
    def render_GET(self, request):
        # blocking
        _couch.delete_db()
        return "deleted:ok\n"

class Count(Root):
    def render_GET(self, request):
        count = db.info()['doc_count']
        return "%s docs\n" % count

db = _couch.get_db()
Root.db = db

root = Create()
root.putChild('delete', Delete())
root.putChild('count', Count())
site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()
