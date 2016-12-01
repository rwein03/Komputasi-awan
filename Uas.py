import base64
import httplib2

from email.mime.text import MIMEText

from oauth2client import tools
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

# create a message to send
message = MIMEText("Message goes here.")
message['to'] = "rwein03@gmail.com"
message['from'] = "momorenjr@gmail.com"
message['subject'] = "your subject goes here"
body = {'raw': base64.b64encode(message.as_string())}

# send it
try:
  message = (gmail_service.users().messages().send(userId="me", body=body).execute())
  print('Message Id: %s' % message['id'])
  print(message)
except Exception as error:
  print('An error occurred: %s' % error)