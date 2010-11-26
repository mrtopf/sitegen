import os
import uuid

from quantumcore.resources import CSSResourceManager, CSSResource
from quantumcore.resources import JSResourceManager, JSResource
from jinja2 import Environment, FileSystemLoader

def generate_resources(cls, mgrcls, resourcelist, base, **kw):
    resources = []
    for no, line in enumerate(resourcelist.split()):
        if line.strip()=="":
            continue
        fp = open(os.path.join(base,line.strip()))
        data = fp.read()
        fp.close()
        res = cls(data, prio=no)
        resources.append(res)
    return mgrcls(resources, **kw)

def generate():

    env = Environment(loader=FileSystemLoader('pages'))
    base = os.getcwd()
    p = os.path.join(base,"config.py")
    fp = open(p,"r")
    config = fp.read()
    fp.close()
    exec(config)

    settings = {}
    settings['css'] = generate_resources(CSSResource, CSSResourceManager, CONFIG.css, base, prefix_url="/css")
    settings['js'] = generate_resources(JSResource, JSResourceManager, CONFIG.js, base, prefix_url="/js")
    settings['nonce'] = unicode(uuid.uuid4())

    output = CONFIG.output

    for name in os.listdir(os.path.join(base,"pages")):
        tmpl = env.get_template(name)
        out = tmpl.render(nonce=settings['nonce'], **CONFIG.template_vars)
        name, suffix = os.path.splitext(name)
        newname = "%s.html" %name
        p = os.path.join(output,newname)
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

if __name__=="__main__":
    generate()
