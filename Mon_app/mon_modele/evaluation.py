import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve, KFold
from sklearn.metrics import mean_absolute_error, median_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from lazypredict.Supervised import LazyRegressor
import plotly.graph_objects as go

def regression_report(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    print(f'MAE: {mean_absolute_error(y_true, y_pred):.2f}')
    print(f'MedAE: {median_absolute_error(y_true, y_pred):.2f}')
    print(f'RMSE: {rmse:.2f}')
    print(f'R²: {r2_score(y_true, y_pred):.2f}')

def evaluate_model(model, X_train, X_test, y_train, y_test):
    kfold = KFold(n_splits=5, shuffle=True, random_state=77)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    regression_report(y_test, y_pred)

    N, train_score, val_score = learning_curve(
        model, X_train, y_train,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=kfold, scoring='r2'
    )

    #plt.plot(N, train_score.mean(axis=1), label="Train")
    #plt.plot(N, val_score.mean(axis=1), label="Validation")
    #plt.title(type(model).__name__)
    #plt.xlabel("Taille du train set")
    #plt.ylabel("Score R²")
    #plt.legend()
    #plt.show()

def lazy_prediction(X,y,fold):
    all_models = []
    
    for train_index, test_index in fold.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
        clf = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
        tableau_models, predictions = clf.fit(X_train, X_test, y_train, y_test)
        
        all_models.append(tableau_models)
    resultat_tableau_modeles = pd.concat(all_models).groupby(level=0).mean().sort_values(by="R-Squared", ascending=False)
    return resultat_tableau_modeles


def evaluation_metriques(dict_models, preprocessor,X_train,y_train,X_test,y_test,fold):
    for nom, model_du_dict in dict_models.items():
        model = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", model_du_dict)
        ])

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        N, train_score, val_score = learning_curve(
            model, X_train, y_train,
            train_sizes=np.linspace(0.1, 1, 10),
            cv=fold,
            scoring='r2'
        )


        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=N,
            y=train_score.mean(axis=1),
            mode='lines+markers',
            name='Train',
            line=dict(color='blue')
        ))

        fig.add_trace(go.Scatter(
            x=N,
            y=val_score.mean(axis=1),
            mode='lines+markers',
            name='Validation',
            line=dict(color='orange')
        ))

        fig.update_layout(
            title=nom,
            xaxis_title='Taille du train set',
            yaxis_title='Score R²',
            yaxis=dict(range=[0, 1.01]),
            legend=dict(x=0.01, y=0.99),
            template='plotly_white',
            width=600,    
            height=400 
        )

        fig.show()

        regression_report(y_test, y_pred)
        print()