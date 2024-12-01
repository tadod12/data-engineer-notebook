SELECT ad1.address, ad2.address
FROM address ad1
    INNER JOIN address ad2
    ON ad1.city_id = ad2.city_id
WHERE ad1.address <> ad2.address;