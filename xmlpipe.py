#!/usr/bin/env python

def dict_concat(*args):
    """concatenates two dictionaries"""
    arr = [t for arg in args for t in arg.iteritems() ]
    return dict(arr)

def unicode_dict(d):
    """applies unicode() to keys and values of input dict d"""
    return dict([(unicode(k), unicode(v)) for k,v in d.iteritems()])

class Pipe(object):
    """xmlpipe2 implementation"""
    def __init__(self, docs_iter, fields, attrs=None):
        self.docs_iter = docs_iter
        self.fields = fields
        self.attrs = attrs
    
    def to_xml(self):
        """return xml"""
        
        from lxml import etree
        from lxml.builder import E, ElementMaker
        
        SPHINX = ElementMaker(namespace='sphinx', nsmap={'sphinx': 'sphinx'})
        mydoc = SPHINX.docset(
            SPHINX.schema(
                *(  [SPHINX.field({"name": f}) for f in self.fields] +
                    [SPHINX.attr(dict([("name", k)] + v.items())) for k,v in self.attrs.iteritems()]    )
            ),
            
            *[SPHINX.document({"id": id}, *[getattr(E, k)(v) for k,v in doc.iteritems()]) for id, doc in self.docs_iter]
        )
        return etree.tostring(mydoc, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    
    def to_elementflow(self):
        """generates xml using elementflow"""
        
        import sys
        import elementflow
        
        with elementflow.xml(sys.stdout, u'sphinx:docset', indent=True) as xml:
            with xml.container(u'sphinx:schema'):
                for f in self.fields:
                    xml.element(u'sphinx:field', attrs={u'name': unicode(f)})
                for attrs_k, attrs_v in self.attrs.iteritems():
                    c_d = dict_concat({u'name': attrs_k}, attrs_v)
                    xml.element(u'sphinx:attr', attrs=unicode_dict(c_d))
            
            for id, doc in self.docs_iter:
                with xml.container(u'sphinx:document', attrs={u'id': unicode(id)}):
                    for k,v in doc.iteritems():
                        xml.element(unicode(k), text=unicode(v))
    


def mongo_gen(limit=1, db = "openstreetmaps", coll = "europe"):
    """
        Generator, yielding db rows
    """
    
    from pymongo import Connection
    
    def f(x):
        import re
        return re.match("name.?", x[0])
    
    ca = Connection()[db][coll]
    for doc in ca.find({"tags.name": {"$exists": True}}).limit(limit):
        names = ", ".join([n[-1] for n in filter(f, doc["tags"].iteritems())])
        yield (    doc["id"],
                    {   # "name": doc["tags"]["name"],
                        "names": names,
                        "lat": doc["coord"]["lat"],
                        "lon": doc["coord"]["lon"]}  )


def main():
    """Main program loop"""
    
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: xmlpipe.py <db> <coll> <limit>")
        exit(1)
    db = sys.argv[1]
    coll = sys.argv[2]
    limit = int(sys.argv[3])
    
    # Connect DB
    # conn = Connection()
    # db = conn["openstreet"]
    # ca = db["central_america"]
    
    pipe = Pipe(
                mongo_gen(limit, db, coll),
                ["names"],
                {
                    "lat": {"type": "float", },
                    "lon": {"type": "float", },
                }
            )
    
    # print(pipe.to_xml())
    pipe.to_elementflow()
    
    # for node in ca.find({"tags.name":"San Salvador"}, ["tags"]).limit(10):
    #     id = unicode(node["_id"])
    #     text = " ".join(list(set([v for k,v in node["tags"].iteritems() if "name" in k])))
    #     
    #     print({id: text})


if __name__ == '__main__':
    main()
