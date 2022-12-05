SELECT * FROM automobile;
SELECT * FROM customer;
SELECT * FROM manufacturer;
SELECT * FROM seller;
SELECT * FROM transactions;
SELECT * FROM warehouse;

--1) Returns vehicle when ONLY make is entered
SELECT *--a_VIN, a_model, a_type, a_year, a_condition, a_color, a_price
FROM automobile
WHERE a_make = 'Chevrolet';
--Returns vehicle when ONLY year is entered
SELECT * 
FROM automobile
WHERE a_year = 2022;
--Returns vehicle when ONLY condition is entered
SELECT *
FROM automobile
WHERE a_condition = "New";
--Returns vehicle when ONLY type is entered
SELECT * 
FROM automobile
WHERE a_type = "Sedan";

--2) Returns vehicle when make AND model are entered
SELECT *
FROM automobile
WHERE a_make = 'Chevrolet'
    AND a_model = 'Tahoe';
--Returns vehicle when ONLY model is entered
SELECT *
FROM automobile
WHERE a_model = 'Camry';
--Returns for year entered
SELECT *
FROM automobile
WHERE a_year = 2022;
--Returns for make AND year
SELECT *
FROM automobile
WHERE a_make = 'Ford'
    AND a_year = 2021;

