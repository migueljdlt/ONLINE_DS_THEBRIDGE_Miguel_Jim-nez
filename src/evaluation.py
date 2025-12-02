#CLASIFICACION

# Evaluamos el mejor modelo en test

best_score_rf_clf = grid_search_clf.best_score_
best_rf_clf = grid_search_clf.best_estimator_
print(best_score_rf_clf)


y_pred_best_rf = best_rf_clf.predict(X_test_clf)
y_pred_proba_best_rf = best_rf_clf.predict_proba(X_test_clf)[:, 1]

# Calculamos métricas
accuracy_best_rf = accuracy_score(y_test_clf, y_pred_best_rf)
precision_best_rf = precision_score(y_test_clf, y_pred_best_rf)
recall_best_rf = recall_score(y_test_clf, y_pred_best_rf)
f1_best_rf = f1_score(y_test_clf, y_pred_best_rf)
roc_auc_best_rf = roc_auc_score(y_test_clf, y_pred_proba_best_rf)

# Visualizamos

print(" Accuracy: ", accuracy_best_rf)
print(" Precision: ", precision_best_rf)
print(" Recall: ", recall_best_rf)
print(" F1-Score: ", f1_best_rf)
print(" ROC-AUC: ", roc_auc_best_rf)


# REGRESION

# Ensemble RF optimizado + XGBoost sin optimizar

# Predicciones en escala log
y_pred_rf_log = best_rf_reg.predict(X_test_reg)
y_pred_xgb_log = pipeline_xgb_reg.predict(X_test_reg)  # Sin optimizar

# Promedio ponderado (30% RF, 70% XGBoost)
y_pred_ensemble_log = 0.3 * y_pred_rf_log + 0.7 * y_pred_xgb_log

# Convertir a escala original
y_pred_ensemble = np.exp(y_pred_ensemble_log)

# Evaluamos
r2_ensemble = r2_score(y_test_original, y_pred_ensemble)
rmse_ensemble = np.sqrt(mean_squared_error(y_test_original, y_pred_ensemble))
mae_ensemble = mean_absolute_error(y_test_original, y_pred_ensemble)

print("R²: ", r2_ensemble)
print("RMSE: ", rmse_ensemble/1e6, "M")
print("MAE: ", mae_ensemble/1e6, "M")

# Comparación
print("Comparación:")
print("RF optimizado: ", r2_best_rf_reg)
print("XGBoost original :",r2_xgb_reg)
print("Ensemble :", r2_ensemble)