SELECT * FROM automobile;
SELECT * FROM customer;
SELECT * FROM manufacturer;
SELECT * FROM seller;
SELECT * FROM transactions;
SELECT * FROM warehouse;

--1) Returns vehicle when ONLY make is entered
SELECT * FROM automobile WHERE a_make = 'Chevrolet';
--Returns vehicle when ONLY year is entered
SELECT *  FROM automobile WHERE a_year = 2022;
--Returns vehicle when ONLY condition is entered
SELECT * FROM automobile WHERE a_condition = "New";
--Returns vehicle when ONLY type is entered
SELECT *  FROM automobile WHERE a_type = "Sedan";
--Returns vehicle when ONLY price is entered
SELECT * FROM automobile WHERE a_price = 25000;

--2) make, model, year, condition, type, price
--Returns vehicle when make AND model are entered
SELECT * FROM automobile
WHERE a_make = 'Chevrolet' AND a_model = 'Tahoe';
--Returns for make AND year
SELECT * FROM automobile
WHERE a_make = 'Ford' AND a_year = 2021;
--Returns vehicle when make AND condition
SELECT * FROM automobile
WHERE a_make = 'Ford' AND a_condition = 'Used';
--Returns vehicle when make AND type entered
SELECT * FROM automobile
WHERE a_make = 'Toyota' AND a_type = 'Sedan';
--Returns vehicles when make AND price entered
SELECT * FROM automobile
WHERE a_make = 'Dodge' AND a_price = 20000;
--year AND condition (COULD BE REDUNDANT; MIGHT REMOVE LATER)
SELECT * FROM automobile 
WHERE a_year = 2021 AND a_condition = 'Used';
--year AND  type
SELECT * FROM automobile
WHERE a_year = 2021 AND a_type = 'SUV';
--year AND price (REDUNDANT; COULD DELETE LATER)
SELECT * FROM automobile
WHERE a_year = 2019 AND a_price = 18000;
--condition AND type
SELECT * FROM automobile
WHERE a_condition = 'Used' AND a_type = 'SUV';
--type AND price
SELECT * FROM automobile
WHERE a_type = 'SUV' AND a_price = 30000;

SELECT (w_VIN + '-' + '1122') as t_trkey, w_VIN, s_name, a_price FROM warehouse, seller, automobile
        WHERE w_VIN = 3114
        AND w_sellerkey = s_sellerkey
        AND w_VIN = a_VIN;



INSERT INTO transactions values(a_VIN+'-'+c_custkey,a_VIN,(count(c_custkey)),s_name, a_price, date)