from movva_tools.flow_service import FlowCopyService
from movva_tools.google_integration import GoogleSheetsIntegration
import pandas as pd


def flow_copy_with_spreadsheets_whatsapp():
    integration = GoogleSheetsIntegration(
        link='spreadsheet_link',
        spreadsheet_page='Whatsapp',
        creds_path='credentials.json'
    )

    data = integration.read_sheet_data()

    # variável para auxiliar a colocar os parâmetros no serviço (opcional)
    df_aux = pd.DataFrame(data[1:], columns=data[0])

    base_flow_name = df_aux['FLUXO ORIGINAL'][0]
    flow_new_name = df_aux['NOVO FLUXO'][0]
    destination_organization_name = df_aux['ORGANIZACAO DESTINO'][0]
    origin_organization_name = df_aux['ORGANIZACAO ORIGEM'][0]

    service = FlowCopyService()

    service.clone(
        base_flow_name=base_flow_name,
        flow_suggested_name=flow_new_name,
        destiny_organization_name=destination_organization_name,
        origin_organization_name=origin_organization_name,
        data=data
    )


def flow_copy_with_spreadsheets_sms():
    integration = GoogleSheetsIntegration(
        link='spreadsheet_link',
        spreadsheet_page='SMS',
        creds_path='credentials.json'
    )

    data = integration.read_sheet_data()

    # variável para auxiliar a colocar os parâmetros no serviço (opcional)
    df_aux = pd.DataFrame(data[1:], columns=data[0])

    base_flow_name = df_aux['FLUXO ORIGINAL'][0]
    flow_new_name = df_aux['NOVO FLUXO'][0]
    destination_organization_name = df_aux['ORGANIZACAO DESTINO'][0]
    origin_organization_name = df_aux['ORGANIZACAO ORIGEM'][0]

    service = FlowCopyService()

    service.clone(
        base_flow_name=base_flow_name,
        flow_suggested_name=flow_new_name,
        destiny_organization_name=destination_organization_name,
        origin_organization_name=origin_organization_name,
        data=data
    )


if __name__ == "__main__":
    flow_copy_with_spreadsheets_whatsapp()
