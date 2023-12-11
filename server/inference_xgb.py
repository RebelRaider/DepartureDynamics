import xgboost as xgb
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import roc_auc_score
import optuna
import os

def train_xgboost(file_name, model_name):
    data = pd.read_csv(f'{file_name}.csv')
    data = data.drop(['Name', 'Email'], axis=1)

    X = data.drop(['Probability of Leaving'], axis=1)
    y = data['Probability of Leaving']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)

    parameters = {
        'verbosity': 1,
        'seed': 42,
        'eval_metric': ['logloss', 'auc'],
        'use_label_encoder': False,
        'n_estimators': 10000,
        'tree_method': 'hist',
        'device': 'cuda'

    }

    model = xgb.train(parameters, dtrain,
                      num_boost_round=parameters['n_estimators'],
                      evals=[(dtrain, 'train'), (dval, 'eval')],
                      early_stopping_rounds=5000)

    model.save_model(f'{model_name}.json')

def inference_xgboost(file_name, model_name='xgboost_model', output_file_name='predicted_results'):
    df = pd.read_csv(f'{file_name}.csv')

    email_name_data = df[['Email', 'Name']]
    df = df.drop(['Name', 'Email'], axis=1)
    
    model = xgb.Booster()
    model.load_model(f'{model_name}.json')

    dtest = xgb.DMatrix(df)
    predictions = model.predict(dtest)

    email_name_data['predicted'] = predictions

    email_name_data.to_csv(f'{output_file_name}.csv', index=False)

    return f'{output_file_name}.csv'

def objective(trial, X, y, X_val, y_val):
    dtrain = xgb.DMatrix(X, label=y)
    dval = xgb.DMatrix(X_val, label=y_val)

    parameters = {
        'verbosity': 1,
        'seed': 42,
        'eval_metric': ['logloss', 'auc'],
        'max_depth': trial.suggest_int('max_depth', 4, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-9, 10, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-9, 10, log=True),
        'subsample': trial.suggest_float('subsample', 0.1, 1),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.1, 1),
        'tree_method': 'hist',
        'device': 'cuda' 
    }

    model = xgb.train(parameters, dtrain,
                      num_boost_round=parameters['n_estimators'],
                      evals=[(dtrain, 'train'), (dval, 'eval')],
                      early_stopping_rounds=50)

    predictions = model.predict(dval)
    roc_auc = roc_auc_score(y_val, predictions)

    return roc_auc

def optimize_xgboost(file_name, model_name):
    data = pd.read_csv(f'{file_name}.csv')
    data = data.drop(['Name', 'Email'], axis=1)

    X = data.drop(['Probability of Leaving'], axis=1)
    y = data['Probability of Leaving']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train, X_val, y_val), n_trials=75)

    best_params = study.best_params

    print(f"Best Hyperparameters: {best_params}")

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)

    # Train the final model with the best hyperparameters
    final_model = xgb.train(best_params, dtrain,
                            num_boost_round=best_params['n_estimators'],
                            evals=[(dtrain, 'train'), (dval, 'eval')],
                            early_stopping_rounds=50)

    # Save the final model
    final_model.save_model(f'{model_name}.json')

# Пример использования:
train_xgboost('dynamic_synthetic_dataset_funny', 'xgb_2')
inference_xgboost('dynamic_synthetic_dataset_test', 'xgb_2', 'predict_xgb_3')
# optimize_xgboost('synthetic_dataset', 'optim_xgb_first')
# inference_xgboost('synthetic_dataset_test', 'optim_xgb_first', 'optim_predict_xgb_2')