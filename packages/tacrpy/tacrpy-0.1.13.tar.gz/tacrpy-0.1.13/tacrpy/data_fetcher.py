"""
Tento modul slouží k načtení různých zdrojů dat. V tuto chvíli umožňuje načíst \
data o projektech a uchazečích/příjemcích ze "zdroje pravdy" a IS VaVaI.
"""

import gspread
import pandas as pd


def projects(creds: object) -> pd.DataFrame:
    """ Načte data o projektech ze "zdroje pravdy" z googlesheets uloženého na Google disku.

    Lze použít pouze v rámci Google Colab prostředí.

    :param creds: údaje, které slouží k authenizaci v rámci Google Colab
    :return: DataFrame načtených dat ze zdroje
    """
    file_id = "1Ax1OYkdg3IA1YZki0fePizgQR6zOuzq7VGhFgeMorDQ"

    gc = gspread.authorize(creds)
    sht = gc.open_by_key(file_id)
    worksheet = sht.get_worksheet(0)

    rows = worksheet.get_all_values()

    df = pd.DataFrame.from_records(rows[1:], columns=rows[0])
    return df


def projects_finance(creds: object) -> pd.DataFrame:
    """ Načte data o financích projektů ze "zdroje pravdy" z googlesheets uloženého na Google disku.

    Finance jsou v rozdělení po jednotlivých letech.
    Lze použít pouze v rámci Google Colab prostředí.

    :param creds: údaje, které slouží k authenizaci v rámci Google Colab
    :return: DataFrame načtených dat ze zdroje
    """
    file_id = "1Ax1OYkdg3IA1YZki0fePizgQR6zOuzq7VGhFgeMorDQ"

    gc = gspread.authorize(creds)
    sht = gc.open_by_key(file_id)
    worksheet = sht.get_worksheet(1)

    rows = worksheet.get_all_values()

    df = pd.DataFrame.from_records(rows[1:], columns=rows[0])
    return df


def organizations(creds: object) -> pd.DataFrame:
    """ Načte data o uchazečích/příjemcích ze "zdroje pravdy" z googlesheets uloženého na Google disku.

    Lze použít pouze v rámci Google Colab prostředí.

    :param creds: údaje, které slouží k authenizaci v rámci Google Colab
    :return: DataFrame načtených dat ze zdroje
    """
    file_id = "1h7HpPn-G0_XY2gb_sExAQDkzR1TswGUH_2FuHCWhbRg"

    gc = gspread.authorize(creds)
    sht = gc.open_by_key(file_id)
    worksheet = sht.get_worksheet(0)

    rows = worksheet.get_all_values()

    df = pd.DataFrame.from_records(rows[1:], columns=rows[0])
    return df


def organizations_finance(creds: object) -> pd.DataFrame:
    """ Načte data o financích uchazečů/příjemců ze "zdroje pravdy" z googlesheets uloženého na Google disku.

    Finance jsou v rozdělení po jednotlivých letech.
    Lze použít pouze v rámci Google Colab prostředí.

    :param creds: údaje, které slouží k authenizaci v rámci Google Colab
    :return: DataFrame načtených dat ze zdroje
    """
    file_id = "1h7HpPn-G0_XY2gb_sExAQDkzR1TswGUH_2FuHCWhbRg"

    gc = gspread.authorize(creds)
    sht = gc.open_by_key(file_id)
    worksheet = sht.get_worksheet(1)

    rows = worksheet.get_all_values()

    df = pd.DataFrame.from_records(rows[1:], columns=rows[0])
    return df


def isvav_projects() -> pd.DataFrame:
    """ Načte data o příjemcích z otevřených dat IS VaVaI.

    Data jsou aktualizovaná cca jednou za čtvrt roku.

    :return: DataFrame načtených dat ze zdroje
    """
    df = pd.read_csv("https://www.isvavai.cz/dokumenty/open-data/CEP-projekty.csv")
    return df


def isvav_organizations() -> pd.DataFrame:
    """ Načte data o projektech z otevřených dat IS VaVaI.

    Data jsou aktualizovaná cca jednou za čtvrt roku.

    :return: DataFrame načtených dat ze zdroje
    """
    df = pd.read_csv("https://www.isvavai.cz/dokumenty/open-data/CEP-ucastnici.csv")
    return df
