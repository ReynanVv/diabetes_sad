# 🩺 Sistema de Apoio à Decisão - Predição de Diabetes

Este projeto é um SAD (Sistema de Apoio à Decisão) que prevê se um paciente tem diabetes com base em dados clínicos, utilizando um modelo de Machine Learning com uma interface interativa feita em Streamlit.

## ⚙️ Como usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Treinar o modelo

```bash
python src/train_model.py
```

### 3. Executar a interface

```bash
streamlit run app.py
```

## 📁 Estrutura do Projeto

```
diabetes_sad/
├── .streamlit/
│   └── config.toml
├── data/
│   ├── add_column.py           # Script auxiliar para inserção de colunas
│   ├── diabetes.csv            # Dataset principal de pacientes
│   ├── predicoes.csv           # Resultados salvos de predições realizadas
│   └── sugar.csv               # Dados de produção e consumo de açúcar por país
├── models/
│   └── diabetes_model.pkl      # Modelo treinado
├── pages/
│   ├── dashboard.py            # Dashboard com gráficos e análises
│   └── lote.py                 # Página para upload de CSVs em lote
├── src/
│   └── train_model.py          # Treinamento do modelo
├── app.py                      # Entrada principal da aplicação
├── requirements.txt            # Dependências do projeto
└── README.md
```

## 📊 Atributos utilizados no Modelo

- Pregnancies
- Glucose
- BloodPressure
- SkinThickness
- Insulin
- BMI
- DiabetesPedigreeFunction
- Age

> A coluna `Outcome` representa o diagnóstico:
> - `0` → Não diabético
> - `1` → Diabético

## 🔁 Funcionalidades

### ✅ Previsão individual:
- Formulário interativo para preencher dados de um paciente e obter a predição.

### 📂 Upload em lote:
- Interface para carregar um arquivo `.csv` com múltiplos pacientes e inserir os dados diretamente no dataset.

### 📊 Dashboard interativo:
- Visualização de gráficos sobre os diagnósticos realizados.
- Gráfico de pizza com a distribuição de casos.
- Gráfico de dispersão entre consumo/produção de açúcar por país e os diagnósticos de diabetes.

## 📥 Estrutura esperada do CSV para Upload em Lote

```csv
Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome,Country
6,148,72,35,0,33.6,0.627,50,1,India
1,85,66,29,0,26.6,0.351,31,0,India
...
```

## 📈 Fonte dos Dados de Açúcar

O arquivo `data/sugar.csv` contém dados de produção e consumo de açúcar entre 2018/19 e 2023/24 por país, organizados com as seguintes colunas:

```csv
Name,Action,2018/19,2019/20,2020/21,2021/22,2022/23,May2023/24
Brazil,production,29500,30300,42050,35450,38050,42010
Brazil,consumption,10600,10650,10150,9500,9500,9542
...
```

Esses dados são usados para análises visuais da relação entre consumo/produção de açúcar e o número de diagnósticos por país.
