# Customer Analytics Dashboard – Online Retail Dataset

## 📌 Description du projet
Ce projet analyse les transactions d’un retailer en ligne basé au Royaume-Uni entre décembre 2010 et décembre 2011.  
L’objectif est de comprendre le comportement des clients, identifier les segments les plus rentables et proposer des actions business basées sur les données.

Le projet inclut :
- nettoyage des données
- analyse exploratoire (EDA)
- segmentation RFM
- visualisations interactives
- dashboard d’analyse client

---

## 📊 Dataset

**Source :** Online Retail Dataset (UCI Machine Learning Repository)  
**Période :** 01/12/2010 → 09/12/2011  
**Instances :** 541,909  
**Features :** 6  
**Type :** Transactionnel, Time-Series  
**Problèmes :**
- valeurs manquantes  
- doublons  
- retours produits  
- données non structurées (codes produits, descriptions)

Ce dataset est souvent utilisé dans les projets d’analyse client, mais la valeur du projet dépend de l’approche, des insights et de la qualité de l’analyse.

---

## 🎯 Objectifs business

- Identifier les clients les plus rentables  
- Comprendre les produits les plus vendus  
- Détecter les tendances saisonnières  
- Segmenter les clients avec la méthode **RFM**  
- Proposer des actions marketing basées sur les données  
- Visualiser les performances via un dashboard interactif

---

## 🛠️ Méthodologie

### 1. Préparation des données
- suppression des doublons  
- gestion des valeurs manquantes  
- filtrage des retours produits  
- création de nouvelles features (montant total, date de commande, etc.)

### 2. Analyse exploratoire (EDA)
- distribution des ventes  
- top produits  
- top clients  
- analyse par pays  
- saisonnalité des ventes

### 3. Segmentation RFM
- calcul Recency, Frequency, Monetary  
- scoring  
- classification des segments (Champions, Loyal, At Risk, etc.)

### 4. Dashboard
- visualisations interactives  
- filtres par pays, produit, segment client  
- KPIs principaux

---

## 📈 Résultats clés

- Les clients B2B génèrent une part importante du chiffre d’affaires  
- Forte saisonnalité autour des fêtes de fin d’année  
- Quelques produits représentent la majorité des ventes  
- Le segment “Champions” est le plus rentable  
- Les retours produits impactent significativement certaines catégories

---

## 📁 Structure du projet

customer-analytics-dashboard/
│── data/
│── notebooks/
│── src/
│── dashboard/
│── requirements.txt
│── README.md


---

## 🚀 Exécution du projet

### Installer les dépendances
pip install -r requirements.txt


### Lancer les notebooks
jupyter notebook



### Lancer le dashboard (si Streamlit)
streamlit run dashboard/app.py



---

## 🧰 Technologies utilisées

- Python  
- Pandas, NumPy  
- Matplotlib, Seaborn  
- Scikit-learn  
- Power BI / Streamlit  
- Git & GitHub

---

## 📬 Contact
Pour toute question ou suggestion, n’hésitez pas à ouvrir une **issue** ou un **pull request**.
