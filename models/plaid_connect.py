from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json

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


# get accounts

#client = Client(client_id=id_plaid, secret=id_secret, access_token='test_bofa')
#accounts = client.auth_get().json()

# get transactions

#client = Client(client_id=id_plaid, secret=id_secret, access_token='test_bofa')
#response = client.connect_get()
#transactions = response.json()

#print transactions
