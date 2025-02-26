import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.decomposition import PCA

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['time'] = pd.to_datetime(df['time'])
    df['hour'] = df['time'].dt.hour
    df['day'] = df['time'].dt.day
    df['month'] = df['time'].dt.month
    return df

def feature_engineering(df):
    df['temp_variation'] = df['temp_c'] - df['feelslike_c']
    df['pressure_variation'] = df['pressure_mb'].diff().fillna(0)
    df['humidity_variation'] = df['humidity'].diff().fillna(0)
    df['wind_humidity_interaction'] = df['wind_kph'] * df['humidity']
    return df

def prepare_data(df):
    df = feature_engineering(df)
    
    X = df[['hour', 'temp_c', 'precip_mm', 'wind_kph', 'humidity', 'pressure_mb', 'temp_variation', 'pressure_variation', 'humidity_variation']]
    y = df[['temp_c', 'precip_mm', 'wind_kph', 'humidity', 'pressure_mb', 'vis_km']]
    
    return X, y

def optimize_rf_model(X_train, y_train):
    rf = RandomForestRegressor(random_state=42)
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    
    print(f"Best hyperparameters: {grid_search.best_params_}")
    return grid_search.best_estimator_

def train_xgboost(X_train, y_train):
    xgb_model = MultiOutputRegressor(xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=6, eta=0.1, random_state=42))
    xgb_model.fit(X_train, y_train)
    return xgb_model

def predict_next_hour(model, last_row):
    next_hour = (last_row['hour'] + 1) % 24
    next_hour_data = last_row.copy()
    next_hour_data['hour'] = next_hour

    X_next = next_hour_data[['hour', 'temp_c', 'precip_mm', 'wind_kph', 'humidity', 'pressure_mb', 'temp_variation']].values.reshape(1, -1)
    
    next_pred = model.predict(X_next)
    
    next_hour_data[['temp_c', 'precip_mm', 'wind_kph', 'humidity', 'pressure_mb', 'vis_km']] = next_pred[0]
    return next_hour_data

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred, multioutput='uniform_average')
    print(f"Mean Squared Error: {mse}")
    print(f"R² Score: {r2}")
    return y_test, y_pred

def plot_predictions(y_test, y_pred, idx, variable_name):
    plt.figure(figsize=(10, 6))
    plt.plot(y_test[variable_name].values, label=f'Actual {variable_name}', color='blue')
    plt.plot(y_pred[:, idx], label=f'Predicted {variable_name}', color='red', linestyle='--')
    plt.title(f'Actual vs Predicted {variable_name}')
    plt.legend()
    plt.show()


# Réduction de la dimensionnalité avec PCA
def apply_pca(X_train, X_test, n_components=0.95):
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    print(f"Variance explained by PCA: {pca.explained_variance_ratio_.sum()}")
    return X_train_pca, X_test_pca

def main():
    file_path = r'C:\Users\briac\Desktop\project finnal\part1\datag\data_weth\historical_data.csv'
    # file_path = 'C:/Users/briac/Desktop/project finnal/part1/datag/data_weth/historical_data.csv'
    # file_path = 'C:\\Users\\briac\\Desktop\\project finnal\\part1\\datag\\data_weth\\historical_data.csv'

    df = load_data(file_path)
    
    X, y = prepare_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    X_train_pca, X_test_pca = apply_pca(X_train, X_test)
    
    print("Optimisation du modèle Random Forest...")
    rf_model = optimize_rf_model(X_train_pca, y_train)
    
    print("Entraînement du modèle XGBoost...")
    xgb_model = train_xgboost(X_train_pca, y_train)
    
    print("Prédiction pour l'heure suivante avec XGBoost :")
    last_row = df.iloc[-1]
    next_hour_data = predict_next_hour(xgb_model, last_row)
    print(next_hour_data)
    
    print("Évaluation du modèle XGBoost :")
    y_test_values, y_pred_values = evaluate_model(xgb_model, X_test_pca, y_test)
    
    for idx, col_name in enumerate(y_test.columns):
        plot_predictions(y_test_values, y_pred_values, idx, col_name)

if __name__ == "__main__":
    main()
