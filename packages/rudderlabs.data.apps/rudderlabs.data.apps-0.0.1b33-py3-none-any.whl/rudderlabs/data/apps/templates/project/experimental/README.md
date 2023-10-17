# Pycaret AutoML

This is the experimantal analysis for the AutoMl using the pycaret and MLflow.

## Pycaret integrating MLflow
### Parameters required to incorporate MLflow

"**log_experiment**" , "**log_plots**" is used to log the experiment files to the MLflow server.

"**experiment_name**" is used to give the name to the experiment for logging in mlflow server.

When these parameters are set "True" Pycaret internally integrates with MLflow and logged all metrics and parameters on MLflow server.

## MLflow dashboard

```
To start the mlflow dashboard server
$ mlflow ui
```
It will provide you a localhost server, this will allow you to view tracking UI where you can see the experiment folders.

**Model page**
![MLflow UI](/Experimental/img/mlflowUI001.png)

**Experiment view**
![MLflow Model UI](/Experimental/img/mlflowUI002.png)
