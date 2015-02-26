#from schema import modeline, modechange, blankschema, has_modeline
import dom
import sys, os
#import metaschema
#
class Workspace(object):
    def __init__(self):
        self.documents = {}
#        self.unbound = []
#        self.copybuf = None
#        self.schema_cache = {}
#
#    def new(self):
#        body = dom.Literal(u"", [])
#        document = dom.Document(body, None)
#        self.unbound.append(document)
#        return document
#
#    def attach(self, document, name):
#        self.unbound.append(document)
#        document.name = name
#        return document
#
    def get(self, path, create=True):
        if path in self.documents:
            return self.documents[path]
        elif os.path.isfile(path):
            document = dom.Document(dom.ListCell("", dom.load(path)), self)
            self.documents[path] = document
            return document
        elif create:
            document = dom.Document(dom.ListCell("", []), self)
            self.documents[path] = document
            return document
        else:
            raise Exception("No such file: {}".format(path))

#    def get_schema(self, name):
#        if name == 'schema':
#            return metaschema.schema
#        path = os.path.join('schemas', name + '.t+')
#        if os.path.isfile(path):
#            if path in self.schema_cache:
#                return self.schema_cache[path]
#            else:
#                schema = self.schema_cache[path] = metaschema.load(dom.load(path))
#                return schema
#        return blankschema
#
#    def active_schema(self, subj):
#        while subj.parent is not None:
#            subj = subj.parent
#            if subj.label == '#' and modechange.validate(subj):
#                modeline = subj[0]
#                return self.get_schema(modeline[0][:])
#        if has_modeline(subj):
#            modeline = subj[0]
#            return self.get_schema(modeline[0][:])
#        return blankschema