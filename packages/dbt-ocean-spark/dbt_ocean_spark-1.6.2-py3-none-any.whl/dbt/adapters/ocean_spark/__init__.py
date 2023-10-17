from dbt.adapters.ocean_spark.connections import SparkConnectionManager  # noqa
from dbt.adapters.ocean_spark.connections import SparkCredentials
from dbt.adapters.ocean_spark.relation import SparkRelation  # noqa
from dbt.adapters.ocean_spark.column import SparkColumn  # noqa
from dbt.adapters.ocean_spark.impl import SparkAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import ocean_spark

Plugin = AdapterPlugin(
    adapter=SparkAdapter, credentials=SparkCredentials, include_path=ocean_spark.PACKAGE_PATH  # type: ignore
)
