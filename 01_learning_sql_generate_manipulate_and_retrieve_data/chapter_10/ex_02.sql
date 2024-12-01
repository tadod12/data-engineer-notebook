SELECT customer.name, sum(payment.amount)
FROM (
    SELECT 101 payment_id, 1 customer_id, 8.99 amount
    UNION ALL
    SELECT 102 payment_id, 3 customer_id, 4.99 amount
    UNION ALL
    SELECT 103 payment_id, 1 customer_id, 7.99 amount
) payment
    RIGHT OUTER JOIN (
        SELECT 1 customer_id, 'John Smith' name
        UNION ALL
        SELECT 2 customer_id, 'Kathy Jones' name
        UNION ALL
        SELECT 3 customer_id, 'Greg Oliver' name
    ) customer
    ON customer.customer_id = payment.customer_id
GROUP BY customer.name;