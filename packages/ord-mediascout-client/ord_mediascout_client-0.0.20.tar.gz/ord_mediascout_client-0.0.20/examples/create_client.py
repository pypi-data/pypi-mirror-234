from ord_mediascout_client import (
    ClientRelationshipType,
    CreateClientWebApiDto,
    GetClientsWebApiDto,
    LegalForm,
    ORDMediascoutClient,
    ORDMediascoutConfig,
)
from ord_mediascout_client.client import APIError, BadResponseError, UnexpectedResponseError

config = ORDMediascoutConfig(url='http://localhost:5000', username='username', password='password')

api = ORDMediascoutClient(config)

client = CreateClientWebApiDto(
    createMode=ClientRelationshipType.DirectClient,
    legalForm=LegalForm.JuridicalPerson,
    inn='7702070139',
    name='Test Client',
    mobilePhone='1234567890',
    epayNumber=None,
    regNumber=None,
    oksmNumber=None,
)

try:
    client = api.create_client(client)
    print(client)

    clients = api.get_clients(GetClientsWebApiDto())
    for client in clients:
        print(client)

except UnexpectedResponseError as ex:
    print('UnexpectedResponseError', ex)
    print('request:', ex.response.request.body)
    print('response:', ex.response.text)
except BadResponseError as ex:
    print('BadRequestError', ex)
    for er in ex.error.errorItems:
        print('  error:', er)
except APIError as ex:
    print('APIError', ex)
except Exception as ex:
    print('Exception', type(ex), ex)
    raise
