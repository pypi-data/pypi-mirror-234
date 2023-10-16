from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Tuple, TypeVar

from pandas import DataFrame, Series

from ..graph.graph_object import Graph
from ..graph.graph_type_check import graph_type_check
from ..model.pipeline_model import PipelineModel
from ..query_runner.query_runner import QueryRunner
from ..server_version.server_version import ServerVersion

MODEL_TYPE = TypeVar("MODEL_TYPE", bound=PipelineModel, covariant=True)


class TrainingPipeline(ABC, Generic[MODEL_TYPE]):
    def __init__(self, name: str, query_runner: QueryRunner, server_version: ServerVersion):
        self._name = name
        self._query_runner = query_runner
        self._server_version = server_version

    def name(self) -> str:
        """
        Get the name of the pipeline.

        Returns:
            The name of the pipeline.

        """
        return self._name

    @abstractmethod
    def _query_prefix(self) -> str:
        pass

    @abstractmethod
    def _create_trained_model(self, name: str, query_runner: QueryRunner) -> MODEL_TYPE:
        pass

    def addNodeProperty(self, procedure_name: str, **config: Any) -> "Series[Any]":
        """
        Add a node property step to the pipeline.

        Args:
            procedure_name: The name of the procedure to use.
            **config: The configuration for the node property.

        Returns:
            The result of the query.

        """
        query = f"{self._query_prefix()}addNodeProperty($pipeline_name, $procedure_name, $config)"
        params = {
            "pipeline_name": self.name(),
            "procedure_name": procedure_name,
            "config": config,
        }
        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    @staticmethod
    def _expand_ranges(config: Dict[str, Any]) -> Dict[str, Any]:
        def _maybe_expand_tuple(value: Any) -> Any:
            return {"range": list(value)} if isinstance(value, tuple) else value

        return {key: _maybe_expand_tuple(val) for (key, val) in config.items()}

    def configureAutoTuning(self, **config: Any) -> "Series[Any]":
        """
        Configure auto-tuning for the pipeline.

        Args:
            **config: The configuration for auto-tuning.

        Returns:
            The result of the query.

        """
        query_prefix = self._query_prefix().replace("beta", "alpha")
        query = f"{query_prefix}configureAutoTuning($pipeline_name, $config)"
        params = {"pipeline_name": self.name(), "config": config}

        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    @graph_type_check
    def train(self, G: Graph, **config: Any) -> Tuple[MODEL_TYPE, "Series[Any]"]:
        """
        Train a model on a given graph using the pipeline.

        Args:
            G: The graph to train on.
            **config: The configuration for training.

        Returns:
            A tuple containing the trained model and the result of the query.

        """
        query = f"{self._query_prefix()}train($graph_name, $config)"
        config["pipeline"] = self.name()
        params = {
            "graph_name": G.name(),
            "config": config,
        }

        result = self._query_runner.run_query_with_logging(query, params).squeeze()

        return (
            self._create_trained_model(config["modelName"], self._query_runner),
            result,
        )

    @graph_type_check
    def train_estimate(self, G: Graph, **config: Any) -> "Series[Any]":
        """
        Estimate the training time for a given graph and configuration.

        Args:
            G: The graph to train on.
            **config: The configuration for training.

        Returns:
            The result of the query.

        """
        query = f"{self._query_prefix()}train.estimate($graph_name, $config)"
        config["pipeline"] = self.name()
        params = {
            "graph_name": G.name(),
            "config": config,
        }

        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    def configureSplit(self, **config: Any) -> "Series[Any]":
        """
        Configure the splits for training the pipeline.

        Args:
            **config: The configuration for the splits.

        Returns:
            The result of the query.

        """
        query = f"{self._query_prefix()}configureSplit($pipeline_name, $config)"
        params = {"pipeline_name": self.name(), "config": config}

        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    def node_property_steps(self) -> DataFrame:
        """
        Get the node property steps of the pipeline.

        Returns:
            A DataFrame containing the node property steps.

        """
        pipeline_info = self._list_info()["pipelineInfo"][0]
        return DataFrame(pipeline_info["featurePipeline"]["nodePropertySteps"])

    def split_config(self) -> "Series[float]":
        """
        Get the split configuration of the pipeline.

        Returns:
            A Series containing the split configuration.

        """
        pipeline_info = self._list_info()["pipelineInfo"][0]
        split_config: "Series[float]" = Series(pipeline_info["splitConfig"])
        return split_config

    def parameter_space(self) -> "Series[Any]":
        """
        Get the parameter space of the pipeline.

        Returns:
            A Series containing the parameter space.

        """
        pipeline_info = self._list_info()["pipelineInfo"][0]
        parameter_space: "Series[Any]" = Series(pipeline_info["trainingParameterSpace"])
        return parameter_space

    def auto_tuning_config(self) -> "Series[Any]":
        """
        Get the auto-tuning configuration of the pipeline.

        Returns:
            A Series containing the auto-tuning configuration.

        """
        pipeline_info = self._list_info()["pipelineInfo"][0]
        auto_tuning_config: "Series[Any]" = Series(pipeline_info["autoTuningConfig"])
        return auto_tuning_config

    def _list_info(self) -> DataFrame:
        query = f"CALL gds{self._tier_namespace()}.pipeline.list($name)"
        params = {"name": self.name()}

        info = self._query_runner.run_query(query, params, custom_error=False)

        if len(info) == 0:
            raise ValueError(f"There is no '{self.name()}' in the pipeline catalog")

        return info

    def type(self) -> str:
        """
        Get the type of the pipeline.

        Returns:
            The type of the pipeline.
            It will be one of NodeClassificationPipeline, LinkPredictionPipeline, or NodeRegressionPipeline.

        """
        return self._list_info()["pipelineType"].squeeze()  # type: ignore

    def creation_time(self) -> Any:  # neo4j.time.DateTime not exported
        """
        Get the creation time of the pipeline.

        Returns:
            The creation time of the pipeline.

        """
        return self._list_info()["creationTime"].squeeze()

    def exists(self) -> bool:
        """
        Check if the pipeline exists.

        Returns:
            True if the pipeline exists, False otherwise.

        """
        query = f"CALL gds{self._tier_namespace()}.pipeline.exists($pipeline_name) YIELD exists"
        params = {"pipeline_name": self._name}

        return self._query_runner.run_query(query, params, custom_error=False)["exists"].squeeze()  # type: ignore

    def drop(self, failIfMissing: bool = False) -> "Series[Any]":
        """
        Drop the pipeline.

        Args:
            failIfMissing: If True, an error will be thrown if the pipeline does not exist.

        Returns:
            The result of the query.

        """
        query = f"CALL gds{self._tier_namespace()}.pipeline.drop($pipeline_name, $fail_if_missing)"
        params = {"pipeline_name": self._name, "fail_if_missing": failIfMissing}

        return self._query_runner.run_query(query, params, custom_error=False).squeeze()  # type: ignore

    def _tier_namespace(self) -> str:
        return "" if self._server_version >= ServerVersion(2, 5, 0) else ".beta"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name()}, type={self.type()})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._list_info().to_dict()})"
