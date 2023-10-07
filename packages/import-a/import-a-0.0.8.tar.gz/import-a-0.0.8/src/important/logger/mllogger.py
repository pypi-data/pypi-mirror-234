import mlflow
from typing import (
    Optional, Union, Dict, Any, List
)
import logging


class MLLogger:
    """
    Make mlflow logging easier
    by setting up the entire handler from experiment id and run_id
    """

    def __init__(
            self, experiment_name: str,
            run_id: Optional[str] = None,
            run_name: Optional[str] = None):
        """
        experiment: name of the experiment
        run_id: if None, create a new run
        """
        self.experiment_name = experiment_name
        self.experiment = mlflow.set_experiment(experiment_name)
        self.experiment_id = self.experiment.experiment_id
        self.run_id = run_id
        if run_id is None:
            # see if we have active run
            if mlflow.active_run() is not None:
                self.run_id = mlflow.active_run().info.run_id
            # set new run
            else:
                run_kwargs = {}
                if run_name is not None:
                    run_kwargs["run_name"] = run_name
                run = mlflow.start_run(
                    experiment_id=self.experiment_id,
                    **run_kwargs
                )
                self.run_id = run.info.run_id
                mlflow.end_run()
        else:
            self.run_id = run_id

    def __add__(self, data: Dict[str, Any]) -> "MLLogger":
        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_id=self.run_id
        ) as run:
            for k, v in data.items():
                if k in run.data.params:
                    logging.warning(
                        f"Found {k} in params, won't overwrite")
                    continue
                mlflow.log_param(k, v)
        return self

    def __repr__(self) -> str:
        return f"{self.experiment_name}/run:{self.run_id}"

    def __setitem__(self, key: str, value: Any) -> None:
        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_id=self.run_id
        ) as run:
            if key in run.data.params:
                logging.warning(
                    f"Found {key} in params, won't overwrite")
                return
            mlflow.log_param(key, value)

    def __getitem__(self, key: str) -> Any:
        """
        extract metric or param from run
        """
        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_id=self.run_id
        ) as run:
            if key in run.data.params:
                return run.data.params[key]
            elif key in run.data.metrics:
                return run.data.metrics[key]
            else:
                raise KeyError(f"{key} not found in params")

    def __mul__(self, data: Dict[str, Union[float, int]]) -> "MLLogger":
        """
        Log metrics
        """
        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_id=self.run_id
        ) as run:
            for k, v in data.items():
                if k in run.data.metrics:
                    logging.warning(
                        f"Found {k} in metrics, won't overwrite")
                    continue
                mlflow.log_metric(k, v)
        return self

    @property
    def params_data(self) -> Dict[str, Any]:
        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_id=self.run_id
        ) as run:
            return run.data.params

    @property
    def metrics_data(self) -> Dict[str, Any]:
        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_id=self.run_id
        ) as run:
            return run.data.metrics

    def query(
        self,
        max_results: int = 10,
        filter_string: Optional[str] = None,
        order_by: List[str] = [],
    ):
        kwargs = dict(order_by=order_by)
        if filter_string is not None:
            kwargs["filter_string"] = filter_string
        return mlflow.search_runs(
            experiment_ids=[self.experiment.experiment_id, ],
            max_results=max_results,
            **kwargs,
        )
