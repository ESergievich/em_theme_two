import os
from datetime import datetime

import pandas as pd

from config import DIRECTORY
from db import SpimexTradingResult, AsyncSessionLocal


def fetch_file_paths():
    return [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY)]


def parse_excel_file(path):
    df = pd.read_excel(path, header=[6, 7])
    df = df.iloc[:-2, 1:]
    df.columns = [' '.join([str(c) for c in col if 'Unnamed' not in str(c)]).strip() for col in df.columns]
    df = df[df['Наименование\nИнструмента'].notna()]
    df['Количество\nДоговоров,\nшт.'] = pd.to_numeric(df['Количество\nДоговоров,\nшт.'], errors='coerce')
    df = df[df['Количество\nДоговоров,\nшт.'] > 0]

    records = []
    for _, row in df.iterrows():
        product_id = row['Код\nИнструмента']
        exchange_product_name = row['Наименование\nИнструмента']
        delivery_basis_name = row['Базис\nпоставки']
        volume = float(row['Объем\nДоговоров\nв единицах\nизмерения'][0])
        total = float(row['Обьем\nДоговоров,\nруб.'][0])
        count = int(row['Количество\nДоговоров,\nшт.'])
        p = path.split('_')[-1]
        date = datetime.strptime(p[:8], "%Y%m%d").date()

        record = SpimexTradingResult(
            exchange_product_id=product_id,
            exchange_product_name=exchange_product_name,
            delivery_basis_name=delivery_basis_name,
            volume=volume,
            total=total,
            count=count,
            oil_id=product_id[:4],
            delivery_basis_id=product_id[4:7],
            delivery_type_id=product_id[-1],
            date=date,
        )
        records.append(record)
    return records


async def process_excel_files():
    file_paths = fetch_file_paths()
    all_records = []
    for path in file_paths:
        records = parse_excel_file(path)
        all_records.extend(records)
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add_all(all_records)
