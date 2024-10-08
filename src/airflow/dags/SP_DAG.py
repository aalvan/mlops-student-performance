from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable

from datetime import datetime, timedelta

Variable.set('random_state', 42)

default_args = {
    'owner': 'Alexis Alva',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry': False,
}

@task.virtualenv(
        task_id='prepare_data',
    requirements = ["scikit-learn==1.5.2"],
    venv_cache_path="/tmp/venv_cache"
)
def _prepare_data():
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import OrdinalEncoder

    save_path = '/opt/airflow/data/processed/StudentPerformanceFactors.csv'
    data_path = '/opt/airflow/data/raw/StudentPerformanceFactors.csv'

    df = pd.read_csv(data_path)
    df = df.dropna()

    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns


    ord_encoder = OrdinalEncoder()
    df.loc[:, cat_cols] = ord_encoder.fit_transform(df[cat_cols])
    df.to_csv(save_path, index=False)

@task.virtualenv(
    task_id = 'build',
    requirements = ["scikit-learn==1.5.2"],
    venv_cache_path="/tmp/venv_cache"
)
def _build():
    import pandas as pd
    from sklearn.model_selection import train_test_split
    
    data_path = '/opt/airflow/data/processed/StudentPerformanceFactors.csv'
    df = pd.read_csv(data_path)

    X = df.drop(columns=['Exam_Score'])
    y = df.loc[:, 'Exam_Score']

    return {
        'X': X.to_dict(orient='records'),
        'y': y.tolist(),
    }

@task.virtualenv(
    task_id = 'hyperparameter_tuning',
    requirements = ["mlflow==2.16.2", "scikit-learn==1.5.2", "hyperopt==0.2.7"],
    venv_cache_path="/tmp/venv_cache"
)
def _hyperparameter_tuning(train_data):
    import mlflow

    import pandas as pd

    from sklearn.metrics import make_scorer
    from sklearn.model_selection import cross_validate
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    from joblib import dump

    from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
    from hyperopt.pyll.base import scope


    X = pd.DataFrame(train_data['X'])
    y = pd.Series(train_data['y'])

    
    TRACKING_SERVER_HOST = "mlflow_server"
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    mlflow.set_experiment("student_performance")

    mlflow.set_experiment_tags(
        {
        "project" : "Student Performance",
        "task": "Regression"
        }
    )
    
    data_path = '/opt/airflow/data/processed/StudentPerformanceFactors.csv'
    #random_state = Variable.get("random_state", default_var=42)
    random_state = 42
    def objective(params):
        with mlflow.start_run() as run:
            mlflow.log_param("train_data_path", data_path)
            
            rf_regressor = RandomForestRegressor(**params)

            mse_scorer = make_scorer(mean_squared_error, greater_is_better=False) # Set greater_is_better=False to minimize
            mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)    

            scoring = {
                'mse': mse_scorer,
                'mae': mae_scorer
            }
            scores = cross_validate(rf_regressor, X, y, scoring=scoring, cv=5)
            
            mse = -scores['test_mse'].mean()  # Negate MSE for consistency
            mae = -scores['test_mae'].mean()

            data_params = {
                'random_state': random_state,
            }

            mlflow.log_params(data_params)

            ml_params = {
                f"rfr_{param}": value for param, value in rf_regressor.get_params().items()
            }
            mlflow.log_params(ml_params)
            
            ml_metrics = {'mse':mse, 'mae': mae}
            mlflow.log_metrics(ml_metrics)
            print(f'mse:{mse}, mae:{mae}')

            mlflow.set_tag('model', 'random-forest-regressor')

            print(f"Experiment ID: {run.info.experiment_id}")
            print(f"Run ID: {run.info.run_id}")

            mlflow.end_run()

            return {'loss': mse, 'status': STATUS_OK, 'params': params}
    
    search_space = {
    'max_depth': scope.int(hp.choice('max_depth', [10, 20, 30])),
    'max_features': hp.choice('max_features', ['sqrt','log2']),
    'n_estimators': scope.int(hp.quniform('n_estimators', 50, 300, 50)),
    }

    trials = Trials()
    best = fmin(fn=objective,
                space=search_space,
                algo=tpe.suggest,
                max_evals=5,
                trials=trials
                )

    best_params = trials.best_trial['result']['params']

    return {'best_params': best_params}

@task.virtualenv(
    task_id = 'train',
    requirements = ["mlflow==2.16.2", "scikit-learn==1.5.2", "hyperopt==0.2.7"],
    venv_cache_path="/tmp/venv_cache"
)
def  _train(parameters): # The "params" name in args is a part of kwargs and therefore reserved.
    import pandas as pd
    import mlflow
    from mlflow.models.signature import infer_signature

    from sklearn.metrics import make_scorer
    from sklearn.model_selection import cross_validate
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error


    artifact_path = 'models/random_regresor.joblib'
    data_path = '/opt/airflow/data/processed/StudentPerformanceFactors.csv'
    random_state = 42

    best_params = parameters['best_params']

    TRACKING_SERVER_HOST = "mlflow_server"
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    mlflow.set_experiment("student_performance")

    with mlflow.start_run() as run:
        mlflow.log_param("train_data_path", data_path)

        df = pd.read_csv(data_path)

        X = df.drop(columns=['Exam_Score']).astype('float64')
        y = df.loc[:, 'Exam_Score'].astype('float64')

        rf_regressor = RandomForestRegressor(**best_params)

        mse_scorer = make_scorer(mean_squared_error, greater_is_better=False) # Set greater_is_better=False to minimize
        mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)    

        scoring = {
            'mse': mse_scorer,
            'mae': mae_scorer
        }
        scores = cross_validate(rf_regressor, X, y, scoring=scoring, cv=5)

        mse = -scores['test_mse'].mean()  # Negate MSE for consistency
        mae = -scores['test_mae'].mean()

        data_params = {
            'random_state': random_state,
        }

        mlflow.log_params(data_params)

        ml_params = {
            f"rfr_{param}": value for param, value in rf_regressor.get_params().items()
        }
        mlflow.log_params(ml_params)

        ml_metrics = {'mse':mse, 'mae': mae}
        mlflow.log_metrics(ml_metrics)
        print(f'mse:{mse}, mae:{mae}')

        mlflow.set_tag('model', 'random-forest-regressor')

        rf_regressor.fit(X,y)

        input_example = X.sample(1)
        signature = infer_signature(X, y)

        mlflow.sklearn.log_model(rf_regressor, artifact_path=artifact_path, signature=signature, input_example=input_example)
        artifact_uri = mlflow.get_artifact_uri()
        print(f'artifact_uri: {artifact_uri}')

        print(f"Experiment ID: {run.info.experiment_id}")
        print(f"Run ID: {run.info.run_id}")


with DAG(
    'student_performance',
    start_date = None,
    default_args = default_args,
    schedule_interval = None,
    description = "A ML pipeline for student performance",
    tags = ['mlops']
) as dag:
    
    build = _build()
    hyperparameter_tuning = _hyperparameter_tuning(build)
    train = _train(hyperparameter_tuning)

    end = DummyOperator(task_id='end')

    _prepare_data() >> build >> hyperparameter_tuning >> train