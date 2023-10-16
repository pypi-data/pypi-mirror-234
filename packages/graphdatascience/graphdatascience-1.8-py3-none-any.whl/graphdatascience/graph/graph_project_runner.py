from typing import Any

from pandas import Series

from ..error.illegal_attr_checker import IllegalAttrChecker
from .graph_object import Graph
from .graph_type_check import from_graph_type_check
from graphdatascience.graph.graph_create_result import GraphCreateResult


class GraphProjectRunner(IllegalAttrChecker):
    def __call__(self, graph_name: str, node_spec: Any, relationship_spec: Any, **config: Any) -> GraphCreateResult:
        result = self._query_runner.run_query_with_logging(
            f"CALL {self._namespace}($graph_name, $node_spec, $relationship_spec, $config)",
            {
                "graph_name": graph_name,
                "node_spec": node_spec,
                "relationship_spec": relationship_spec,
                "config": config,
            },
        ).squeeze()

        return GraphCreateResult(Graph(graph_name, self._query_runner, self._server_version), result)

    def estimate(self, node_projection: Any, relationship_projection: Any, **config: Any) -> "Series[Any]":
        self._namespace += ".estimate"
        result = self._query_runner.run_query(
            f"CALL {self._namespace}($node_spec, $relationship_spec, $config)",
            {
                "node_spec": node_projection,
                "relationship_spec": relationship_projection,
                "config": config,
            },
        )

        return result.squeeze()  # type: ignore

    @property
    def cypher(self) -> "GraphProjectRunner":
        return GraphProjectRunner(self._query_runner, self._namespace + ".cypher", self._server_version)


class GraphProjectBetaRunner(IllegalAttrChecker):
    @from_graph_type_check
    def subgraph(
        self,
        graph_name: str,
        from_G: Graph,
        node_filter: str,
        relationship_filter: str,
        **config: Any,
    ) -> GraphCreateResult:
        self._namespace += ".subgraph"
        result = self._query_runner.run_query_with_logging(
            f"CALL {self._namespace}($graph_name, $from_graph_name, $node_filter, $relationship_filter, $config)",
            {
                "graph_name": graph_name,
                "from_graph_name": from_G.name(),
                "node_filter": node_filter,
                "relationship_filter": relationship_filter,
                "config": config,
            },
        ).squeeze()

        return GraphCreateResult(Graph(graph_name, self._query_runner, self._server_version), result)
