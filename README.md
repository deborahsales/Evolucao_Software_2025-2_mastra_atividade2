# 🧾 Evolução de Software 2025-2

### Equipe 4

01 - Carlos Eduardo Dias dos Santos - 202100104941  
02 - Déborah Abreu Sales - 202100060758  
03 - Eduardo Afonso Passos Silva - 201800102096  
04 - Guilherme Ilan Barboza Carvalho - 201900051196  
05 - Marcelo Venicius Almeida Lima - 202000012981  
06 - Mikael Douglas Santos Farias - 201700053275  
07 - Raí Rafael Santos Silva – 202000138043  
08 - Matheus Soares Santana - 201800147786

# 🔍 Análise de Code Smells com LLMs

Este repositório contém a **pipeline automatizada de análise de code smells** desenvolvida como parte de uma atividade acadêmica, utilizando **modelos de linguagem de grande porte (LLMs)** para identificar problemas de qualidade de código com base **exclusiva na taxonomia do Refactoring Guru**.

A análise foi conduzida sobre o projeto **[mastra-ai/mastra](https://github.com/mastra-ai/mastra)**, considerando múltiplas releases do repositório e diferentes modelos de linguagem, com foco na **evolução da qualidade do software**.

---

## 📌 Objetivo

O objetivo desta atividade é:

- Identificar *code smells* no projeto selecionado pela equipe na Atividade 1, usando a taxonomia do **Refactoring Guru**.
- Utilizar **três modelos de linguagem diferentes** da plataforma **Hugging Face** para analisar o código-fonte.
- Comparar os resultados obtidos pelos modelos, avaliando a precisão e as justificativas técnicas.
- Avaliar a **efetividade dos modelos de linguagem** na identificação de *code smells*.
- Analisar a **evolução da qualidade do código** ao longo das releases do projeto.
- **Documentar todo o processo experimental** e disponibilizar no **GitHub**.
- Produzir um **tutorial em PDF** e um **vídeo explicativo** sobre o processo e os resultados.

---

## 🧠 Taxonomia de Code Smells

A análise segue **estritamente** a taxonomia definida pelo portal **Refactoring Guru**, limitada às seguintes categorias:

- **Bloaters**
- **Object-Orientation Abusers**
- **Change Preventers**
- **Dispensables**
- **Couplers**

⚠️ Não são utilizados sinônimos, categorias alternativas ou classificações externas.

---

## 🧪 Ambiente de Execução

A pipeline foi desenvolvida e executada no ambiente **Google Colab (Free Tier)**, escolhido por sua acessibilidade e facilidade de reprodução dos experimentos.

### Limitações consideradas:
- Memória RAM limitada
- Tempo máximo de execução da sessão
- Possíveis desconexões inesperadas

Essas restrições motivaram decisões de projeto voltadas à **execução incremental**, **persistência frequente dos resultados** e **processamento em lotes (batching)**.

---

## 🔐 Gerenciamento Seguro do Token do Hugging Face

O acesso aos modelos de linguagem é realizado por meio de autenticação na plataforma **Hugging Face**.

Para garantir segurança:
- O token de acesso é armazenado utilizando o recurso **Secrets do Google Colab**
- O token é referenciado apenas pela variável de ambiente `HF_TOKEN`
- Nenhuma credencial sensível é versionada ou exposta no repositório

---

## ⚙️ Pipeline de Análise

A pipeline foi implementada em Python e estruturada nas seguintes etapas:

1. **Instalação dinâmica das dependências**
2. **Autenticação no Hugging Face**
3. **Clonagem do repositório do projeto analisado**
4. **Seleção das releases (tags)**
5. **Coleta dos arquivos-fonte relevantes**
6. **Análise assistida por modelos de linguagem**
7. **Persistência incremental dos resultados**
8. **Consolidação final em arquivo JSON**

Cada modelo é executado de forma **independente**, evitando carregamento simultâneo e reduzindo o consumo de memória.

---

## 📂 Seleção dos Arquivos Analisados

A análise é restrita aos arquivos:

- Localizados em diretórios `src`
- Pertencentes aos packages selecionados do monorepo
- Escritos em **JavaScript** e **TypeScript**

Arquivos de configuração, testes, documentação, exemplos e artefatos de build são **explicitamente excluídos**, a fim de reduzir ruído e focar na lógica central do sistema.

---

## 🤖 Modelos de Linguagem Utilizados

Os modelos são configurados e executados de forma modular. Exemplo de mapeamento:

```python
MODELS = {
    "qwen_small": "Qwen/Qwen2.5-Coder-3B-Instruct",
    "qwen": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "starcoder": "bigcode/starcoder2-7b"
}
```
---

## 📤 Formato da Saída

Os resultados são armazenados em arquivos JSON, organizados por:

- Release do projeto
- Arquivo analisado
- Modelo de linguagem utilizado

Cada entrada segue o formato:

    
    {
    "code_smells": [
        {
        "name": "Nome do code smell",
        "category": "Categoria Refactoring Guru",
        "snippet": "Trecho de código ou localização",
        "justification": "Justificativa técnica",
        "impact": "Impactos potenciais",
        "refactoring": "Sugestão de refatoração"
        }
    ]
    }


Caso nenhum code smell seja identificado:

    
    {
    "code_smells": []
    }
    
---
## ♻️ Execução Incremental e Reprodutibilidade

Para garantir reprodutibilidade e tolerância a falhas:

- Os resultados são salvos após o processamento de cada arquivo
- A execução pode ser retomada a partir do último checkpoint
- O arquivo incremental é posteriormente consolidado como saída final

Essa abordagem evita retrabalho em caso de falhas ou interrupções do ambiente.

---
## 📘 Notebook Principal

O experimento completo está documentado no notebook:


📓 [`mastra_code_smell_analysis.ipynb`](./mastra_code_smell_analysis.ipynb)

Este notebook contém todo o código necessário para reprodução do experimento, desde a preparação do ambiente até a geração do arquivo final de resultados.