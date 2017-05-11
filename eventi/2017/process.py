from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_sheet():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    spreadsheetId = '1n6dIIsgcZeb8Tm4T4dkNCNN9ZEvyzr2jNOvEVTNk944'
    rangeName = 'Elenco partecipanti!A:Z'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    return result

def main():
    print("collecting google sheet data")
    result = get_sheet()
    values = result.get('values', [])
    sheet = [dict(zip(values[0], row)) for row in values[1:]]

    print("{} rows read".format(len(sheet)))
    
    sheet.sort(key=lambda row: (row['cognome'], row['nome']))
    
    ROW_TEMPLATE = u'<b>{nome} {cognome}</b> - {affiliazione}, {paese}<br />'
    participants_html = u'\n'.join([ROW_TEMPLATE.format(**row) for row in sheet if row['nome']])
    speakers_html = u'\n'.join([ROW_TEMPLATE.format(**row) for row in sheet if row['gruppo'] == 'speaker'])

    #    print(speakers_html)
    
    BASE_TEMPLATE = file('base.html.in').read()
    
    for filename in ["index.html", "participants.html"]:
        TEMPLATE = file(filename + ".in").read()
        html = TEMPLATE.format(PARTICIPANTS=participants_html.encode('utf8'))
        html = BASE_TEMPLATE.format(BODY=html)
        with open(filename, "w") as out:
            print("writing file {}".format(filename))
            out.write(html)

if __name__ == '__main__':
    main()
