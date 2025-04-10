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
├── data/
│   └── diabetes.csv
├── models/
│   └── diabetes_model.pkl
├── src/
│   ├── train_model.py
│   └── utils.py
├── app.py
└── requirements.txt
```

## 📊 Atributos utilizados

- Pregnancies
- Glucose
- BloodPressure
- SkinThickness
- Insulin
- BMI
- DiabetesPedigreeFunction
- Age

## 🎯 Saída do Modelo

- `0` → Não diabético
- `1` → Diabético