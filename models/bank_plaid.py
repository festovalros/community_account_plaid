from odoo import api, fields, models
import logging

#from . import plaid_connect
from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json


_logger = logging.getLogger(__name__)


class PlaidAccountJournal(models.Model):
    _inherit = 'account.journal'

    plaid_user = fields.Char('Plaid User')
    plaid_password = fields.Char('Plaid Password')
    access_token = fields.Char('Access Token', help="Acess Token provided by Plaid API")
    plaid_active = fields.Boolean('Active for Plaid')


class AccountBankStatementPlaid(models.Model):
    _inherit = "account.bank.statement"

    #_name = 'prueba'
    campo_prueba = fields.Char('prueba')

    id_plaid = '584f8ac239361943b6a40c2f'
    id_secret = '2eb94d1cfb298020b6d4c1e396eb75'
    bank_user = 'play_test'
    bank_pass = 'play_good'


    client = Client(client_id=id_plaid, secret=id_secret)
    account_type = 'bofa'

    try:
        response = client.connect(account_type, {
         'username': bank_user,
         'password': bank_pass
        })
    except plaid_errors.PlaidError, e:
         pass
    else:
        if response.status_code == 200:
            # User connected
            data = resposnse.json()
        elif response.stat_code == 201:
            # MFA required
            try:
                mfa_response = answer_mfa(response.json())
            except plaid_errors.PlaidError, e:
                pass
            else:
                None
                # check for 200 vs 201 responses
                # 201 indicates that additional MFA steps required
            

    def answer_mfa(data):
        if data['type'] == 'questions':
            # Ask your user for the answer to the question[s].
            # Although questions is a list, there is only ever a
            # single element in this list, at present
            return answer_question([q['question'] for q in data['mfa']])
        elif data['type'] == 'list':
            return answer_list(data['mfa'])
        elif data['type'] == 'selection':
            return answer_selections(data['mfa'])
        else:
            raise Exception('Unknown mfa type from Plaid')


    def answer_question(questions):
        # We have magically inferred the answer
        # so we respond immediately
        # In the real world, we would present questions[0]
        # to our user and submit their response
        answer = 'tomato'
        return client.connect_step(account_type, answer)


    def answer_list(devices):
        # You should specify the device to which the passcode is sent.
        # The available devices are present in the devices list
        return client.connect_step('bofa', None, options={
            'send_method': {'type': 'phone'}
        })


    def answer_selections(selections):
        # We have magically inferred the answers
        # so we respond immediately
        # In the real world, we would present the selection
        # questions and choices to our user and submit their responses
        # in a JSON-encoded array with answers provided
        # in the same order as the given questions
        answer = json.dumps(['Yes', 'No'])
        return client.connect_step(account_type, answer)

    
    @api.multi
    def load_statements_line_from_plaid(self,id_plaid = '584f8ac239361943b6a40c2f', id_secret = '2eb94d1cfb298020b6d4c1e396eb75',access_token='test_bofa'):
        # get transactions
        _logger.warning('\n\n\n Respuesta1: \n \n\n\n')

        
        client = Client(client_id=id_plaid, secret=id_secret, access_token='test_bofa')
        #PARA DELIMITAR CON FECFA response = client.connect_get(opts={'gte':'2014-06-01'}).json()
        response = client.connect_get().json()
        accounts = client.auth_get().json()
        #transactions = response.json()
        
        _logger.info('\n\n\n transaccion: \n %s \n\n\n' % response['transactions'][0])
        
        _logger.info('\n\n\n Numero de Cuenta: \n %s \n\n\n' % accounts['accounts'][2]['numbers']['account'])
        _logger.info('\n\n\n id de la cuenta: \n %s \n\n\n' % accounts['accounts'][2]['_id'])
        _logger.info('\n\n\n id de la Cuenta en la transaccion: \n %s \n\n\n' % response['transactions'][0]['_account'])
        _logger.info('\n\n\n Monto de la transaccion: \n %s \n\n\n' % response['transactions'][0]['amount'])
        _logger.info('\n\n\n fecha de la transaccion: \n %s \n\n\n' % response['transactions'][0]['date'])
        _logger.info('\n\n\n nombre del partner que realiza transaccion: \n %s \n\n\n' % response['transactions'][0]['name'])

        #for account in accounts['accounts']:

        values = []
        for resp in response['transactions']:
            values.append((0,0,{'name': resp['name'],
        						'ref': resp['_id'],
        						'amount': resp['amount'],
        						'date': resp['date']
        						}))

        #OBSOLETO
        #new_id = self.env['account.bank.statement'].create({'name':"Prueba5", 'journal_id':6, 'line_ids': [(0,0,{'name': 'pruebaline', 'ref': '00002-line', 'amount': 100})]})
        #new_id = self.env['account.bank.statement'].create({'name':"Prueba5", 'journal_id':6, 'line_ids': [(0,0,{'name': response['transactions'][0]['name'],
        #																										 'ref': response['transactions'][0]['_id'],
        #																										 'amount': response['transactions'][0]['amount'],
        #																										 'date': response['transactions'][0]['date']
        #																										 })]})
        #

        new_id = self.env['account.bank.statement'].create({'name':"Prueba5", 'journal_id':6, 'line_ids': values})
        return True
