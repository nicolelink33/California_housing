import ibis
from ibis import _
import duckdb


CSV = "../data/processed/housing_with_county.csv"
OUT = "../data/processed/housing_with_county.parquet"
duckdb.execute(f"""
    COPY (SELECT * FROM read_csv_auto('{CSV}'))
    TO '{OUT}' (FORMAT PARQUET)
""")