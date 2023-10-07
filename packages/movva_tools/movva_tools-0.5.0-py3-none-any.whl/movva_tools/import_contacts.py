from temba_client.v2 import TembaClient
import asyncio

from datetime import datetime
from pandas import DataFrame
from movva_tools.utils import set_prenome_column
from more_itertools import chunked


class AsyncTembaClient(TembaClient):
    """
        Classe modificada do Client Python do RapidPro para criar requisições
        assíncronas aos recursos da API do RapidPro.
    """

    async def create_contact_async(
        self, name=None, language=None, urns=None, fields=None, groups=None
    ):
        """
        Asynchronously creates a new contact
        :param str name: full name
        :param str language: the language code, e.g. "eng"
        :param list[str] urns: list of URN strings
        :param dict[str,str] fields: dictionary of contact field values
        :param list groups: list of group objects, UUIDs or names
        :return: the new contact
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.create_contact, name, language, urns, fields, groups)


class ImportContacts:
    """
        Determina métodos para cadastrar contatos no RapidPro.
    """

    def __init__(self, url, organization_token) -> None:
        self.__url = url
        self.__organization_token = organization_token
        self.client = None
        self.contact_fields = []
        self.contact_labels = []
        self.pos_contacts_with_erros = []
        self.pos_contacts_with_success = []

    @staticmethod
    def break_list_into_groups(input_list, chunk_size=100) -> list:
        """
            Determina uma lista que contém lotes de tamanho informado em
            chunk_size.
        """
        return list(chunked(input_list, chunk_size))

    def set_client(self):
        """
            Inicia conexão com Client do RapidPro.
        """
        self.client = AsyncTembaClient(self.__url, self.__organization_token)
        return self.client

    def set_pattern_of_fields(self, fields: list):

        for index, field in enumerate(fields):
            fields[index] = field.upper()

        return fields

    def get_contact_fields_info(self) -> list:

        keys = self.client.get_fields().iterfetches(retry_on_rate_exceed=True)

        for register in keys:
            for f in register:
                self.contact_fields.append(f.key)
                self.contact_labels.append(f.key.upper())

    def insert_ddi_in_urns(self, numero):
        numero_str = str(numero)
        if numero_str.startswith('55'):
            return numero
        else:
            return '55' + numero_str

    def get_contact_fields_in_dataframe(self, dataframe: DataFrame):

        dataframe.rename(columns=lambda x: x.upper(), inplace=True)
        dataframe_fields = dataframe.columns

        intersection = set(self.contact_labels).intersection(dataframe_fields)

        df = dataframe.loc[:, list(intersection)]

        return df

    def create_group_contacts(self, suggested_group_name=None) -> str:
        """
            Cria um grupo para armazenar os contatos no padrão:
            imported_${dd/mm/aaaa} com data atual ou informado através
            do parâmetro suggested_group_name.
        """

        date = datetime.now().strftime("%d/%m/%Y")
        group_name = f'imported {date}'

        if suggested_group_name:
            group_name = suggested_group_name

        try:
            self.client.create_group(name=group_name)
        except Exception:
            return group_name

        return group_name

    def adjust_contact_fields_sheet(self, dataframe: DataFrame) -> list:

        dataframe.rename(columns=lambda x: x.lower(), inplace=True)

        return dataframe

    def set_tel_urn(self, urn: str) -> str:
        urn_pattern = 'tel:+'

        return f'{urn_pattern}{urn}'

    def set_whatsapp_urn(self, urn: str) -> str:
        urn_pattern = 'whatsapp:'

        return f'{urn_pattern}{urn}'

    def export_unsigned_contacts(self, df: DataFrame, export=True):
        """
            Filtra os contatos não cadastrados do DataFrame de contatos
            e com export=True, cria um arquivo excel com os dados dos contatos
            não cadastrados.
        """
        contatos_nao_cadastrados = df.iloc[self.pos_contacts_with_erros]

        if export:
            contatos_nao_cadastrados.to_excel('nao_cadastrados.xlsx')

        return contatos_nao_cadastrados

    def process_contacts(self, df: DataFrame, group_name=None, prenome_given=True) -> (DataFrame, str):
        """
            Método que predefine o fluxo de cadastro de contatos a partir de um dataframe.
        """

        self.set_client()

        self.get_contact_fields_info()

        df = self.get_contact_fields_in_dataframe(dataframe=df)

        if prenome_given:
            df = set_prenome_column(df)

        self.adjust_contact_fields_sheet(df)

        group = self.create_group_contacts(suggested_group_name=group_name)

        return (df, group)

    async def create_contact_async(self, payload, group, df, index):
        """
            Cadastra os contatos no Rapidpro e verifica se houve alguma
            falha na requisição de cadastro.
        """

        try:
            # Utiliza o método assíncrono da classe AsyncTembaClient
            response = await self.client.create_contact_async(
                name=payload['nome'],
                urns=[
                    self.set_tel_urn(payload['celular']),
                    self.set_whatsapp_urn(payload['celular'])
                ],
                fields=payload,
                groups=[group]
            )

            # Verificar se o cadastro foi bem-sucedido
            if not hasattr(response, 'uuid') and index not in self.pos_contacts_with_success:
                # Armazena a posição do contato que falhou no cadastro.
                self.pos_contacts_with_erros.append(index)
            else:
                self.pos_contacts_with_success.append(index)

        except Exception as e:
            # Armazena a posição do contato que falhou no cadastro.
            print(f"Erro ao cadastrar contato n° {index}: {e}")
            self.pos_contacts_with_erros.append(index)

        return self.pos_contacts_with_erros

    async def create_contacts_in_batches(
        self, payloads, group, batch_size=100
    ):
        """
            Cria lotes de contatos para evitar gargalos e facilitar rotina assíncrona.
        """
        # Divide a lista de payloads em lotes menores
        batches = [payloads[i:i + batch_size] for i in range(0, len(payloads), batch_size)]

        results = []

        for batch in batches:
            tasks = [self.create_contact_async(payload, group, batch, index) for index, payload in enumerate(batch)]
            # Executa as tarefas de criação em lote de forma assíncrona
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

        return results

    async def import_contacts(self, df: DataFrame, group_name=None, urn_column=None):

        """
            Cadastra os contatos de um DataFrame no RapidPro.
        """

        df, group = self.process_contacts(df, group_name)

        df = df.fillna('')

        df['celular'] = df['celular'].apply(self.insert_ddi_in_urns)

        # Cria uma lista de payloads com os dados de cada contato
        payloads = [row.to_dict() for _, row in df.iterrows()]

        # Executa a criação de contatos em lotes de forma assíncrona
        await self.create_contacts_in_batches(payloads, group)

        nao_cadastrados = self.export_unsigned_contacts(df, export=False)

        if not nao_cadastrados.empty:
            print('Alguns contatos não foram cadastrados com sucesso. Um arquivo será gerado com os contatos não cadastrados...')
        else:
            print('Contatos cadastrados com sucesso!')

        self.export_unsigned_contacts(nao_cadastrados)

    def delete_contacts(self, group_name=None, contact_id_list=None):
        if group_name:
            contacts_cursor = self.client.get_contacts(
                group=group_name
            ).iterfetches(retry_on_rate_exceed=True)

            contacts = []
            for register in contacts_cursor:
                for contact in register:
                    contacts.append(contact.uuid)

            grouped_list = self.break_list_into_groups(contacts)
            for contacts_list in grouped_list:

                try:
                    self.client.bulk_delete_contacts(contacts=contacts_list)
                except Exception as e:
                    pass

        else:
            grouped_list = self.break_list_into_groups(contact_id_list)

            for contacts_list in grouped_list:

                try:
                    self.client.bulk_delete_contacts(contacts=contacts_list)
                except Exception as e:
                    pass
