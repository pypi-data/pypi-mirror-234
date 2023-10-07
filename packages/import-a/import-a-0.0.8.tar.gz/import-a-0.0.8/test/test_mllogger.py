import mlflow
from important.logger.mllogger import MLLogger
import logging
from time import sleep


mlflow.set_tracking_uri("http://localhost:9876")


mllogger = MLLogger("test_experiment", run_name="test_run")


def test_logging_params():
    global mllogger
    logging.info("input params")
    mllogger = mllogger + dict(
        a=1,
        b=2,
        c="model-name",
    )

    logging.info("input params with duplicate keys")
    mllogger = mllogger + dict(
        a=4,
        d=3,
    )

    assert mllogger["a"] == "1"
    assert mllogger["b"] == "2"
    assert mllogger["c"] == "model-name"
    assert mllogger["d"] == "3"


def test_logging_metrics():
    global mllogger
    logging.info("input metrics")
    mllogger = mllogger * dict(
        train_loss=0.1,
        val_loss=0.2,
        test_loss=0.3,
    )

    logging.info("input metrics with duplicate keys")
    mllogger = mllogger * dict(
        train_loss=0.4,
        val_loss=0.5,
    )

    assert mllogger["train_loss"] == 0.1
    assert mllogger["val_loss"] == 0.2
    assert mllogger["test_loss"] == 0.3


mllogger2 = MLLogger("test_experiment", run_id=mllogger.run_id)


def test_query():
    df = mllogger2.query()
    assert df["metrics.train_loss"].values[0] == 0.1
