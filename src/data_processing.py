#CLASIFICACION

# Definimos los hiperparámetros

param_grid_clf = {
    'classifier__n_estimators': [200, 300, 500],
    'classifier__max_depth': [5, 7, 10],
    'classifier__min_samples_split': [5, 10, 20],
    'classifier__min_samples_leaf': [2, 5, 10]
}

grid_search_clf = GridSearchCV(
    estimator=pipeline_rf,
    param_grid=param_grid_clf,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=2,
    return_train_score=True
)

#REGRESION
# Definimos los hiperparámetros

param_grid_reg = {
    'regressor__n_estimators': [200, 300, 500],
    'regressor__max_depth': [5, 7, 10],
    'regressor__min_samples_split': [5, 10, 20],
    'regressor__min_samples_leaf': [2, 5, 10]
}

grid_search_reg = GridSearchCV(
    estimator=pipeline_rf_reg,
    param_grid=param_grid_reg,
    cv=5,
    scoring='r2',
    n_jobs=-1,
    verbose=2,
    return_train_score=True
)
