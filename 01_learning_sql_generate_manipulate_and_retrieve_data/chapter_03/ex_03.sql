SELECT DISTINCT r.customer_id
FROM rental r
WHERE date(r.rental_date) = '2005-07-05';