""" The prototype pattern is useful when we have an existing object that 
needs to stay untouched and we want to create an exact copy of it, allowing changes
in some parts of the copy.
"""

import copy

class Website:
    def __init__(self, name, domain, description, author, **kwargs):
        """ Examples of optional attributes: category, creation date, technologies, keywords"""
        self.name = name
        self.domain = domain
        self.description = description
        self.author = author
        for key in kwargs:
            setattr(self, key, kwargs[key])

        def __str__(self):
            summary = [f"Website '{self.name}'\n"]
            infos = vars(self).items()
            ordered_infos = sorted(infos)
            for attr, val in ordered_infos:
                if attr == "name":
                    continue
                summary.append(f"{attr}: {val}\n")
            return ''.join(summary)
        
class Prototype:
    def __init__(self):
        self.objects = dict()

    def register(self, identifier, obj):
        self.objects[identifier] = obj
    
    def unregister(self, identifier):
        del self.object[identifier]

    def clone(self, identifier, **attrs):
        found = self.objects.get(identifier)
        if not found:
            raise ValueError(f"Incorrect object identifier: {identifier}")
        obj = copy.deepcopy(found)
        for key in attrs:
            setattr(obj, key, attrs[key])
        
        return obj
    
keywords = ("python", "data", "apis", "automation")
site_1 = Website("Content",
                 domain="content.com",
                 description="Content description",
                 author="Max Mustermann",
                 category="Blog",
                 keywords=keywords)
prototype = Prototype()
identifier = "ka-cg-1"
prototype.register(identifier, site_1)

site_2 = prototype.clone(identifier, 
                         name="ExtraContent",
                         domain="extracontent.com",
                         description="Experiment of original content.",
                         category="Membership",
                         creation_date="Today")

# Test
print(site_1 is site_2)