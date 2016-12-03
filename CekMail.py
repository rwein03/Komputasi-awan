from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file 
from oauth2client import tools
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets


SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET = 'client_secret.json'

store = file.Storage('storage.json')
creds = store.get()
if creds is None or creds.invalid:
	flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPE)
	creds = tools.run_flow(flow, store)
GMAIL = build('gmail', 'v1', http=creds.authorize(Http()))

threads = GMAIL.users().threads().list(userId='me').execute().get('threads', [])
for thread in threads:
	tdata = GMAIL.users().threads().get(userId='me', id=thread['id']).execute()
	nmsgs = len(tdata['messages'])
	
	if nmsgs >= 2:
		msg = tdata['messages'][0]['payload']
		subject = ''
		for header in msg['headers']:
			if header['name'] == 'Subject':
				subject = header['value']
				break
		if subject:
			print '%s (%d msgs)' % (subject, nmsgs)