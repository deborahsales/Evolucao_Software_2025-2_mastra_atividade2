import os
import json
from huggingface_hub import InferenceClient
from git import Repo
from dotenv import load_dotenv
import concurrent.futures
from tqdm import tqdm


# --- 1. CONFIGURAÇÕES DE AMBIENTE ---
load_dotenv()

def get_env_int(key, default=None):
    """Auxiliar para converter variáveis de ambiente para inteiro com segurança."""
    value = os.getenv(key)
    if value is None:
        if default is not None:
            return default
        raise ValueError(f"ERRO: Variável obrigatória {key} não encontrada no .env")
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"ERRO: A variável {key} deve ser um número inteiro. Recebido: '{value}'")

os.environ["TOKENIZERS_PARALLELISM"] = "false"

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("ERRO: HF_TOKEN não encontrado no arquivo .env")

LIMIT_FILES_PER_TAG = get_env_int("LIMIT_FILES_PER_TAG", default=0)
MAX_TOKENS          = get_env_int("MAX_TOKENS", default=1000)
MAX_WORKERS         = get_env_int("MAX_WORKERS", default=16)

print(f"🚀 Configurações carregadas: Workers={MAX_WORKERS}, MaxTokens={MAX_TOKENS}, LimitFilesPerTag={LIMIT_FILES_PER_TAG}")

# --- 2. CONFIGURAÇÕES DE MODELOS E CAMINHOS ---
MODELS = {
    "qwen_small": "Qwen/Qwen2.5-Coder-3B-Instruct",
    "qwen_medium": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "qwen_larger": "Qwen/Qwen2.5-Coder-14B-Instruct"
}

ALLOWED_PACKAGE_DIRS = [
    "packages/core",
    "packages/memory",
    "packages/rag",
    "packages/agent-builder",
    "packages/server",
    "packages/auth",
    "packages/deployer",
    "packages/cli",
]

EXCLUDED_PATTERNS = [".test.", ".spec.", ".d.ts"]

PROMPT_TEMPLATE = """
Você é um especialista em engenharia de software e qualidade de código.

Analise o código-fonte abaixo e identifique possíveis CODE SMELLS,
considerando EXCLUSIVAMENTE a taxonomia de code smells apresentada no portal
Refactoring Guru (https://refactoring.guru/refactoring/smells).

Utilize SOMENTE os code smells pertencentes às seguintes categorias do
Refactoring Guru:
- Bloaters
- Object-Orientation Abusers
- Change Preventers
- Dispensables
- Couplers

NÃO invente novos code smells, NÃO utilize classificações fora dessa lista
e NÃO utilize sinônimos diferentes para os nomes oficiais.

A resposta DEVE ser apresentada EXCLUSIVAMENTE em formato JSON válido,
sem texto adicional, comentários ou explicações fora do JSON.

Utilize EXATAMENTE a seguinte estrutura:

{
  "code_smells": [
    {
      "name": "Nome exato do code smell conforme Refactoring Guru",
      "category": "Uma das categorias: Bloaters | Object-Orientation Abusers | Change Preventers | Dispensables | Couplers",
      "snippet": "Trecho de código relevante ou descrição precisa da localização",
      "justification": "Justificativa técnica detalhada",
      "impact": "Impacto potencial na manutenibilidade, legibilidade, desempenho e testabilidade",
      "refactoring": "Sugestão de refatoração alinhada ao Refactoring Guru"
    }
  ]
}

Caso nenhum code smell da lista seja identificado, retorne:

{
  "code_smells": []
}

Código:
"""

REPO_URL = "https://github.com/mastra-ai/mastra.git"
BASE_DIR = os.path.join(os.getcwd(), "mastra")

# --- 3. INICIALIZAÇÃO DO REPOSITÓRIO ---
if not os.path.exists(BASE_DIR):
    print(f"Clonando repositório em {BASE_DIR}...")
    Repo.clone_from(REPO_URL, BASE_DIR)
repo = Repo(BASE_DIR)

