from typing import Optional

from pyspark.sql import DataFrame
from pyspark.sql import functions as sf

from replay.models.base_rec import NonPersonalizedRecommender


class PopRec(NonPersonalizedRecommender):
    """
    Recommend objects using their popularity.

    Popularity of an item is a probability that random user rated this item.

    .. math::
        Popularity(i) = \\dfrac{N_i}{N}

    :math:`N_i` - number of users who rated item :math:`i`

    :math:`N` - total number of users

    >>> import pandas as pd
    >>> data_frame = pd.DataFrame({"user_idx": [1, 1, 2, 2, 3, 4], "item_idx": [1, 2, 2, 3, 3, 3], "relevance": [0.5, 1, 0.1, 0.8, 0.7, 1]})
    >>> data_frame
       user_idx  item_idx  relevance
    0         1         1        0.5
    1         1         2        1.0
    2         2         2        0.1
    3         2         3        0.8
    4         3         3        0.7
    5         4         3        1.0

    >>> from replay.utils.spark_utils import convert2spark
    >>> data_frame = convert2spark(data_frame)

    >>> res = PopRec().fit_predict(data_frame, 1)
    >>> res.toPandas().sort_values("user_idx", ignore_index=True)
       user_idx  item_idx  relevance
    0         1         3       0.75
    1         2         1       0.25
    2         3         2       0.50
    3         4         2       0.50

    >>> res = PopRec().fit_predict(data_frame, 1, filter_seen_items=False)
    >>> res.toPandas().sort_values("user_idx", ignore_index=True)
       user_idx  item_idx  relevance
    0         1         3       0.75
    1         2         3       0.75
    2         3         3       0.75
    3         4         3       0.75

    >>> res = PopRec(use_relevance=True).fit_predict(data_frame, 1)
    >>> res.toPandas().sort_values("user_idx", ignore_index=True)
       user_idx  item_idx  relevance
    0         1         3      0.625
    1         2         1      0.125
    2         3         2      0.275
    3         4         2      0.275

    """

    sample: bool = False

    def __init__(
        self,
        use_relevance: bool = False,
        add_cold_items: bool = True,
        cold_weight: float = 0.5,
    ):
        """
        :param use_relevance: flag to use relevance values as is or to treat them as 1
        :param add_cold_items: flag to consider cold items in recommendations building
            if present in `items` parameter of `predict` method
            or `pairs` parameter of `predict_pairs` methods.
            If true, cold items are assigned relevance equals to the less relevant item relevance
            multiplied by cold_weight and may appear among top-K recommendations.
            Otherwise cold items are filtered out.
            Could be changed after model training by setting the `add_cold_items` attribute.
        : param cold_weight: if `add_cold_items` is True,
            cold items are added with reduced relevance.
            The relevance for cold items is equal to the relevance
            of a least relevant item multiplied by a `cold_weight` value.
            `Cold_weight` value should be in interval (0, 1].
        """
        self.use_relevance = use_relevance
        super().__init__(
            add_cold_items=add_cold_items, cold_weight=cold_weight
        )

    @property
    def _init_args(self):
        return {
            "use_relevance": self.use_relevance,
            "add_cold_items": self.add_cold_items,
            "cold_weight": self.cold_weight,
        }

    def _fit(
        self,
        log: DataFrame,
        user_features: Optional[DataFrame] = None,
        item_features: Optional[DataFrame] = None,
    ) -> None:

        agg_func = sf.countDistinct("user_idx").alias("relevance")
        if self.use_relevance:
            agg_func = sf.sum("relevance").alias("relevance")

        self.item_popularity = (
            log.groupBy("item_idx")
            .agg(agg_func)
            .withColumn(
                "relevance", sf.col("relevance") / sf.lit(self.users_count)
            )
        )

        self.item_popularity.cache().count()
        self.fill = self._calc_fill(self.item_popularity, self.cold_weight)
