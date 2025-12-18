import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "."

category_translation = {
    "Bloaters": "Inchaço de Código",
    "Change Preventers": "Dificultadores de Mudança",
    "Object-Orientation Abusers": "Abuso de Orientação a Objetos",
    "Dispensables": "Código Desnecessário",
    "Couplers": "Alto Acoplamento",
    "Primitive Obsession": "Obsessão por Tipos Primitivos",
    "Performance Hogs": "Problemas de Desempenho"
}

MODEL_MAP = {
    "qwen_small":  ("Qwen", "3B"),
    "qwen_medium": ("Qwen", "7B"),
    "qwen_larger": ("Qwen", "14B")
}

records = []

for file in os.listdir(DATA_DIR):
    if not file.endswith(".json"):
        continue

    file_path = os.path.join(DATA_DIR, file)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        for item in data:
            model_key = item.get("model")

            if model_key not in MODEL_MAP:
                continue

            model_name, model_size = MODEL_MAP[model_key]

            tag = item.get("tag", "unknown")

            for smell in item.get("analysis", {}).get("code_smells", []):
                records.append({
                    "arquivo": file,
                    "tag": tag,
                    "release": "release",
                    "modelo": model_name,
                    "modelo_tamanho": model_size,
                    "modelo_completo": f"{model_name}-{model_size}",
                    "categoria": smell.get("category"),
                    "categoria_pt": category_translation.get(
                        smell.get("category"), "Outros"
                    ),
                    "smell": smell.get("name"),
                    "impacto": smell.get("impact")
                })

df = pd.DataFrame(records)

print("Total de Code Smells:", len(df))
print(df.head())

if df.empty:
    raise RuntimeError("Nenhum Code Smell encontrado. Verifique os arquivos JSON.")

sns.set(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.countplot(
    data=df,
    x="modelo_completo",
    order=df["modelo_completo"].value_counts().index
)
plt.title("Quantidade de Code Smells por Modelo de IA")
plt.xlabel("Modelo")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(
    data=df,
    y="categoria_pt",
    hue="modelo_completo",
    order=df["categoria_pt"].value_counts().index
)
plt.title("Categorias de Code Smells por Modelo de IA")
plt.xlabel("Quantidade")
plt.ylabel("Categoria")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.countplot(
    data=df,
    y="tag",
    order=df["tag"].value_counts().index
)
plt.title("Quantidade de Code Smells por Tag (Mastra)")
plt.xlabel("Quantidade")
plt.ylabel("Tag")
plt.tight_layout()
plt.show()
