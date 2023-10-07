import os
import yaml
import inspect

class Schema:
    
    def __new__(cls, *args, **kwargs):
        # Create a new instance of Schema
        return super().__new__(cls)
    
    def __init__(self):
        # Initialise
        here = os.path.dirname(os.path.abspath(inspect.getfile(Schema)))
        print(here)
        with open(here + "/schema/schema.yml", "r") as stream:
            try:
                self._yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit()

    def subterms(self, term):
        terms = []
        for t in sorted(self._yaml['terms'], key = lambda pos: self._yaml['terms'][pos]['_position']):
            o = self._yaml['terms'][t]
            if o['scope'] == term['scope'] and 'super-term' in o.keys() and term['term'] == o['super-term']:
                terms.append(o)
        return terms

    def termsFor(self, typee):
        isContainer = False
        if typee == 'Container' or typee in map(lambda o:o['type'], self.containers()):
            isContainer = True
        terms = []
        for t in sorted(self._yaml['terms'], key = lambda pos: self._yaml['terms'][pos]['_position']):
            o = self._yaml['terms'][t]
            if 'super-term' not in o.keys() or o['super-term'] == '':
                if o['scope'] == 'Container' and isContainer:
                    terms.append(o)
                if o['scope'] == 'Component' and not isContainer:
                    terms.append(o)
        return terms

    def subtypes(self, typee):
        types = []
        for t in sorted(self._yaml['types'], key = lambda pos: self._yaml['types'][pos]['_position']):
            o = self._yaml['types'][t]
            if 'supertype-id' in o.keys() and typee == o['supertype-id']:
                types.append(o)
        return types

    def allsubtypes(self, typee):
        all = []
        types = self.subtypes(typee)
        all = all + types
        for t in types:
           all = all + self.allsubtypes(t['type'])
        return all
        

    def containers(self):
        return self.allsubtypes('Container')

    def components(self):
        return self.allsubtypes('Component')

    def types(self):
        types = []
        #sorted(student_Dict, key = lambda name: student_Dict[name].age)
        for t in sorted(self._yaml['types'], key = lambda pos: self._yaml['types'][pos]['_position']):
            o = self._yaml['types'][t]
            ks = ['type', 'label', 'supertype-id']
            t = {}
            for k in ks:
                if k in o:
                    t[k] = o[k]
            types.append(t)
        return types

    def terms(self):
        terms = []
        for t in sorted(self._yaml['terms'], key = lambda pos: self._yaml['terms'][pos]['_position']):
            o = self._yaml['terms'][t]
            terms.append(o)
        return terms
    def licences(self):
        licences = []
        for t in sorted(self._yaml['licences'], key = lambda pos: self._yaml['licences'][pos]['_position']):
            o = self._yaml['licences'][t]
            licences.append(o)
        return licences

    def asString(self, item, key):
        if key in item.keys():
            return item[key]
        else:
            return ''

# class MD:
#     def isComponent(self):
#         return True

# if __name__ == '__main__':
    # reeco = Schema()
    #     print(reeco.types())
    # out = eval("{ 'key': 1}")
#     out = eval("Schema()")
#     print(out, type(out))