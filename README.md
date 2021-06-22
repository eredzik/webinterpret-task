# About
This is homework task for Webinterpret company.
The task is to verify impact of both shipping types on business.

# How to reproduce
Put the sqlite database into `./data` directory, run codes.

# To check
How much is sold with both shipping types - sum of GMV and sum of item counts
Control for time, category_id, shipping_type, source_country, target_country

To answer this I will build a regression model with formula:
```
Target ~
    alpha +
    beta1i * category_id_i +
    beta1i * category_id_i * shipping_type_b +
    beta2 * shipping_type_b +
    beta3j * year_j +
    beta3j * year_j * shipping_type_b +
    beta4k * source_country_k +
    beta5l * target_country_l +
    epsilon
```
With model built this way we can answer following questions:
Are shipping types different overall?
Is there any effect of shipping type for certain categories?
Is there any effect of shipping_type in certain years?


With following questions in mind we have another theoretic problem - how to formulate target variable.
Active_gmv is short for Gross Merchandise Value - this value alone in my opinion by itself can't tell whether shipping types differ - there could many other factors in play which are more important that shipping type.
I can scale that value with use of item_count variable as suggested by interviewer so that I get value that is proportional to overall interest in product. This value is not interpretable as far as I know but should give us estimates less biased by overall popularity of the product.
Because of skewness of the distribution (it seems to be lognormal) as target of model will be chosen log(active_gmv/item_count). It should be interpreted as higher the metric the better (more revenue per unit of available stock)
For modeling categorical data I used two encoding scenarios: Treatment and Sum encoding.
Treatment encoding encodes data with one reference level so effects from model (namely shipping type there) should be interpreted as effect of swapping reference to treatment (which is shipping B there).
Sum encoding gives estimates for all categories which should be interpreted as deviation from the mean of all parameters. It allows for less biased comparison and interpretation of parameters as we don't need any reference.

# Model results

Most of model parameters are statisticaly significant at statistical significance level of 0.05.
Model specified before seems to fit data quite nicely - it has acheived R-squared statistic of 0.6.

We can infer from that model that although shipping B has higher target metric hence better profitability, in many cases this effect is superseded by local effects for certain categories or source/target combination. With use of this model we could predict for given seller's inventory which shipping type he should use for which category or if he had to choose one, give him some objective metric about which one would be more beneficial on average.

For example i chosen some sellers from dataset:
| Seller_id | target_org  | target_predicted_A | Target_predicted_B                           | Decision                                     |
| --------- | ----------- | ------------------ | -------------------------------------------- | -------------------------------------------- |
| 116       | -326.328588 | -365.946997        | -312.731061                                  | Would benefit from switching everything to B |
| 91129     | -2.693849   | -3.748263          | Would benefit from switching everything to A |

But more informative for sellers would be information on what categories should have access to some shipping type -> that would maximize profit. It would require doing same exercise as above but aggregating not only by seller but also by category.

Confidence interval for predictions calculation is included in outputs of the `model.py` code.


# Problems with data

1. Below we can see that there is are some duplicate values in data - shipping type A has duplicate values.
    ```
    select *
    from counts
    where target_country='UK' and source_country='IT' and category_id='131090';
    ```
    - As remedy I used the assumption that those rows are not summed properly and should be summed.

2. Some target countries have non real values - maybe this data should be discarded? It has to be investigated by someone providing the data.