import pandas as pd


def set_prenome_column(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['PRENOME'] = df['NOME'].apply(lambda x: x.split()[0])
        return df
    except KeyError:
        raise KeyError('A chave NOME é obrigatória na planilha.')


def date_formatter(df: pd.DataFrame, birth_date_column: str) -> pd.DataFrame:
    df[f'{birth_date_column}_FORMATADA'] = pd.to_datetime(
        df[birth_date_column], format='"%Y-%m-%dT%H:%M:%SZ"'
    )

    df[f'{birth_date_column}_FORMATADA'] = df[f'{birth_date_column}_FORMATADA'].astype(str)

    return df
