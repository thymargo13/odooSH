# -*- coding:utf-8 -*-

from odoo import http

class Academy(http.Controller):
    #route -- everyone can see
    #website=True -- it is a website not just backend
    @http.route('/academy/', auth='public', website=True)
    def index(self, **kwargs):
        return "Hello World"
    
    @http.route('/academy/course/', auth='public', website=True)
    def course(self, **kwargs):
        #search all the courses
        courses = http.request.env['academy.course'].search([])
        #moduleName.templateId
        return http.request.render('odoo_academy.course_website',{
            'courses':courses,
        })
    
    @http.route('/academy/<model("academy.session"):session>/', auth='public', website=True)
    def session(self, session):
        return http.request.render('odoo_academy.session_website',{
            'session':session,
        })