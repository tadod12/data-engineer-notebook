ALTER TABLE rental
ADD CONSTRAINT fk_rental_customer FOREIGN KEY (customer_id)
    REFERENCES customer(customer_id) ON DELETE RESTRICT;