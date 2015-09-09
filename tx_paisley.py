from twisted.web import server
from twisted.internet import reactor, defer
from twisted.web.resource import Resource
from twisted.python import log

from paisley import CouchDB

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
        return self.db.saveDoc('couch-benchmarks', doc)

    def _write_GET(self, msg, request):
        request.write(msg)
        request.finish()


class Create(Root):

    def render_GET(self, request):
        d = self.insert_doc()
        msg = "created:ok\n"
        d.addCallback(lambda _: self._write_GET(msg, request))
        return server.NOT_DONE_YET

class Delete(Root):
    def render_GET(self, request):
        _couch.delete_db()
        return "deleted:ok\n"

class Count(Root):
    @defer.inlineCallbacks
    def _get_count(self):
        info = yield db.infoDB('couch-benchmarks')
        count =  info['doc_count']
        defer.returnValue("%s docs\n" % count)
    
    def render_GET(self, request):
        d = self._get_count()
        d.addCallback(self._write_GET, request)
        return server.NOT_DONE_YET

db_sync = _couch.get_db()
db = CouchDB('localhost')
Root.db = db
Root.db_sync = db_sync

def create_db():
    d = db.createDB('couch-benchmarks')

    def del_and_create(_):
        d = db.deleteDB('couch-benchmarks')
        d.addCallback(lambda _: db.createDB('couch-benchmarks'))
        return d
    d.addErrback(del_and_create)
    d.addErrback(lambda f: log.err(f))

reactor.callWhenRunning(create_db)

root = Create()
root.putChild('delete', Delete())
root.putChild('count', Count())
site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()
