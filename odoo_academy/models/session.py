# -*- coding: utf-8 -*-

from odoo import models, fields, api
from  datetime import timedelta
from odoo.exceptions import  UserError, ValidationError

class Session(models.Model):
    _name = 'academy.session'
    _description ='Session Info'
    
    course_id = fields.Many2one(comodel_name='academy.course',
                              string='Course',
                              ondelete='cascade',
                              required=True)
    #related field
    name = fields.Char(string = 'Title', related='course_id.name')
    instructor_id  =  fields.Many2one(comodel_name='res.partner',string='Instructor')
    student_ids =  fields.Many2many(comodel_name='res.partner', string='Students')
    start_date =   fields.Date(string='Start Date',
                              default=fields.Date.today)
    duration = fields.Integer(string='Session Days',
                              default=1)
    end_date =   fields.Date(string='End Date',
                             compute='_compute_end_date',
                             inverse='_inverse_end_date',
                             store=True)
    state = fields.Selection(string='States',
                            selection=[('draft','Draft'),
                                       ('open','In Progress'),
                                       ('done','Done'),
                                       ('complete','Complete')],
                            default='draft',
                            requirement=True)
    total_price = fields.Float(string='Total Price',
                              related='course_id.total_price')
    
    @api.depends('start_date','duration')
    def _compute_end_date(self):
        for record in self:
            if not (record.start_date and record.duration):
                record.end_date = record.start_date
            else:
                duration =  timedelta(days=record.duration)
                record.end_date =  record.start_date + duration
    
    def  _inverse_end_date (self):
        for record in self:
            if record.start_date  and  record.end_date:
                # ().days  --> convert to  days
                # +1 --> Monday  -  Thurdays  = 4days.  but  we consider  it  as  5 days
                record.duration = (record.end_date - record.start_date).days + 1
            else:
                continue