# CLASIFICACION

# Entrenamos

grid_search_clf.fit(X_train_clf, y_train_clf)

# Análisis de los hiperparámetros

for param, value in grid_search_clf.best_params_.items():
    print(f"   {param}: {value}")

#REGRESION
#XGBOOST
# Entrenar

grid_search_xgb_reg.fit(X_train_reg, y_train_reg)

# Análisis de los hiperparámetros

print("Mejores Hiperparámetros:")
for param, value in grid_search_xgb_reg.best_params_.items():
    print(f"   {param}: {value}")
#RANDOM FOREST
# Entrenar

grid_search_reg.fit(X_train_reg, y_train_reg)

# Análisis de los hiperparámetros

print("Mejores Hiperparámetros:")
for param, value in grid_search_reg.best_params_.items():
    print(f"   {param}: {value}")
# Ensemble RF optimizado + XGBoost sin optimizar

# Predicciones en escala log
y_pred_rf_log = best_rf_reg.predict(X_test_reg)
y_pred_xgb_log = pipeline_xgb_reg.predict(X_test_reg)  # Sin optimizar

# Promedio ponderado (30% RF, 70% XGBoost)
y_pred_ensemble_log = 0.3 * y_pred_rf_log + 0.7 * y_pred_xgb_log

# Convertir a escala original
y_pred_ensemble = np.exp(y_pred_ensemble_log)