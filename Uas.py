import httplib2
import os
import logging

from oauth2client import tools
# from oauth2client import run
from oauth2client.file import Storage
# from oauth2client.client import AccessTokenRefreshError
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
import json

CLIENT_SECRETS_FILE = "client_secret.json"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = "Missing client secrets file"


def authenticate():
    httplib2.debuglevel = 4
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_READ_WRITE_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage("%s-oauth2.json")
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        print('invalid credentials')
        credentials = run_flow(flow, storage)

    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))

    tags = "classical music", "yehudi mehunin"
    body = dict(
        snippet=dict(
            title="some title",
            description="a  description",
            tags=tags,
            categoryId="4"
        ),
        status=dict(
            privacyStatus="Private"
        )
    )

    thingy = service.videos().insert(part=",".join(body.keys()), body=None, media_body=MediaFileUpload(
        "1977.mp4", mimetype="video/mp4", chunksize=1024 * 1024, resumable=False))

    thingy.execute()

authenticate()