from datetime import datetime

import pandas as pd
from bq_easy_zfullio import Client
from google.cloud.bigquery import SchemaField


def prepare_realty(path_file: str) -> pd.DataFrame:
    df = pd.read_excel(path_file, sheet_name="Calls")
    df = df.rename(columns={"Дата/время": "datetime",
                            "Объект": "object",
                            "Входящий номер": "incoming_number",
                            "Внутренний номер": "internal_number",
                            "Длительность ожидания": "waiting_time",
                            "Длительность разговора": "call_duration",
                            "Рассчитанная стоимость звонка": "price",
                            "Тип объекта": "type"})
    df = df.astype({"datetime": "datetime64[ns]",
                    "object": str,
                    "incoming_number": str,
                    "internal_number": str,
                    "waiting_time": str,
                    "call_duration": str,
                    "price": int,
                    "type": str})
    df["date_upload"] = datetime.now()
    return df


def push_realty(path_file: str, bq_path_token: str, bq_project_id: str, bq_table: str) -> (datetime, datetime):
    df = prepare_realty(path_file)
    start_date: datetime = df["datetime"].min()
    finish_date: datetime = df["datetime"].max()
    schema = [SchemaField("datetime", "DATETIME"), SchemaField("object", "STRING"),
              SchemaField("incoming_number", "STRING"), SchemaField("internal_number", "STRING"),
              SchemaField("waiting_time", "STRING"), SchemaField("call_duration", "STRING"),
              SchemaField("price", "INT64"), SchemaField("type", "STRING"), SchemaField("date_upload", "DATETIME")]
    bq = Client(bq_path_token, bq_project_id)
    bq.upload_table(df, bq_table, schema)
    return start_date, finish_date


def prepare_cian(path_file: str) -> pd.DataFrame:
    df = pd.read_excel(path_file, sheet_name="Статистика звонков")
    df = df.rename(columns={"Id": "id", "Дата": "call_datetime", "Входящий номер": "incoming_number",
                            "Подменный номер клиента": "substitute_client_number",
                            "Подменный номер застройщика": "replacement_builder_number",
                            "Исходящий номер/SIP URI": "outgoing_number", "Название ЖК": "object", "Статус": "status",
                            "Статус ответа(только ОЗ)": "response_status",
                            "Разговор": "call_duration", "Тариф": "tariff", "Аукцион": "auction",
                            "Cписано в баллах": "written_in_points", "Тип": "type_of_call", "Тип лида": "type_of_lead",
                            "Сумма": "final_cost"})
    df["tariff"] = df["tariff"].replace({"\xa0": ""}, regex=True).astype(int)
    df["auction"] = df["auction"].replace({"\xa0": ""}, regex=True).astype(int)
    df["final_cost"] = df["final_cost"].replace({"\xa0": ""}, regex=True).astype(int)
    df["written_in_points"] = df["auction"].replace({"\xa0": ""}, regex=True).astype(int)
    df = df.astype(
        {"call_datetime": "datetime64[ns]", "tariff": int, "auction": int, "object": str, "call_duration": str,
         "incoming_number": str})
    df["date_upload"] = datetime.now()
    return df


def push_cian(path_file: str, bq_path_token: str, bq_project_id: str, bq_table: str) -> (datetime, datetime):
    df = prepare_cian(path_file)
    start_date: datetime = df["call_datetime"].min()
    finish_date: datetime = df["call_datetime"].max()
    schema = [SchemaField("id", "INT64"), SchemaField("call_datetime", "datetime"),
              SchemaField("incoming_number", "STRING"), SchemaField("substitute_client_number", "STRING"),
              SchemaField("replacement_builder_number", "STRING"), SchemaField("outgoing_number", "STRING"),
              SchemaField("object", "STRING"), SchemaField("status", "STRING"), SchemaField("call_duration", "STRING"),
              SchemaField("tariff", "INT64"), SchemaField("auction", "INT64"),
              SchemaField("written_in_points", "INT64"), SchemaField("type_of_call", "STRING"),
              SchemaField("type_of_lead", "STRING"), SchemaField("final_cost", "INT64"),
              SchemaField("date_upload", "DATETIME"),
              SchemaField("response_status", "STRING")
              ]
    bq = Client(bq_path_token, bq_project_id)
    bq.upload_table(df, bq_table, schema)
    return start_date, finish_date


