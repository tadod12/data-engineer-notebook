SELECT title
FROM film
WHERE film_id IN (
    SELECT fc.film_id
    FROM film_category fc
        INNER JOIN category c
            ON fc.category_id = c.category_id
    WHERE c.name = 'Action'
    );
