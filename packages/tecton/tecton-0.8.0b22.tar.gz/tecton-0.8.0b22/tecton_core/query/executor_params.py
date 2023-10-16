from enum import Enum


class QueryTreeStep(Enum):
    """
    Query trees are executed in steps. Each step can be executed on its own compute, and can stage its results in preparation for the next step.
    """

    # Rewrites the initial un-modified query tree before executing data source scans / feature view transformations
    INIT = 1
    # Runs feature view transformations to produce un-aggregated feature data.
    PIPELINE = 2
    # Runs partial aggregations, full aggregations, and the as-of join.
    AGGREGATION = 3
    # Runs on-demand transformations.
    ODFV = 4


# Where to stage results to when using the query tree executor.
# By default, this will stage to memory (i.e. Snowflake -> memory -> DuckDB)
class QueryTreeStagingLocation(Enum):
    DWH = 1
    S3 = 2
    MEMORY = 3
    FILE = 4


URI_SCHEME_TO_STAGING_LOCATION = {
    # If user specifies a uri like /tmp/dir
    "": QueryTreeStagingLocation.FILE,
    # If user specifies a uri like file:///tmp/dir
    "file": QueryTreeStagingLocation.FILE,
    # If user specifies a uri like s3://
    "s3": QueryTreeStagingLocation.S3,
}
