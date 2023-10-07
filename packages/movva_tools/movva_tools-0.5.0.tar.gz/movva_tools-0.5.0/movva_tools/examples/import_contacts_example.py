from movva_tools.import_contacts import ImportContacts
from movva_tools.google_integration import GoogleSheetsIntegration
import pandas as pd
import asyncio
import time
import os


async def main():
    sheets_integration = GoogleSheetsIntegration(
        creds_path='movva_tools/credentials.json',
        spreadsheet_name='SPREADSHEET_NAME',
        link='LINK'
    )

    data = sheets_integration.read_sheet_data()

    dataframe = pd.DataFrame(data[1:], columns=data[0])

    rapidpro_integration = ImportContacts(
        url=os.environ.get('RAPIDPRO_URL'),
        organization_token=os.environ.get('ORGANIZATION_TOKEN')  # Encontrado no RapidPro
    )

    erase_contacts = False

    if erase_contacts:
        start_time = time.time()
        rapidpro_integration.set_client()
        rapidpro_integration.delete_contacts(group_name='imported 09/08/2023')
        end_time = time.time()
    else:
        start_time = time.time()
        await rapidpro_integration.import_contacts(df=dataframe)
        end_time = time.time()

    # Calcular o tempo total de execução
    execution_time = end_time - start_time

    if execution_time >= 60:
        # Caso o tempo de execução seja maior ou igual a 60 segundos,
        # faz a conversão para minutos e segundos
        minutes = int(execution_time // 60)
        seconds = execution_time % 60
        print(f"Tempo de execução: {minutes} minutos e {seconds:.4f} segundos")
    else:
        # Caso o tempo de execução seja menor que 60 segundos, mostra apenas em segundos
        print(f"Tempo de execução: {execution_time:.4f} segundos")

if __name__ == '__main__':
    asyncio.run(main())
