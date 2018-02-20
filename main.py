#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class CalculateHandler(BaseHandler):
    def post(self):
        vnos_razdalja = float(self.request.get("razdalja"))
        vnos_pretvorba = int(self.request.get("izbira_pretvorbe"))

        if vnos_pretvorba == 1:
            rezultat = vnos_razdalja / 1.6


        elif vnos_pretvorba == 2:
            rezultat = vnos_razdalja * 1.6

        else:
            rezultat = "Prosimo izberite 1 za pretvorbo iz km v mi ali 2 za pretvorbo iz mi v km!"


        podatki={"rezultat": rezultat, "vnos_razdalja": vnos_razdalja, "vnos_pretvorba": vnos_pretvorba}
        return self.render_template("rezultat.html", podatki)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/pretvorba', CalculateHandler),
], debug=True)
