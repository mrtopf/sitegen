import os
import uuid
import imp

from quantumcore.resources import CSSResourceManager, CSSResource
from quantumcore.resources import JSResourceManager, JSResource
from jinja2 import Environment, FileSystemLoader

class SiteGenerator(object):

    def __init__(self):
        """prepare site generator"""
        self.base = os.getcwd()
        self.env = Environment(loader=FileSystemLoader(self.base))
        fp, pathname, description = imp.find_module("config", [self.base])
        obj = imp.load_module("config", fp, pathname, description)
        self.config = obj.CONFIG
        self.nonce = unicode(uuid.uuid4())

    def generate_resources(self, cls, mgrcls, rtype, **kw):
        """generate a resource list"""
        resources = []
        for no, line in enumerate(getattr(self.config, rtype, "").split()):
            if line.strip()=="":
                continue
            name = line.strip()
            tmpl = self.env.get_template(rtype+"/"+name)
            out = tmpl.render(nonce=self.nonce, **self.config.template_vars)
            res = cls(out, prio=no)
            resources.append(res)
        return mgrcls(resources, **kw)

    def generate(self):

        # read the configuration


        #p = os.path.join(self.base,"config.py")
        #fp = open(p,"r")
        #config = fp.read()
        #fp.close()
        #exec(config)

        settings = {}
        settings['css'] = self.generate_resources(CSSResource, CSSResourceManager, "css", prefix_url="/css")
        settings['js'] = self.generate_resources(JSResource, JSResourceManager, "js", prefix_url="/js")
        settings['nonce'] = unicode(uuid.uuid4())

        output = self.config.output

        for name in os.listdir(os.path.join(self.base,"pages")):
            tmpl = self.env.get_template("pages/"+name)
            out = tmpl.render(nonce=self.nonce, **self.config.template_vars)
            #name, suffix = os.path.splitext(name)
            #newname = "%s.html" %name
            p = os.path.join(output,name)
            fp = open(p,"w+")
            fp.write(out)
            fp.close()

        # write JS
        for ofilename in settings['js'].filenames.keys():
            filename = ofilename.split("?")[0]
            filename = filename.split("/")[-1]
            fp = open(os.path.join(output,"js",filename),"w+")
            fp.write(settings['js'].get_payload(ofilename))
            fp.close()

        # write CSS
        for ofilename in settings['css'].filenames.keys():
            filename = ofilename.split("?")[0]
            filename = filename.split("/")[-1]
            fp = open(os.path.join(output,"css",filename),"w+")
            fp.write(settings['css'].get_payload(ofilename))
            fp.close()

def generate():
    g = SiteGenerator()
    g.generate()
