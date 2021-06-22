import logging
import sys

import statsmodels.api as sm
import statsmodels.formula.api as smf
from patsy.contrasts import Sum, Treatment
from sklearn.metrics import r2_score

from utils import get_data_from_db, get_subset

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

df = get_data_from_db()
train, test = get_subset(df, test_size=0.6)
model = smf.ols(
    formula="""
            target ~
                shipping_type +
                year +
                C(category_id, Sum) * C(shipping_type, Treatment) +
                C(year, Sum) * C(shipping_type, Treatment) +
                C(source_country, Sum) * C(target_country, Sum)""",
    data=train,
).fit()
logging.info(model.summary())

logging.info(
    "R2 statistic on test set: {}".format(r2_score(test["target"], model.predict(test)))  # type: ignore
)

example_sellers = test.seller_id.unique()  # type: ignore
example_sellers_data = test[test.seller_id.isin(example_sellers)].copy()  # type: ignore

for shipping_type in ["A", "B"]:
    example_sellers_data["shipping_type"] = shipping_type
    predictions = model.get_prediction(example_sellers_data).summary_frame(alpha=0.05)
    example_sellers_data[f"prediction_{shipping_type}"] = predictions["mean"]
    example_sellers_data[f"lower_ci_{shipping_type}"] = predictions["obs_ci_lower"]
    example_sellers_data[f"upper_ci_{shipping_type}"] = predictions["obs_ci_upper"]
predicted = example_sellers_data.groupby("seller_id")[
    [
        "target",
        "lower_ci_A",
        "prediction_A",
        "upper_ci_A",
        "lower_ci_B",
        "prediction_B",
        "upper_ci_B",
    ]
].agg("sum")
predicted["order"] = predicted["prediction_A"] - predicted["prediction_B"]

logging.info("Sellers results if he used A:")
logging.info(
    predicted[
        [
            "target",
            "lower_ci_A",
            "prediction_A",
            "upper_ci_A",
            'order'
        ]
    ].sort_values("order")
)

logging.info("Sellers results if he used B:")
logging.info(
    predicted[
        [
            "target",
            "lower_ci_B",
            "prediction_B",
            "upper_ci_B",
            'order'
        ]
    ].sort_values("order")
)