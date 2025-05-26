# Pattern Classifier using 5-Neighborhood Cellular Automata

A novel machine learning classifier based on **2-state 5-neighborhood Cellular Automata (CA)** using **strictly single-length cycles** to perform pattern classification on real-world datasets.

> 📍 **Presented at 4th Asian Symposium on Cellular Automata Technology (ASCAT) 2025**
> 📍 **Selected for publication in Springer Nature** 

---

## 📌 Overview

This project explores the design and implementation of a pattern classifier using **5-neighborhood Cellular Automata (CA)**. The classifier uses binary CA rules with desirable cyclic behavior to effectively separate and classify input patterns into distinct classes.

Key highlights include:

* Use of **strictly single-length cycle CA**.
* Identification of **balanced and unbalanced rules** with stable attractor behavior.
* Encoding strategies for transforming real-world datasets for CA-based classification.
* Competitive performance against conventional classifiers like KNN, SVC, XGB, etc.

---

## 🧬 Cellular Automata (CA) Model

* **Type**: 2-state (0 or 1)
* **Neighborhood**: 5 cells (i.e., \[i-2, i-1, i, i+1, i+2])
* **Boundary Condition**: Null
* **Cycle Structure**: Strictly single-length cycles
* **Rule Format**: 32-bit binary string (e.g., `1114110`)
* **Rule Selection**:

  * Based on number of self-replicating Rule Min Terms (RMTs)
  * Balanced vs. unbalanced rule categorization
  * Cycle behavior observed for CA sizes 4 to 10

---

## 🧩 Data Encoding

Real-world data is encoded into binary strings compatible with the CA model.

* 🔢 **Continuous Features**: Frequency encoding (into 2–3 bins)
* 🏷️ **Categorical Features**: One-hot encoding
* 📏 **CA Size** = Total bits after encoding (e.g., 21 for Raisin dataset)

---

## 🏋️ Training Process

Each training instance evolves into an **attractor** using a chosen CA rule.

### Training Efficiency:

$\text{Efficiency} = \left(\frac{\sum_{i=1}^{k} A_i}{n}\right) \times 100$

Where:

* $n$ = number of training patterns
* $k$ = number of useful attractors
* $A_i$ = maximum number of class instances attracted to the $i^{th}$ attractor

---

## 🧪 Testing & Evaluation

Standard classification metrics are used:

* **Accuracy**
* **Precision**
* **Recall**
* **F1-score**

Comparison with traditional classifiers (KNN, LDA, SVC, XGB, Ridge, etc.) shows **competitive or better performance** across multiple datasets.

---

## 📊 Datasets Used

| Dataset       | Attributes | Instances | CA Size | Max Bin Size |
| ------------- | ---------- | --------- | ------- | ------------ |
| Raisin        | 7          | 900       | 21      | 3            |
| Rice          | 7          | 3810      | 21      | 3            |
| Breast Cancer | 9          | 116       | 18      | 2            |

---

## 📈 Results Summary

### 📌 Best Performing CA Rule: `1114110`

| Dataset       | Accuracy | Precision | Recall | F1-Score |
| ------------- | -------- | --------- | ------ | -------- |
| Raisin        | 85.71%   | 90.48%    | 90.48% | 90.48%   |
| Rice          | 75.00%   | 73.08%    | 88.37% | 80.00%   |
| Breast Cancer | 59.09%   | 55.00%    | 100%   | 70.97%   |

---

## 🧐 Comparative Analysis

* The selected CA rules exhibit **stable cyclic behavior** and a **moderate number of attractors** across CA sizes.
* CA classifiers outperform or match standard models on key metrics.
* Efficient encoding bridges the gap between raw tabular data and CA configuration.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).

---

## 📬 Contact

* **Priya Kumari** – [GitHub](https://github.com/pri998)
