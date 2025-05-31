# 🧬 PLIP Interactions – Processamento e Modelagem de Interações Biológicas

Este projeto tem como objetivo a manipulação e modelagem de dados extraídos de arquivos `.txt` gerados pelo PLIP (Protein-Ligand Interaction Profiler). O foco está na leitura, parsing e estruturação orientada a objetos dessas interações, promovendo um fluxo de dados limpo, modular e reutilizável.

## 🚀 Funcionalidades

- Leitura robusta de arquivos com interações proteína-ligante
- Tratamento de erros e linhas incompletas
- Mapeamento e parsing de diferentes tipos de interações
- Modelagem dos dados com classes orientadas a objetos
- Integração de componentes em um fluxo automatizado
- Testes unitários para validação do sistema

---

## 🗂️ Estrutura do Projeto

```
<!--
📂 __pycache__/          # Arquivos temporários do Python
📜 .env                  # Variáveis de ambiente (não deve ser versionado em produção)
📜 .gitignore            # Arquivos e pastas ignorados no controle de versão
📜 exemple.env           # Exemplo de arquivo .env para configuração local
📜 files.py              # Módulo com funções gerais
📜 interactions.py       # Módulo principal para manipulação de interações
📜 LICENSE               # Licença do projeto
📜 main.py               # Script principal de execução
📜 report.txt            # Arquivo de entrada ou saída de interações

📌 Observações

✅ __pycache__/ é gerado automaticamente e geralmente ignorado no .gitignore.
✅ .env deve conter variáveis sensíveis e não deve ser enviado ao repositório (use o exemple.env como base).
✅ tabelas.py e tables.py parecem ter a mesma funcionalidade, apenas em idiomas diferentes — pode ser interessante padronizar.
✅ interactions.py, files.py e main.py são os módulos principais do projeto.

🚀 Projeto em desenvolvimento — contribuições são bem-vindas!
-->

```

---

## ⚙️ Requisitos

- Python 3.10+
- [venv] Ambiente virtual (recomendado)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/stefanybrier/plip_interactions.git
cd plip_interactions

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## 📌 Como Usar

1. Certifique-se de que o arquivo `reports.txt` está no diretório raiz do projeto.
2. Execute o script principal:

```bash
python main.py
```

O sistema irá processar as interações do arquivo, modelar os dados e instanciar objetos conforme o tipo de interação.

---

## 🧪 Testes

Execute os testes unitários com `pytest`:

```bash
pip install pytest
pytest tests/
```

---

## 📈 Etapas do Desenvolvimento

### 1. Análise Inicial e Leitura de Dados
- Configuração do repositório e ambiente virtual
- Leitura linha a linha do `reports.txt`
- Tratamento de linhas inválidas ou incompletas

### 2. Projeto e Modelagem de Dados
- Identificação de padrões
- Mapeamento por tipo de interação
- Parsing individualizado por tipo

### 3. Implementação de Classes
- Definição de métodos, atributos e relacionamentos
- Instanciação de objetos a partir do parsing

### 4. Integração e Fluxo de Dados
- Script controlador conectando leitura, parsing e modelagem
- Validação de fluxos com diferentes arquivos

### 5. Testes e Validação
- Testes unitários e correção de bugs
- Melhorias contínuas no código

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

> Projeto desenvolvido para fins educacionais e científicos, com foco em bioinformática e análise computacional de interações moleculares.
