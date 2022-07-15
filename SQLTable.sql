-- Set timezone --
SET timezone = 'Asia/Ho_Chi_Minh';

-- Role table -- 

CREATE TABLE role (
	id_role serial PRIMARY KEY,
    name text
);

INSERT INTO role (id_role, name)
VALUES
(1, 'admin'),
(2, 'staff'),
(3, 'customer');


-- Account table --

CREATE TABLE account(
    username text PRIMARY KEY,
    password text,
    name text,
    id_role serial,
    code text,
    code_expired timestamp without time zone,
    FOREIGN KEY(id_role) REFERENCES role(id_role)
);

-- Customer table --

CREATE TABLE customer(
    gender smallint, -- 1: nam, 0: nu
    email text UNIQUE,
    phone text UNIQUE,
    username text PRIMARY KEY,
    wallet int default 0,
    date_created timestamp without time zone default CURRENT_TIMESTAMP NOT NULL,

    FOREIGN KEY(username) REFERENCES account(username)
);

-- Image table  --

CREATE TABLE image (
	id_image serial PRIMARY KEY,
	link text
);

-- Brand table --

CREATE TABLE brand (
	id_brand serial PRIMARY KEY,
	name varchar(30) UNIQUE
);

INSERT INTO brand (name)
VALUES
('Apple'),
('Asus'),
('Acer'),
('Dell'),
('Lenovo'),
('MSI'),
('Surface'),
('huawei');


-- Product table --

CREATE TABLE product (
	id_product serial PRIMARY KEY,
	id_brand serial NOT NULL,
	name text,
	description text,
	listed_price int,
	current_price int,
	quantity int,
    score float default 0,
    review_turn int default 0,

	FOREIGN KEY (id_brand) REFERENCES brand(id_brand)
);

-- Product_image table --

CREATE TABLE product_image(
	id_product serial,
    id_image serial,

    FOREIGN KEY(id_product) REFERENCES product(id_product),
    FOREIGN KEY(id_image) REFERENCES image(id_image),
    PRIMARY KEY(id_product, id_image)
);

-- Gift table --

CREATE TABLE gift(
    id_gift serial PRIMARY KEY,
    name text,
    id_image serial,
    exchange_value int,
    quantity int,

    FOREIGN KEY(id_image) REFERENCES image(id_image)
);

-- Product_gift table --

CREATE TABLE product_gift(
    id_gift serial,
    id_product serial,

    FOREIGN KEY(id_gift) REFERENCES gift(id_gift),
    FOREIGN KEY(id_product) REFERENCES product(id_product),
    PRIMARY KEY(id_gift, id_product)
);

-- Category table --

CREATE TABLE category(
    id_category serial PRIMARY KEY,
    name text
);

INSERT INTO category(id_category, name) VALUES
(1, 'Gaming'),
(2, 'Học tập, văn phòng'),
(3, 'Đồ họa'),
(4, 'Mỏng nhẹ'),
(5, 'Cao cấp'),
(6, 'Giảm sâu');

-- Product_category table --

CREATE TABLE product_category(
    id_category serial,
    id_product serial,
    FOREIGN KEY(id_category) REFERENCES category(id_category),
    FOREIGN KEY(id_product) REFERENCES product(id_product),
    PRIMARY KEY(id_category, id_product)
);

-- Voucher table --

CREATE TABLE voucher(
    id_voucher serial PRIMARY KEY,
    name text,
    effective_date timestamp,
    expiration_date timestamp,
    value int
);

-- Account_voucher table --

CREATE TABLE account_voucher(
    id_av serial PRIMARY KEY,
    username text,
    id_voucher serial,

    FOREIGN KEY(username) REFERENCES account(username),
    FOREIGN KEY(id_voucher) REFERENCES voucher(id_voucher)
);

-- Cart table --

CREATE TABLE cart(
    username text NOT NULL,
    id_product serial NOT NULL,
    quantity int,

    FOREIGN KEY(username) REFERENCES account(username),
    FOREIGN KEY(id_product) REFERENCES product(id_product),
    PRIMARY KEY(username, id_product)
);

-- Status table --

CREATE TABLE status(
    id_status serial PRIMARY KEY,
    name text
);

INSERT INTO status(id_status, name) VALUES
(0, 'Đã hủy'),
(1, 'Đã mua'),
(2, 'Đã thanh toán'),
(3, 'Đã giao');

-- Bill table --

CREATE TABLE bill (
	id_bill serial PRIMARY KEY,
	username text,
	date_time timestamp without time zone default CURRENT_TIMESTAMP NOT NULL,
	address text,
	total int,
    id_voucher serial,
    gift_discount int,
	id_status serial,
	-- status
		-- 0: huy hang
		-- 1: nhan don
		-- 2: dang giao
		-- 3: da giao
	FOREIGN KEY (username) REFERENCES account(username),
    FOREIGN KEY(id_status) REFERENCES status(id_status),
    FOREIGN KEY(id_voucher) REFERENCES voucher(id_voucher)
);

-- Product_bill table --

CREATE TABLE product_bill(
    id_bill serial,
    id_product serial,
    quantity int,
    price int,
    rating int,

    FOREIGN KEY(id_bill) REFERENCES bill(id_bill),
    FOREIGN KEY(id_product) REFERENCES product(id_product),
    PRIMARY KEY(id_bill, id_product)
);

-- Gift table --

CREATE TABLE gift_bill(
    id_gift serial,
    id_bill serial,
    quantity_received int,
    quantity_taken int,
    discount int,

    FOREIGN KEY(id_gift) REFERENCES gift(id_gift),
    FOREIGN KEY(id_bill) REFERENCES bill(id_bill),
    PRIMARY KEY(id_gift, id_bill)
);

-- Comment table --

CREATE TABLE comment(
    id_comment serial PRIMARY KEY,
    username text,
    content text,

    FOREIGN KEY(username) REFERENCES account(username)
);


-- Notification table --

CREATE TABLE notification(
    id_notification serial PRIMARY KEY,
    username text,
    title text,
    content text,

    FOREIGN KEY(username) REFERENCES account(username)
);