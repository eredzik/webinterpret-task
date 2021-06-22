-- checking structure
select *
from transactions
limit 500;
select *
from categories
limit 500;
select *
from counts
limit 500;
-- Main query to select data from database
with temp1 as (
    select target_country,
        source_country,
        category_id,
        shipping_type,
        year,
        sum(item_count) as item_count
    from counts
    group by target_country,
        source_country,
        category_id,
        shipping_type,
        year
)
SELECT t1.*,
    t2.category_id,
    t3.item_count,
    t3.year
from transactions t1
    left join categories t2 on t1.item_id = t2.item_id
    left join temp1 t3 on t1.target_country = t3.target_country
    and t1.source_country = t3.source_country
    and t2.category_id = t3.category_id
    and t1.shipping_type = t3.shipping_type
    and strftime('%Y', t1.timestamp) = t3.year
limit 500;
-- Verifying number of categories within each shipping type
select t2.category_id,
    t1.shipping_type,
    count(*),
    avg(active_gmv) as vv
from transactions t1
    left join categories t2 on t1.item_id = t2.item_id
group by t2.category_id,
    t1.shipping_type;
-- Veryfying number of sellers
select seller_id,
    count(*)
from transactions
group by seller_id;
-- Below we can see that there is are some duplicate values in data - shipping type A has duplicate values.
select *
from counts
where target_country = 'UK'
    and source_country = 'IT'
    and category_id = '131090';
select *
from transactions
where active_gmv < 1;
select distinct category_id
from transactions t1
    left join categories t2 on t1.item_id = t2.item_id;