CREATE TABLE customer (
    --c_custkey integer PRIMARY KEY,
    --c_vinID integer not null,
    c_Lname	varchar(45) not null,
    c_Fname	varchar(45) not null,
    c_age integer not null,
    c_phone	varchar(45) not null,	
    c_address varchar(45) not null,	
    c_city varchar(45) not null,	
    c_state	varchar(2) not null,
    c_email	varchar(45) not null
);

CREATE TABLE seller (
    --s_sellerkey integer PRIMARY KEY,
    --s_vinID integer not null,
    s_name varchar(45) not null,
    s_phone varchar(45) not null,
    s_city varchar(45) not null,
    s_state varchar(2) not null,
    s_email varchar(50) not null
);

CREATE TABLE manufacturer (
    m_name varchar(50) not null,
    m_email varchar(50) not null,
    m_address varchar(50) not null,
    m_city_state varchar(50) not null,
    m_model varchar(50) not null
);

CREATE TABLE transactions (
    t_trkey integer PRIMARY KEY,
    t_custkey integer NOT NULL,
    t_sellerkey integer NOT NULL,
    t_VIN integer NOT NULL,
    t_date datetime NOT NULL
);

CREATE TABLE automobile (
    a_vinID integer PRIMARY KEY,
    a_model varchar(45) not null,
    a_type varchar(45) not null,
    a_year integer not null,
    a_condition varchar(5) not null,
    a_price decimal(11,2) not null,
    a_color varchar(45) not null,
    a_location integer not null
);

CREATE TABLE warehouse (
    w_name varchar(45) not null,
    w_city varchar(45) not null,
    w_state	varchar(2) not null,
    w_inventory integer not null
);