class Node(dict):
    """OSM Node model"""
    
    def __init__(self, lat, lon, **kwargs):
        self["tags"] = {}
        self["features"] = []
        self["coord"] = {"lat": lat, "lon": lon}
        for arg in kwargs.items():
            self[arg[0]] = arg[1]
    
    def __getattr__(self, name):
        """__getattr__ overload to dict.__getitem__"""
        return self[name]
    
    def __setattr__(self, name, value):
        """__setattr__ overload to dict.__setattr__"""
        self[name] = value
    
    def add_tag(self, key, value):
        """adds new tag"""
        key = key.replace(".", ":")
        self.tags[key] = value
        self.features = self.tags.keys()
    

class POI(object):
    """Point of Interest"""
    def __init__(self, name, feature_class, type, node):
        self.name = name
        self.feature_class = feature_class
        self.type = type
        self.node = node
    
