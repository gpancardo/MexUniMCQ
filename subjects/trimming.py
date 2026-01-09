from pathlib import Path
import pandas as pd
import json

# Leer
df = pd.read_json(Path(__file__).parent / "biologia.jsonl", lines=True, encoding='utf-8')

# Reducir a 250
while len(df) > 250:
    counts = df["tema"].value_counts()
    over = counts[counts > 10].index.tolist()
    if not over:
        break
    tema = pd.Series(over).sample(n=1).iloc[0]
    idx = df[df["tema"] == tema].sample(n=1).index
    df = df.drop(idx).reset_index(drop=True)

# Guardar SIN escapes Unicode
with open("biologia_250.jsonl", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        # Convertir la fila a dict y escribir con ensure_ascii=False
        f.write(json.dumps(row.to_dict(), ensure_ascii=False) + "\n")

print("Guardado con acentos reales (no escapes).")