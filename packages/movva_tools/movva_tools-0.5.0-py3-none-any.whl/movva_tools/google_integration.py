import json
import os
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from movva_tools.constants import GoogleSheets


# If modifying these scopes, delete the file token.json.
SCOPES = GoogleSheets.READ_ONLY_SCOPE


class GoogleSheetsIntegration:

    def __init__(self, link, spreadsheet_page):
        self.__link = link
        self.spreadsheet_page = spreadsheet_page
        self.service = None
        self._secret_manager_service = None
        self.__spreadsheet_id = None

    def check_data(self):
        """
            Verifica se as informações necessárias para a classe
            foram informadas.
        """
        if not self.__link or not self.__spreadsheet_id or not self.spreadsheet_page:
            raise Exception('The spreadsheet link, name and id must be informed')

    def __extract_id_from_google_sheets_link(self):
        """
            Extrai o id do link da planilha do Google através do
            padrão de expressão regular
        """

        pattern = r'/d/([a-zA-Z0-9-_]+)'

        # Procura pelo padrão no link fornecido
        match = re.search(pattern, self.__link)

        # Se houver uma correspondência, retorna o ID encontrado, caso contrário, retorna None
        if match:
            return match.group(1)
        else:
            raise Exception('Planilha não encontrada.')

    def __fetch_credentials_data(self):

        environment = None
        token_path = None
        creds_path = os.environ.get('CREDENTIALS_API_GOOGLE_SHEETS', None)

        if not creds_path:
            token_path = os.environ.get('TOKEN_LOCAL_PATH', '')
            creds_path = os.environ.get('CREDENTIALS_LOCAL_PATH', None)
            environment = 'local'
        else:
            token_path = os.environ.get('TOKEN_API_GOOGLE_SHEETS', None)
            environment = 'production'

        if not creds_path or not token_path:
            raise ConnectionError('As credenciais da API do Google Sheets não foram informadas.')

        return creds_path, token_path, environment

    def _validate_google_sheets_token(self, creds, gsheets_token_path, environment):
        if environment == 'local':
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.

            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.__creds_path, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    print('Openning token.json file...')
                    with open(gsheets_token_path, 'w') as token:
                        token.write(creds.to_json())

        else:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        return creds

    def __authorize_google_sheets(self):
        """
            Cria/carrega credenciais de acesso da API do Google Sheets
            e inicia a conexão com a API.
        """
        creds_path, token_path, environment = self.__fetch_credentials_data()

        if environment != 'local':

            gsheets_token_path = json.loads(
                token_path
            )

            creds = Credentials.from_authorized_user_info(gsheets_token_path, SCOPES)
        else:
            gsheets_token_path = token_path

            if os.path.exists(gsheets_token_path):
                creds = Credentials.from_authorized_user_file(
                    gsheets_token_path, SCOPES
                )

        creds = self._validate_google_sheets_token(creds, gsheets_token_path, environment)

        # Create Google Sheets connection
        service = build('sheets', 'v4', credentials=creds)

        return service

    def read_sheet_data(self, end_selection: str = None) -> list:
        """
            Lê e armazena em uma estrutura de listas o conteúdo da planilha.
        """

        self.__spreadsheet_id = self.__extract_id_from_google_sheets_link()

        self.check_data()

        self.service = self.__authorize_google_sheets()

        # Call the Sheets API
        end_selection = end_selection if end_selection else 'BZ'
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.__spreadsheet_id,
            range=f'{self.spreadsheet_page}!A1:{end_selection}'
        ).execute()

        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        return values
