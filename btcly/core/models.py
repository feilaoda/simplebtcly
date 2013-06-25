

class AttributeDict(dict): 
    def __getattr__(self, key):
        print "key: ", key
        if self.has_key(key):
            value = self[key]
            print "value: ", key,value
            return self[key]
        return None

