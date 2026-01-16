import json
import re
from pathlib import Path

# Carpeta donde está este script
BASE_DIR = Path(__file__).resolve().parent

input_path = BASE_DIR / "historia_universal.jsonl"
output_path = BASE_DIR / "historia_universal_sin_numeracion.jsonl"

pattern = re.compile(r"^\d+\.\s+")

if not input_path.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

with input_path.open("r", encoding="utf-8") as infile, \
     output_path.open("w", encoding="utf-8") as outfile:

    for line in infile:
        item = json.loads(line)
        if "pregunta" in item:
            item["pregunta"] = pattern.sub("", item["pregunta"])
        outfile.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Proceso terminado correctamente.")
print(f"Archivo generado: {output_path}")
