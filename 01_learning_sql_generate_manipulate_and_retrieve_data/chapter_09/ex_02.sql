SELECT title
FROM film f
WHERE EXISTS(
    SELECT 1
    FROM film_category fc
        INNER JOIN category c
            ON fc.category_id = c.category_id
    WHERE c.name = 'Action'
        AND fc.film_id = f.film_id
);
