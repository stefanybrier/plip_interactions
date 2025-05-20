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
📁 plip_interactions/
 ┣ 📂 classes/                 # Classes que representam interações biológicas
 ┣ 📂 utils/                   # Funções de leitura, parsing e manipulação
 ┣ main.py                    # Script principal de execução
 ┣ requirements.txt           # Dependências do projeto
📁 tests/                      # Testes unitários
 ┣ test_leitura.py
 ┣ test_classes.py
reports.txt                   # Arquivo de entrada com as interações
README.md
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
