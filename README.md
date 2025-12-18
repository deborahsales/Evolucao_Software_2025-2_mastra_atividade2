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

A análise foi conduzida sobre o projeto **[mastra-ai/mastra](https://github.com/mastra-ai/mastra)**, considerando três releases do repositório e diferentes modelos de linguagem, com foco na **evolução da qualidade do software**.

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

A análise é **estritamente baseada na taxonomia de code smells do Refactoring Guru**, amplamente reconhecida na literatura de Engenharia de Software.

As categorias consideradas incluem, entre outras:

- Bloaters
- Object-Orientation Abusers
- Change Preventers
- Dispensables
- Couplers

⚠️ **Não são considerados smells fora dessa taxonomia**, nem categorias criadas ou inferidas pelos modelos.

---

## 🤖 Modelos de Linguagem Utilizados

Foram selecionados três LLMs disponibilizados na plataforma Hugging Face, com o objetivo de garantir diversidade de escala e comparar comportamentos analíticos:

| Identificador | Modelo | Parâmetros | Finalidade Experimental |
|--------------|--------|------------|--------------------------|
| `qwen_small` | Qwen/Qwen2.5-Coder-3B-Instruct | 3B | Modelo leve, referência mínima |
| `qwen_medium` | Qwen/Qwen2.5-Coder-7B-Instruct | 7B | Modelo intermediário |
| `qwen_large` | Qwen/Qwen2.5-Coder-14B-Instruct | 14B | Modelo mais robusto |

A escolha privilegia **modelos especializados em código**, com instruções ajustadas para tarefas de análise e explicação.

---

## 🔐 Gerenciamento Seguro do Token do Hugging Face

O acesso aos modelos de linguagem é realizado por meio de autenticação na plataforma **Hugging Face**.

Para garantir segurança:
- O token de acesso é armazenado utilizando um arquivo .env
- O token é referenciado apenas pela variável de ambiente `HF_TOKEN`
- Nenhuma credencial sensível é versionada ou exposta no repositório

---

## ⚙️ Pipeline de Análise

1. Extração incremental dos arquivos de código-fonte;
2. Envio controlado de trechos de código aos LLMs;
3. Solicitação explícita para identificação de code smells segundo o Refactoring Guru;
4. Estruturação da resposta em formato JSON;
5. Armazenamento dos resultados por modelo, arquivo e release.

Cada modelo é executado **de forma independente**, permitindo comparações diretas entre suas saídas.

---

### Execução Incremental e Checkpoints

Devido às limitações computacionais do ambiente, a análise é realizada de forma incremental:

- Processamento arquivo a arquivo;
- Persistência de resultados parciais (checkpoints);
- Possibilidade de retomada sem perda de dados.

Essa estratégia garante **robustez experimental e reprodutibilidade**.

---

## 📘 Documentação e Apresentação
📄 **[Abrir tutorial.pdf](./Tutorial.pdf)**  
🎥 **[Assistir vídeo explicativo](https://drive.google.com/file/d/1kXSKNRNi8SqEwAB2kTYX-Z8r6t7Zx1l2/view?usp=sharing)**
