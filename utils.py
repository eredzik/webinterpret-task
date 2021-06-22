import sqlite3

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def get_data_from_db():
    con = sqlite3.connect("data/shipping.db")
    df = pd.read_sql_query(
        """
with temp1 as
(select
    target_country,
    source_country,
    category_id,
    shipping_type,
    year,
    sum(item_count) as item_count
from counts
group by
    target_country,
    source_country,
    category_id,
    shipping_type,
    year)
SELECT
t1.*,
t2.category_id,
t3.item_count,
t3.year
from transactions t1
left join categories t2
on t1.item_id = t2.item_id
left join temp1 t3
on t1.target_country = t3.target_country and
    t1.source_country = t3.source_country and
    t2.category_id = t3.category_id and
    t1.shipping_type = t3.shipping_type and
strftime('%Y', t1.timestamp) = t3.year
        """,
        con,
    )
    con.close()
    df["target"] = np.log(df["active_gmv"] / df["item_count"])
    return df


def get_subset(df: pd.DataFrame, test_size=0.9):
    # We remove "active_gmv" less than 5 to ensure logarithm wont explode to minus infinity
    train, test = train_test_split(
        df, test_size=test_size, stratify=df[["category_id", "shipping_type"]]
    )
    return train, test


def to_enumerated(df: pd.DataFrame):
    dict_of_values = {x: i for i, x in enumerate(list(df.unique()))}
    return [dict_of_values[z] for z in df.values]