# --- 4. FUNÇÕES DE SUPORTE ---

def collect_source_files(base_dir):
    """Coleta arquivos TS/JS apenas das pastas src dos pacotes permitidos."""
    files_collected = []
    for pkg in ALLOWED_PACKAGE_DIRS:
        src_dir = os.path.join(base_dir, pkg, "src")
        if not os.path.exists(src_dir):
            continue
        for root, _, files in os.walk(src_dir):
            for file in files:
                full_path = os.path.join(root, file)
                # Verifica extensão e padrões excluídos
                if (full_path.endswith((".ts", ".js", ".tsx")) and 
                    not any(p in full_path for p in EXCLUDED_PATTERNS)):
                    
                    rel_path = os.path.relpath(full_path, base_dir)
                    files_collected.append((full_path, rel_path))
    return files_collected

def analyze_code_smells(file_content, model_id):
    client = InferenceClient(model=model_id, token=HF_TOKEN)
    prompt = f"{PROMPT_TEMPLATE}\n{file_content}"
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
            temperature=0.1
        )
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
        return json.loads(content)
    except Exception as e:
        return {"error": f"Erro no modelo {model_id}: {str(e)}"}

def process_task(task):
    file_path, rel_path, tag_name, model_alias, model_id = task
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
        if len(code.strip()) < 50:
            return None
        analysis = analyze_code_smells(code, model_id)
        return {"tag": tag_name, "model": model_alias, "file": rel_path, "analysis": analysis}
    except Exception as e:
        return {"tag": tag_name, "model": model_alias, "file": rel_path, "error": str(e)}

# --- 5. LOOP PRINCIPAL ---
tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)[:3]

for tag in tags:
    sanitized_tag_name = tag.name.replace('/', '_').replace('@', '')
    tag_file_name = f"resultados_parciais_{sanitized_tag_name}"
    
    print(f"\n🚀 Analisando Tag: {tag.name}")
    repo.git.checkout(tag.name, force=True)
    
    # Coleta de arquivos candidatos
    all_files_found = collect_source_files(BASE_DIR)

    if LIMIT_FILES_PER_TAG > 0:
        print(f"⚠️ Limitador ativo: Processando apenas {LIMIT_FILES_PER_TAG} arquivos de {len(all_files_found)} encontrados.")
        all_files_found = all_files_found[:LIMIT_FILES_PER_TAG]
    else:
        print(f"📂 Processando todos os {len(all_files_found)} arquivos encontrados.")

    # Criar tarefas para os modelos
    tasks = []
    for full_path, rel_path in all_files_found:
        for m_alias, m_id in MODELS.items():
            tasks.append((full_path, rel_path, tag.name, m_alias, m_id))

    tag_results = []
    for m_alias, m_id in MODELS.items():
        print(f"\n🧠 Iniciando processamento com modelo: {m_alias}")
        filename_with_model_alias = f"{tag_file_name}_{m_alias}.json"
        tag_file_path = os.path.join(os.getcwd(), filename_with_model_alias)
        
        # Cria tarefas apenas para o modelo atual
        current_model_tasks = []
        for full_path, rel_path in all_files_found:
            current_model_tasks.append((full_path, rel_path, tag.name, m_alias, m_id))

        # Executa as tarefas do modelo atual em paralelo (arquivos)
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(process_task, t) for t in current_model_tasks]
            for future in tqdm(concurrent.futures.as_completed(futures), 
                              total=len(futures), 
                              desc=f"Progresso {m_alias}"):
                res = future.result()
                if res:
                    tag_results.append(res)
        
        # Salva o arquivo após a conclusão de cada modelo para segurança
        with open(tag_file_path, "w", encoding="utf-8") as f:
            json.dump(tag_results, f, indent=4, ensure_ascii=False)

        tag_results = []

        print(f"💾 Resultados finais da tag {tag.name} com o modelo {m_alias} salvos em: {filename_with_model_alias}")

print(f"\n✅ Concluído!")