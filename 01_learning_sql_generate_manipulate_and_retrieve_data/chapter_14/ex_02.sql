DROP VIEW IF EXISTS country_cus_payments;

CREATE VIEW country_cus_payments (country, tot_payments)
AS
SELECT co.country, (
       SELECT SUM(p.amount)
       FROM payment p
        INNER JOIN customer cu ON p.customer_id = cu.customer_id
        INNER JOIN address a ON cu.address_id = a.address_id
        INNER JOIN city ci ON a.city_id = ci.city_id
       WHERE ci.country_id = co.country_id
    )
FROM country co;

SELECT *
FROM country_cus_payments;
