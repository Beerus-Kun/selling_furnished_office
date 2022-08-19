-- Set timezone --
SET timezone = 'Asia/Ho_Chi_Minh';

-- Role table -- 

CREATE TABLE role (
	id_role integer PRIMARY KEY,
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
    id_role serial,
    FOREIGN KEY(id_role) REFERENCES role(id_role)
);

-- Customer table --

CREATE TABLE customer(
    phone text PRIMARY KEY,
    email text UNIQUE,
    username text UNIQUE,
        -- notify_token text,
    name text,
    gender smallint, -- 1: nam, 0: nu
    FOREIGN KEY(username) REFERENCES account(username)
);

-- Product type table --
CREATE TABLE product_type (
	id_type integer PRIMARY KEY,
	name text
);

INSERT INTO product_type(id_type, name) VALUES
(1, 'Ghế'),
(2, 'Bàn');

-- Category table --
CREATE TABLE category(
    id_category serial PRIMARY KEY,
    id_type integer not NULL,
    name text,
    FOREIGN KEY (id_type) REFERENCES product_type(id_type)
);

INSERT INTO category(name, id_type) VALUES
('Bàn giám đốc - trưởng phòng', 2),
('Bàn họp', 2),
('Bàn nhân viên', 2),
('Bàn nhóm', 2),
('Bàn công thái học', 2),
('Ghế giám đốc - trưởng phòng', 1),
('Ghế xoay nhân viên', 1),
('Ghế chân quỳ', 1),
('Ghế băng chờ', 1),
('Ghế gấp', 1),
('Ghế công thái học', 1);

-- Product table --
CREATE TABLE product (
	id_product serial PRIMARY KEY,
    id_category integer,
	name text,
	description text,
	listed_price int,
	current_price int,
	quantity int,
    score float default 0,
    review_turn int default 0,
    image text,
    FOREIGN KEY (id_category) REFERENCES category(id_category)
);

-- Coupon table --
CREATE TABLE coupon(
    id_coupon text PRIMARY KEY,
    quantity integer,
    expiration_date timestamp,
    value int
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
(3, 'Đã giao'),
(4, 'Bị từ chối');

-- Bill table --

CREATE TABLE bill (
	id_bill serial PRIMARY KEY,
	phone text,
	date_time timestamp without time zone default CURRENT_TIMESTAMP NOT NULL,
	address text,
	total int,
    id_coupon text,
	id_status int,
    name text,

	FOREIGN KEY (phone) REFERENCES customer(phone),
    FOREIGN KEY(id_status) REFERENCES status(id_status),
    FOREIGN KEY(id_coupon) REFERENCES coupon(id_coupon)
);

-- Product_bill table --

CREATE TABLE product_bill(
    id_bill integer,
    id_product integer,
    quantity int,
    price int,
    is_rating smallint,

    FOREIGN KEY(id_bill) REFERENCES bill(id_bill),
    FOREIGN KEY(id_product) REFERENCES product(id_product),
    PRIMARY KEY(id_bill, id_product)
);

-- Comment table --

CREATE TABLE comment(
    id_comment serial PRIMARY KEY,
    id_product int not NULL,
    username text not NULL,
    content text,

    FOREIGN KEY(username) REFERENCES account(username),
    FOREIGN KEY(id_product) REFERENCES product(id_product)
);