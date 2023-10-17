"""**Graphs** provide a natural language interface to graph databases."""

from promptmanager.script.base.graphs.arangodb_graph import ArangoGraph
from promptmanager.script.base.graphs.falkordb_graph import FalkorDBGraph
from promptmanager.script.base.graphs.hugegraph import HugeGraph
from promptmanager.script.base.graphs.kuzu_graph import KuzuGraph
from promptmanager.script.base.graphs.memgraph_graph import MemgraphGraph
from promptmanager.script.base.graphs.nebula_graph import NebulaGraph
from promptmanager.script.base.graphs.neo4j_graph import Neo4jGraph
from promptmanager.script.base.graphs.neptune_graph import NeptuneGraph
from promptmanager.script.base.graphs.networkx_graph import NetworkxEntityGraph
from promptmanager.script.base.graphs.rdf_graph import RdfGraph

__all__ = [
    "MemgraphGraph",
    "NetworkxEntityGraph",
    "Neo4jGraph",
    "NebulaGraph",
    "NeptuneGraph",
    "KuzuGraph",
    "HugeGraph",
    "RdfGraph",
    "ArangoGraph",
    "FalkorDBGraph",
]
