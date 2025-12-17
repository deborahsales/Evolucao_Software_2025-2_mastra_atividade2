import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "."

records = []

# 🔤 Tradução das categorias
category_translation = {
    "Bloaters": "Inchaço de Código",
    "Change Preventers": "Dificultadores de Mudança",
    "Object-Orientation Abusers": "Abuso de Orientação a Objetos",
    "Dispensables": "Código Desnecessário",
    "Couplers": "Alto Acoplamento",
    "Primitive Obsession": "Obsessão por Tipos Primitivos",
    "Performance Hogs": "Problemas de Desempenho"
}

# 🔹 Ler todos os arquivos JSON
for file in os.listdir(DATA_DIR):
    if file.endswith(".json"):
        file_path = os.path.join(DATA_DIR, file)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for item in data:
                for smell in item.get("analysis", {}).get("code_smells", []):
                    records.append({
                        "file": item.get("file"),
                        "package": item.get("tag"),
                        "model": item.get("model"),
                        "smell_name": smell.get("name"),
                        "category": smell.get("category"),
                        "impact": smell.get("impact")
                    })

# 🔹 Criar DataFrame
df = pd.DataFrame(records)

# 🟢 Aplicar tradução
df["categoria_pt"] = df["category"].map(category_translation)

print("Total de Code Smells:", len(df))
print(df.head())

# =========================
# 📊 GRÁFICOS
# =========================

sns.set(style="whitegrid")

plt.figure(figsize=(10, 6))
sns.countplot(
    data=df,
    y="categoria_pt",
    order=df["categoria_pt"].value_counts().index
)
plt.title("Quantidade de Code Smells por Categoria")
plt.xlabel("Quantidade")
plt.ylabel("Categoria")
plt.tight_layout()
plt.show()

# # 🔸 Tipos de code smells
# plt.figure(figsize=(10, 6))
# sns.countplot(
#     data=df,
#     y="smell_name",
#     order=df["smell_name"].value_counts().index
# )
# plt.title("Tipos de Code Smells")
# plt.xlabel("Quantidade")
# plt.ylabel("Tipo")
# plt.tight_layout()
# plt.show()

# 🔸 Code smells por arquivo
# plt.figure(figsize=(12, 6))
# sns.countplot(
#     data=df,
#     x="file",
#     order=df["file"].value_counts().index
# )
# plt.title("Quantidade de Code Smells por Arquivo")
# plt.xlabel("Arquivo")
# plt.ylabel("Quantidade")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.show()

# # 🔸 Gráfico de pizza (categorias em PT-BR)
# category_counts = df["categoria_pt"].value_counts()
#
# plt.figure(figsize=(6, 6))
# plt.pie(
#     category_counts,
#     labels=category_counts.index,
#     autopct="%1.1f%%",
#     startangle=140
# )
plt.title("Distribuição Percentual de Code Smells por Categoria")
plt.tight_layout()
plt.show()
