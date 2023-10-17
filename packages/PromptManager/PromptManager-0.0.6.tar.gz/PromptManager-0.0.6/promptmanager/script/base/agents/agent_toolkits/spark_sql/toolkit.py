"""Toolkit for interacting with Spark SQL."""
from typing import List

from promptmanager.script.base.agents.agent_toolkits.base import BaseToolkit
from promptmanager.script.base.pydantic_v1 import Field
from promptmanager.script.base.schema.language_model import BaseLanguageModel
from promptmanager.script.base.tools import BaseTool
from promptmanager.script.base.tools.spark_sql.tool import (
    InfoSparkSQLTool,
    ListSparkSQLTool,
    QueryCheckerTool,
    QuerySparkSQLTool,
)
from promptmanager.script.base.utilities.spark_sql import SparkSQL


class SparkSQLToolkit(BaseToolkit):
    """Toolkit for interacting with Spark SQL."""

    db: SparkSQL = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            QuerySparkSQLTool(db=self.db),
            InfoSparkSQLTool(db=self.db),
            ListSparkSQLTool(db=self.db),
            QueryCheckerTool(db=self.db, llm=self.llm),
        ]
