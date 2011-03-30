#!/usr/bin/env python

from lxml import etree as ET
from pymongo import Connection

from model import Node, POI

class Cruncher(object):
    """XML Cruncher!!!"""
    
    current_node = None
    nodes = []
    
    def start(self, tag, attrib):
        """parser enters tag"""
        
        if tag == "node":
            self.current_node = Node(attrib["id"], attrib["lat"], attrib["lon"])
        elif tag == "tag" and self.current_node:
            self.current_node.add_tag(attrib["k"], attrib["v"])
    
    def end(self, tag):
        """parses end tags"""
        if tag == "node" and self.current_node:
            if self.current_node.tags.has_key("name"):
                self.nodes.append(self.current_node)
            self.current_node = None
    
    def close(self):
        """parser closes"""
        nodes, self.nodes = self.nodes, []
        return nodes
    

class Counter(object):
    """Counts our named tags"""
    
    in_node = False
    count = 0
    
    def __init__(self, countable_aspect):
        """Ctor sets tag wich we'll count"""
        self._countable_aspect = countable_aspect
    
    def start(self, tag, attrib):
        """parser enters tag"""
        if tag == "node":
            self.in_node = True
        elif tag == "tag" and self.in_node and attrib.get("k") == self._countable_aspect:
            print "{tag}: {attrib}".format(tag=tag, attrib=attrib)
            self.count += 1
    
    def end(self, tag):
        """parser exits tag"""
        if tag == "node":
            self.in_node = False
    
    def close(self):
        """parser closes"""
        count, self.count = self.count, 0
        return count
    

class MongoLoader(object):
    """Parses xml nodes and inserts appropriate ones to db"""

    def __init__(self, collection_name, named_only, tag_names):
        """C'tor sets tag wich we'll count"""
        self._named_only = named_only
        
        if isinstance(tag_names, list):
            self._tag_names = set(tag_names)
        else:
            self._tag_names = set([tag_names])
        
        self._current_node = None
        self._count = 0
        
        conn = Connection('localhost', 27017)
        db = conn['openstreet']
        self._ca = db[collection_name]
    
    def start(self, tag, attrib):
        """parser enters tag"""
        
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
            
            # tags_set = set(self._current_node.tags)
            # if not self._named_only or "name" in tags_set:
            #     if len(tags_set & self._tag_names):
            #         self._save_node()
            
            if "name" in self._current_node.tags:
                self._save_node()
                
            self._current_node = None
    
    def close(self):
        """parser closes"""
        count, self._count = self._count, 0
        return count
    
    def _save_node(self):
        """Save current_node to list"""
        self._ca.insert(self._current_node)
        self._count += 1
    

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: cruncher.py <filename> <collection_name>")
        exit(1)
    
    filename = sys.argv[1]
    collection_name = sys.argv[2]
    
    tag_names = ["amenity", "tourism", "historic", "natural", "sport", "place"]
    
    # c = Cruncher()
    # parser = ET.XMLParser(target=c)
    # nodes = ET.fromstring(teststring, parser)
    # 
    # for node in nodes:
    #     print node
    
    # c = Counter(countable_name)
    # parser = ET.XMLParser(target = c)
    # count = ET.parse(filename, parser)
    # 
    # print count
    
    c = MongoLoader(collection_name, True, tag_names)
    parser = ET.XMLParser(target = c)
    count = ET.parse(filename, parser)
    
    print count
