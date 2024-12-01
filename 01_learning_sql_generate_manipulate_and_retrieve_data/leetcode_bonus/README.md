# Code learn from leetcode

## Define Window function

    SELECT DISTINCT visited_on, 
        SUM(amount) OVER w AS amount,
        ROUND((SUM(amount) OVER w)/7, 2) AS average_amount
    FROM customer
    WINDOW w AS (
        ORDER BY visited_on
        RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW
    )
    LIMIT 6, 999;