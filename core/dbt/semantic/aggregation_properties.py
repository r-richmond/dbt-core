from dbt.dataclass_schema import StrEnum


class AggregationType(StrEnum):
    """Aggregation methods for measures"""

    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    COUNT_DISTINCT = "count_distinct"
    SUM_BOOLEAN = "sum_boolean"
    AVERAGE = "average"
    PERCENTILE = "percentile"
    MEDIAN = "median"

    @property
    def is_additive(self) -> bool:
        """Indicates that if you sum values over a dimension grouping, you will still get an accurate result for this metric."""
        if (
            self is AggregationType.SUM
            or self is AggregationType.SUM_BOOLEAN
            or self is AggregationType.COUNT
        ):
            return True
        elif (
            self is AggregationType.MIN
            or self is AggregationType.MAX
            or self is AggregationType.COUNT_DISTINCT
            or self is AggregationType.BOOLEAN
            or self is AggregationType.AVERAGE
            or self is AggregationType.PERCENTILE
            or self is AggregationType.MEDIAN
        ):
            return False
        # else:
        # assert_values_exhausted(self)

    @property
    def is_expansive(self) -> bool:
        """Expansive ≝ Op( X ∪ Y ∪ ...) = Op( Op(X) ∪ Op(Y) ∪ ...)
        NOTE: COUNT is only expansive because it's transformed into a SUM agg during model transformation
        """
        return self in (
            AggregationType.SUM,
            AggregationType.MIN,
            AggregationType.MAX,
            AggregationType.BOOLEAN,
            AggregationType.COUNT,
        )

    @property
    def fill_nulls_with_0(self) -> bool:
        """Indicates if charts should show 0 instead of null where there are gaps in data."""
        return self in (
            AggregationType.SUM,
            AggregationType.COUNT_DISTINCT,
            AggregationType.SUM_BOOLEAN,
            AggregationType.COUNT,
        )

    @property
    def can_limit_dimension_values(self) -> bool:
        """Indicates if we can limit dimension values in charts.
        Currently, this means:
        1. The dimensions we care about most are the ones with the highest numeric values
        2. We can calculate the "other" column in the postprocessor (meaning the metric is expansive)
        """
        return self in (AggregationType.SUM, AggregationType.SUM_BOOLEAN, AggregationType.COUNT)


class AggregationState(StrEnum):
    """Represents how the measure is aggregated."""

    NON_AGGREGATED = "NON_AGGREGATED"
    PARTIAL = "PARTIAL"
    COMPLETE = "COMPLETE"

    def __repr__(self) -> str:  # noqa: D
        return f"{self.__class__.__name__}.{self.name}"