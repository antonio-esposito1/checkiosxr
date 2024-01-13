"Assorted class utilities and tools"

class AttrDisplay:
    "Provides an inheritable display overload method that shows instances with their class names and a name=value pair for each attribute stored on the instances itself"
    "(but not attrs inherited from its classes). Can be mixed into any class, and will work on any instance."
    
    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('%s=%s' % (key, getattr(self, key)))
        return ', '.join(attrs)
    
    #questo ho la precedenza su __rpr__ ed è usata conf print e str function
    def __str__(self):
        return '[Nome %s: Attributi %s]' % (self.__class__.__name__, self.gatherAttrs())
    
    #usato in tutti gli altri contesti dove non viene usato __str__ ad esempio interactive echo, repr function, nested data
    def __repr__(self):
        return '[%s: %s]' % (self.__class__.__name__, self.gatherAttrs())
    
#Sel Test Code
if __name__ == '__main__':
    
    class TopTest(AttrDisplay):
        count = 0
        def __init__(self):
            self.attr1 = TopTest.count
            self.attr2 = TopTest.count + 1
            TopTest.count +=2
            
    class SubTest(TopTest):
        pass
    
    X, Y = TopTest(), SubTest()
    print(X)
    print(Y)
