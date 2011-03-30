#!/usr/bin/env python

class JSONLoader(object):
    """Parses xml nodes and inserts appropriate ones to db"""
    
    def __init__(self):
        """C'tor sets tag wich we'll count"""
        
        from json import JSONEncoder
        self._encoder = JSONEncoder()
        
        self._current_node = None
        self._count = 0
    
    def start(self, tag, attrib):
        """parser enters tag"""
        
        from model import Node
        
        if tag == "node":
            # Start node writing
            self._current_node = Node(  float(attrib["lat"]),
                                        float(attrib["lon"]),
                                        id = int(attrib["id"])  )
        elif tag == "tag" and self._current_node:
            # Add tag to node
            self._current_node.add_tag(attrib["k"], attrib["v"])
    
    def end(self, tag):
        """parser reached end of tag"""
        if tag == "node" and self._current_node:
            self.__save_node()
            self._current_node = None
    
    def close(self):
        """parser closes"""
        count, self._count = self._count, 0
        return count
    
    def __save_node(self):
        """Save current_node to list"""
        print(self._encoder.encode(self._current_node))
        self._count += 1
    


def main():
    import sys
    from lxml import etree
    
    if len(sys.argv) < 2:
        print("Usage: tojson.py <filename>")
        exit(1)
    filename = sys.argv[1]
    
    c = JSONLoader()
    parser = etree.XMLParser(target = c)
    count = etree.parse(filename, parser)
    
    # print count

if __name__ == '__main__':
    main()

