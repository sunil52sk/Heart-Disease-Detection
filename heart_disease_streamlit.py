# -*- coding: utf-8 -*-
"""heart_disease_streamlit.ipynb
Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19WCT3nA1tHU45LWoUCryYtbOVXptxh9M
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import random

# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction Using GWO-Optimized Decision Tree",
    page_icon="🌲",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {background-color: #f9f9f9;}
    .stButton>button {background-color: #4CAF50; color: white;}
    .stSelectbox label, .stSlider label {font-weight: bold;}
    .metric-box {padding: 20px; border-radius: 10px; background-color: crimson; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.header("📁 Data & Parameters")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        target_col = st.selectbox("Select target column", df.columns)
    else:
        df = None
        target_col = None

    st.header("⚙️ GWO Parameters")
    pop_size = st.slider("Population size", 5, 30, 15)
    max_iter = st.slider("Max iterations", 10, 50, 30)

# Main content area
st.title("🌲 Heart Disease Prediction Using GWO-Optimized Decision Tree Classifier")
st.markdown("---")

if uploaded_file is not None and target_col is not None:
    # Data preparation
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Data preview
    st.subheader("📋 Data Preview")
    st.dataframe(df.head(), use_container_width=True)
    st.dataframe(df.tail(), use_container_width=True)
    # GWO implementation functions (from original code)
    # ... [Include all the GWO functions here] ...
    #=====================================================
    # 1. Read Data
    #===================================================== 
    df = pd.read_csv("E:\heart_disease_detection_streamlit\content\heart.csv")
    print(df.head())

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        test_size=0.2, 
        random_state=42,
        stratify=y
    )

    print(f"Training Data: {X_train.shape}, Testing Data: {X_test.shape}")

    #=====================================================
    # 2. GWO Implementation
    #=====================================================
    def decode_solution(wolf):
        criterion_code = int(round(wolf[0]))
        criterion = 'gini' if criterion_code == 0 else 'entropy'
        
        max_depth = int(round(wolf[1]))
        max_depth = np.clip(max_depth, 2, 10)
        
        min_samples_split = int(round(wolf[2]))
        min_samples_split = np.clip(min_samples_split, 2, 10)
        
        min_samples_leaf = int(round(wolf[3]))
        min_samples_leaf = np.clip(min_samples_leaf, 1, 10)
        
        return {
            'criterion': criterion,
            'max_depth': max_depth,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf
        }

    def initialize_population(pop_size, dim, bounds):
        population = []
        for _ in range(pop_size):
            wolf = np.array([random.uniform(bounds[i][0], bounds[i][1]) for i in range(dim)])
            population.append(wolf)
        return population

    def fitness_function(wolf, X, y):
        params = decode_solution(wolf)
        model = DecisionTreeClassifier(
            criterion=params['criterion'],
            max_depth=params['max_depth'],
            min_samples_split=params['min_samples_split'],
            min_samples_leaf=params['min_samples_leaf'],
            random_state=42
        )
        scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        return np.mean(scores)

    def update_position(wolf, alpha, beta, delta, a, dim, bounds):
        new_wolf = np.copy(wolf)
        for i in range(dim):
            r1 = random.random()
            r2 = random.random()
            A1 = 2*a*r1 - a
            C1 = 2*r2
            D_alpha = abs(C1*alpha[i] - wolf[i])
            X1 = alpha[i] - A1*D_alpha
            
            r1 = random.random()
            r2 = random.random()
            A2 = 2*a*r1 - a
            C2 = 2*r2
            
            D_beta = abs(C2*beta[i] - wolf[i])
            X2 = beta[i] - A2*D_beta
            
            r1 = random.random()
            r2 = random.random()
            A3 = 2*a*r1 - a
            C3 = 2*r2
            
            D_delta = abs(C3*delta[i] - wolf[i])
            X3 = delta[i] - A3*D_delta
            
            new_wolf[i] = (X1 + X2 + X3) / 3.0
            new_wolf[i] = np.clip(new_wolf[i], bounds[i][0], bounds[i][1])
        
        return new_wolf
    fitness_history = []
    def advanced_gwo(X, y, pop_size=10, max_iter=20):
        dim = 4
        bounds = [(0, 1), (2, 10), (2, 10), (1, 10)]
        
        wolves = initialize_population(pop_size, dim, bounds)
        fitness = [fitness_function(w, X, y) for w in wolves]
        
        alpha_idx = np.argmax(fitness)
        alpha = wolves[alpha_idx]
        alpha_fitness = fitness[alpha_idx]
        
        sorted_indices = np.argsort(fitness)[::-1]
        beta = wolves[sorted_indices[1]]
        beta_fitness = fitness[sorted_indices[1]]
        delta = wolves[sorted_indices[2]]
        delta_fitness = fitness[sorted_indices[2]]
        
        for iteration in range(max_iter):
            a = 2 - iteration*(2/max_iter)
            
            for i in range(pop_size):
                wolves[i] = update_position(wolves[i], alpha, beta, delta, a, dim, bounds)
                fitness[i] = fitness_function(wolves[i], X, y)
            
            alpha_idx = np.argmax(fitness)
            alpha = wolves[alpha_idx]
            alpha_fitness = fitness[alpha_idx]
            
            sorted_indices = np.argsort(fitness)[::-1]
            beta = wolves[sorted_indices[1]]
            beta_fitness = fitness[sorted_indices[1]]
            delta = wolves[sorted_indices[2]]
            delta_fitness = fitness[sorted_indices[2]]

            fitness_history.append(alpha_fitness) 
            
            print(f"Iteration {iteration+1}/{max_iter} | Best Fitness: {alpha_fitness:.4f}")
        
        return alpha, alpha_fitness

    # #=====================================================
    # # 3. Run GWO & Train Final Model
    # #=====================================================
    # best_wolf, best_fitness = advanced_gwo(X_train, y_train, pop_size=15, max_iter=30)
    # print("\nBest Wolf (raw vector):", best_wolf)
    # print("Best CV Accuracy (Alpha Fitness):", best_fitness)

    # best_params = decode_solution(best_wolf)
    # print("Best Hyperparameters:", best_params)

    # # Train final model
    # final_model = DecisionTreeClassifier(
    #     criterion=best_params['criterion'],
    #     max_depth=best_params['max_depth'],
    #     min_samples_split=best_params['min_samples_split'],
    #     min_samples_leaf=best_params['min_samples_leaf'],
    #     random_state=42
    # )
    # final_model.fit(X_train, y_train)

    

# Run GWO Optimization button
if uploaded_file is not None and target_col is not None:
    if st.button("🚀 Run GWO Optimization", use_container_width=True):
        with st.spinner("🔍 Optimizing hyperparameters..."):
            fitness_history.clear()
            best_wolf, best_fitness = advanced_gwo(X_train, y_train, pop_size=pop_size, max_iter=max_iter)
            best_params = decode_solution(best_wolf)

            # Train final model
            model = DecisionTreeClassifier(
                **best_params,
                random_state=42
            )
            model.fit(X_train, y_train)
            st.session_state.final_model = model
            y_pred = st.session_state.final_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)

            # Results display
            st.success("Optimization complete!")
            st.markdown("---")

            # Metrics columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<div class='metric-box'>📈 Best CV Accuracy: {:.4f}</div>".format(best_fitness),
                           unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='metric-box'>🎯 Test Accuracy: {:.4f}</div>".format(accuracy),
                           unsafe_allow_html=True)
            with col3:
                st.markdown("<div class='metric-box'>⚙️ Best Parameters: {} </div>".format(best_params),
                           unsafe_allow_html=True)

            # Visualizations
            st.markdown("---")
            col_viz1, col_viz2 = st.columns(2)

            with col_viz1:
                st.subheader("📈 Fitness Progress")
                fig1, ax1 = plt.subplots()
                ax1.plot(fitness_history, marker='o', color='#4CAF50')
                ax1.set_xlabel("Iteration", fontweight='bold')
                ax1.set_ylabel("Accuracy", fontweight='bold')
                plt.grid(True, alpha=0.3)
                st.pyplot(fig1)

            with col_viz2:
                st.subheader("📊 Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred)
                fig2, ax2 = plt.subplots()
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2)
                ax2.set_xlabel('Predicted', fontweight='bold')
                ax2.set_ylabel('Actual', fontweight='bold')
                st.pyplot(fig2)
# Prediction form
    st.markdown("---")
    st.subheader("🔮 Make a Prediction")
    with st.form("prediction_form", clear_on_submit=False):
        cols = st.columns(3)
        input_data = {}
        for i, feature in enumerate(X.columns):
            with cols[i % 3]:
                input_data[feature] = st.number_input(
                    f"{feature}",
                    value=float(X[feature].mean()),
                    step=0.1,
                    format="%.2f"
                )
        input_data_as_numpy_array = np.asarray(list(input_data.values()))
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
        if st.form_submit_button("Predict"):
            prediction = st.session_state.final_model.predict(input_data_reshaped)
            st.session_state.prediction = prediction[0]
            st.session_state.input_data = input_data

            # Log the prediction
            if 'prediction_log' not in st.session_state:
                st.session_state.prediction_log = []
            st.session_state.prediction_log.append({
                'input_data': input_data,
                'prediction': prediction[0]
            })

    if 'prediction' in st.session_state:
        # st.write("🔢 Input Data:")
        # for feature, value in st.session_state.input_data.items():
        #     st.write(f"{feature}: {value:.2f}")
        prediction_result = "does not have heart disease" if st.session_state.prediction == 0 else "has heart disease"
        st.markdown("<div class='metric-box'>🎯 The Person has {}</div>".format(prediction_result),
                           unsafe_allow_html=True)

else:
    st.warning("⚠️ Please upload a CSV file and select the target column to begin.")