def prepare_avito(path_file: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(path_file, encoding='cp1251')
    df = df.rename(columns={"Дата звонка": "date",
                            "Время звонка": "time",
                            "Длительность звонка в секундах": "call_duration",
                            "Кто звонил": "incoming_number",
                            "Кому звонили": "outgoing_number",
                            "Стоимость звонка в рублях": "final_cost",
                            "Статус звонка": "status",
                            "Регион": "geo",
                            "Группа": "object",
                            "id звонка": "id"})
    df["final_cost"] = df["final_cost"].str.replace(',', '.')
    df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.time
    df = df.astype({"date": "datetime64[ns]",
                    "call_duration": "int32",
                    "incoming_number": "string",
                    "outgoing_number": "string",
                    "final_cost": float,
                    "status": "string",
                    "geo": "string",
                    "object": "string",
                    "id": "string"})
    df["date_upload"] = datetime.now()
    return df


def push_avito(path_file: str, bq_path_token: str, bq_project_id: str, bq_table: str) -> (datetime, datetime):
    df = prepare_avito(path_file)
    start_date: datetime = df["date"].min()
    finish_date: datetime = df["date"].max()
    schema = [SchemaField("date", "DATE"),
              SchemaField("time", "TIME"),
              SchemaField("call_duration", "INT64"),
              SchemaField("incoming_number", "STRING"),
              SchemaField("outgoing_number", "STRING"),
              SchemaField("final_cost", "FLOAT64"),
              SchemaField("status", "STRING"),
              SchemaField("geo", "STRING"),
              SchemaField("object", "STRING"),
              SchemaField("id", "STRING"),
              SchemaField("date_upload", "DATETIME")]
    bq = Client(bq_path_token, bq_project_id)
    bq.upload_table(df, bq_table, schema)
    return start_date, finish_date


def prepare_novostroy_m(path_file: str) -> pd.DataFrame:
    df = pd.read_excel(path_file, sheet_name="Make-Connect.ru")
    df = df.rename(columns={"Дата": "date",
                            "Время": "time",
                            "Название РК": "campaign",
                            "Телефон абонента": "incoming_number",
                            "Длительность звонка": "call_duration",
                            "Спор": "dispute",
                            "Итоговый статус": "status",
                            "Признак звонка": "sign",
                            "Итоговая стоимость": "final_cost"
                            })
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.date
    df = df.astype({"campaign": str,
                    "incoming_number": str,
                    "call_duration": str,
                    "dispute": str,
                    "status": str,
                    "sign": str,
                    "final_cost": float
                    })
    df["date_upload"] = datetime.now()
    return df


def push_novostroy_m(path_file: str, bq_path_token: str, bq_project_id: str, bq_table: str) -> (datetime, datetime):
    df = prepare_novostroy_m(path_file)
    start_date: datetime = df["date"].min()
    finish_date: datetime = df["date"].max()
    schema = [SchemaField("date", "DATE"),
              SchemaField("time", "TIME"),
              SchemaField("campaign", "STRING"),
              SchemaField("incoming_number", "STRING"),
              SchemaField("call_duration", "STRING"),
              SchemaField("dispute", "STRING"),
              SchemaField("status", "STRING"),
              SchemaField("sign", "STRING"),
              SchemaField("final_cost", "FLOAT64"),
              SchemaField("date_upload", "DATETIME")]
    bq = Client(bq_path_token, bq_project_id)
    bq.upload_table(df, bq_table, schema)
    return start_date, finish_date
