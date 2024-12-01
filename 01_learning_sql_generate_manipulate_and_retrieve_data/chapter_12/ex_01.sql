DROP TABLE IF EXISTS Account, Transaction;

CREATE TABLE Account
(
    account_id         INT,
    avail_balance      INT,
    last_activity_date DATETIME,
    CONSTRAINT pk_account PRIMARY KEY (account_id)
);

CREATE TABLE Transaction
(
    txn_id      INT,
    txn_date    DATE,
    account_id  INT,
    txn_type_cd ENUM ('C', 'D'),
    amount      INT,
    CONSTRAINT pk_transaction PRIMARY KEY (txn_id),
    CONSTRAINT fk_trans_acc FOREIGN KEY (account_id) REFERENCES Account (account_id)
);

INSERT INTO Account
VALUES (123, 500, '2019-07-10 20:53:27'),
       (789, 75, '2019-06-22 15:18:35');

INSERT INTO Transaction
VALUES (1001, '2019-05-15', 123, 'C', 500),
       (1002, '2019-06-01', 789, 'C', 75);

START TRANSACTION;

INSERT INTO Transaction
VALUES (1003, now(), 123, 'D', 50),
       (1004, now(), 789, 'C', 50);

UPDATE Account
SET avail_balance = avail_balance - 50, last_activity_date = now()
WHERE account_id = 123;

UPDATE Account
SET avail_balance = avail_balance + 50, last_activity_date = now()
WHERE account_id = 789;

COMMIT;

SELECT * FROM Transaction NATURAL JOIN Account;
