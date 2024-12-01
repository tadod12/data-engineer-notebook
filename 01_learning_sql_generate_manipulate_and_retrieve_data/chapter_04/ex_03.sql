SELECT *
FROM payment
WHERE amount NOT IN (1.98, 7.98, 9.98)
ORDER BY amount;