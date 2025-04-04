import pandas as pd
import json
import os


CSV_PATH = os.path.join(os.path.dirname(__file__), "Relatorio_cadop.csv")

df = pd.read_csv(CSV_PATH, delimiter=";", dtype=str)

df = df.where(pd.notna(df), None)

JSON_PATH = os.path.join(os.path.dirname(__file__), "Relatorio_cadop.json")

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=4)

print(f"JSON salvo em: {JSON_PATH}")