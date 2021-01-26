# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import  UserError, ValidationError

class Course(models.Model):
    _name = 'academy.course'
    _description ='Course Info'
    
    name = fields.Char(string = 'Title', required=True)
    description = fields.Text(string='Description')
    level = fields.Selection(string='Level', 
                             selection=[('beginner', 'Beginner'),
                                        ('intermediate', 'Intermediate'),
                                        ('advanced', 'Advanced')
                                       ],
                            copy=False)
    
    active = fields.Boolean(string='Active', default=True)
    
    base_price =  fields.Float(string='Base  Price', default=0.00)
    additional_fee = fields.Float(string='Additional Fee', default=0.00)
    total_price =  fields.Float(string='Total Price',readonly=True)
    
    #one to many -->  link  with  session
    session_ids =  fields.One2many(comodel_name='academy.session',
                                  inverse_name='course_id',
                                  string='Sessions')

    
    #if base price / additional fee change trigger the method.
    #Add Exception, if base price <0 -->  error
    @api.onchange('base_price', 'additional_fee')
    def _onchange_total_price(self):
         #Add Exception, if base price <0 -->  error
        if self.base_price<0.00:
            raise UserError('Base Price  cannot be set as Negative.')
         #set total price = base price + additional fee
        self.total_price =  self.base_price +  self.additional_fee
        
    @api.constrains('additional_fee')
    def _check_additional_fee(self):
        for record in self:
            #  set additional_fee always greater than 10.00
            if  record.additional_fee < 0.00:
                raise ValidationError('Additional Fee cannot be less than 0.00: %s' % record.additional_fee)
                
        