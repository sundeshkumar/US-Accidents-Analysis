# 🚦 US Accidents Data Mining Project (2016–2023)

## 📌 Project Overview
This project analyzes a massive dataset of US traffic accidents to identify patterns, hotspots, and the influence of environmental factors on road safety. Using a dataset of **1 million records**, the project applies Data Mining and Machine Learning techniques to predict accident **Severity** (Scale 1–4) based on weather, time, and location data.

## 🎯 Research Questions
1. **Hotspots:** Which locations (States) have the highest frequency of accidents?
2. **Time Patterns:** How do accident rates change during rush hours, days of the week, and months?
3. **Environmental Impact:** Do Temperature, Humidity, Pressure ,Visibility and  Start_Lat,Start_Lng, influence how severe an accident is?
4. **Predictability:** Can we accurately predict accident severity using environmental variables?

## 🛠️ Tech Stack
* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Machine Learning:** Scikit-Learn (Random Forest Classifier)

---

## 📅 Project Roadmap & Methodology

### Week 1 - Data Selection and Problem Definition
### Week 2: Data Acquisition & Exploratory Data Analysis (EDA)
* **Data Loading:** Loaded a subset of **1,000,000 rows** from the dataset to optimize performance.
* **Initial Inspection:** Checked data shapes, types, and severity distribution.
* **Visual Insight:** Generated a Bar Chart showing accident counts across all US States to identify geographic hotspots.

### Week 3: Data Cleaning & Feature Engineering
* **Handling Missing Values:**
    * **Dropped Columns:** Removed columns with excessive missing data or low relevance: `End_Lat`, `End_Lng`, `Precipitation(in)`, `Wind_Chill(F)`.
    * **Imputation:** Filled missing environmental data (Temperature, Humidity, Pressure, Visibility, Wind Speed) with the **Median** value to maintain statistical integrity.
    * **Dropped Rows:** Removed remaining rows with null values to ensure a clean dataset.
* **Feature Extraction:**
    * Converted `Start_Time` to datetime objects.
    * Extracted new features: `Hour`, `Month`, and `Weekday`.
* **Sanity Check:** Validated that the dataset contained 0 missing values before modeling.

### Week 4 & 5: Modeling & Evaluation
* **Preprocessing:** Selected only numeric features and replaced infinite values with 0.
* **Algorithm:** Trained a **Random Forest Classifier** (`n_estimators=50`).
* **Split:** Used an 80/20 Train-Test split.
* **Evaluation:** Generated Accuracy Scores, Classification Reports, and Confusion Matrices.

---

## 📊 Key Insights & Visualizations

### 1. Geographic Hotspots
We analyzed the `State` column to see where accidents occur most frequently.
* *Observation:* A bar chart of state counts revealed that states with high populations and dense traffic networks are major hotspots.

### 2. Temporal Patterns (Rush Hour)
By plotting accidents by `Hour`:
* *Observation:* There is a distinct bimodal distribution with peaks during **morning (7–9 AM)** and **evening (4–6 PM)** rush hours, indicating traffic volume is a key driver of accident frequency.

### 3. Environmental Factors vs. Severity
We used Box Plots and Correlation Heatmaps to study weather impacts.
* *Observation:* While temperature and humidity show a spread across all severity levels, factors like **Visibility** and **Pressure** showed correlation with accident severity.

---

## 🤖 Model Performance

We trained a Random Forest model to predict Severity.

**Model Results:**
* **Accuracy:** 80.83%
* **Top Predictors:** The Feature Importance plot revealed that **Start_Lat, Start_Lng, and Hour** were the most significant factors in predicting severity, followed by environmental variables.

### Feature Importance
*(The model prioritized spatial and temporal features over purely environmental ones, suggesting that "Where" and "When" matter more than "Weather".)*

---

## 🚀 How to Run This Project
1.  **Download the Data:** Get the `US_Accidents_March23.csv` file from Kaggle.
2.  **Install Dependencies:**
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn
    ```
3.  **Update Path:** Change the file path in the code to match your local directory:
    ```python
    df = pd.read_csv(r"Your_Path_Here\US_Accidents_March23.csv", nrows=1000000)
    ```
4.  **Run the Notebook:**
    The analysis is divided into sequential steps (Cleaning -> Visualization -> Modeling). Run the Jupyter Notebook cells in order.

---

## 📢 Conclusion
This project successfully demonstrated that traffic accident severity is not random. By analyzing **1 million records**, we found that **Location (Lat/Lng)** and **Time of Day** are the strongest predictors of accidents. While environmental factors play a role, human factors (rush hour traffic) and infrastructure (location) are the primary drivers of accident severity.