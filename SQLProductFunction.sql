-- create new category --
-- create_category(name, id_type)
-- return void
-- CREATE OR REPLACE function (
	
-- )
-- returns void
-- language plpgsql    
-- as $$
-- --Declare  
-- --err integer;  
-- begin
    
-- end;$$;

-- select * from test(array [1,2,3,4,5,6])

-- create new product --
-- create_product(id_category, name, discription, quantity, listed_price, arr image)
-- return id
CREATE OR REPLACE function create_product(
    p_id_category int,
    p_name text,
    p_description text,
    p_quantity int,
    p_listed_price int,
	p_image text
)
returns int
language plpgsql    
as $$
Declare  
id integer;  
begin
    insert into product(id_category, name, description, quantity, listed_price, current_price, image)
    values (p_id_category, p_name, p_description, p_quantity, p_listed_price, p_listed_price, p_image)
    returning id_product into id;
    return id;
end;$$;

-- update product --
-- update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
-- return void
CREATE OR REPLACE function update_product(
    p_id_product int,
	p_id_category int,
    p_name text,
    p_description text,
    p_quantity int,
    p_listed_price int,
	p_image text
)
returns void
language plpgsql    
as $$
--Declare  
--err integer;  
begin
-- insert into product(id_category, name, description, quantity, listed_price, current_price, image)
--     values (p_id_category, p_name, p_description, p_quantity, p_listed_price, p_listed_price, p_image)
    update product
    set id_category = p_id_category, name = p_name, quantity = p_quantity, description = p_description, current_price = p_listed_price, image = p_image
    where id_product = p_id_product;
end;$$;

-- buy product --
-- buy_product(arr id_product, arr quantity)
-- return int -1, 1
CREATE OR REPLACE function buy_product(
	p_id_product int[],
    p_quantity int[]
)
returns int
language plpgsql    
as $$
Declare  
num1 integer;
num2 integer;
begin
    num1 = array_length(p_id_product, 1);
    num2 = array_length(p_quantity, 1);
    if num1 <> num2 then
        return -1;
    else 
        for i in 1..num1 loop
            update product
            set quantity = quantity - p_quantity[i]
            where id_product = p_id_product[i];
        end loop;
		return 1;
    end if;
end;$$;

-- select product --
-- select_product()
-- return table
CREATE OR REPLACE function select_product(
	p_id_category int default null
)
returns table(
    id_product int,
    id_category int,
    name text,
    description text,
    listed_price int,
    current_price int,
    quantity int,
    score float,
    review_turn int,
    image text,
	category_name text
)
language plpgsql    
as $$
--Declare  
--err integer;  
begin
	if p_id_category is null or p_id_category = 0 then
		return query
		select p.*, c.name
		from product p
		join category c
		on p.id_category = c.id_category
        order by (p.quantity >0 is false), score desc, review_turn desc;
	else
		return query
		select p.*, c.name
		from product p
		join category c
		on p.id_category = c.id_category
		where p.id_category = p_id_category
		order by (p.quantity >0 is false), score desc, review_turn desc;
	end if;
end;$$;

-- review product --
-- review_product(arr id_product, arr score)
-- return int
CREATE OR REPLACE function review_product(
	p_id_product int[],
    p_score int[]
)
returns int
language plpgsql    
as $$
Declare  
num1 integer;
num2 integer;
begin
    num1 = array_length(p_id_product, 1);
    num2 = array_length(p_score, 1);
    if num1 <> num2 then
        return -1;
    else 
        for i in 1..num1 loop
            update product
            set score = score + (p_score[i] - score)/(review_turn + 1),
                review_turn = review_turn + 1
            where id_product = p_id_product[i];
        end loop;
		return 1;
    end if;
end;$$;


CREATE OR REPLACE function product_search(
	p_name text,
	p_id_category int default null
)
returns table(
    id_product int,
    id_category int,
    name text,
    description text,
    listed_price int,
    current_price int,
    quantity int,
    score float,
    review_turn int,
    image text,
	category_name text
)
language plpgsql    
as $$
begin
    if p_id_category is null or p_id_category = 0 then
		return query
		select p.*, c.name
		from product p
		join category c
		on p.id_category = c.id_category
		where p.name ILIKE p_name
        order by (p.quantity >0 is false), score desc, review_turn desc;
	else
		return query
		select p.*, c.name
		from product p
		join category c
		on p.id_category = c.id_category
		where p.id_category = p_id_category and p.name ILIKE p_name
		order by (p.quantity >0 is false), score desc, review_turn desc;
	end if;
end;$$;

CREATE OR REPLACE function rate_product(
	p_id_product int,
    p_score int,
	p_id_bill int
)
returns void
language plpgsql    
as $$
begin
    update product
            set score = score + (p_score - score)/(review_turn + 1),
                review_turn = review_turn + 1
            where id_product = p_id_product;
	update product_bill 
	set is_rating = 1::int2
	where id_bill = p_id_bill and id_product = p_id_product;
end;$$;

CREATE OR REPLACE function select_bill(
    p_phone text
)
returns table(
    id_bill integer,
    "time" text,
    date text,
    address text, 
    total int, 
    discount int, 
    id_status int, 
    name text, 
    email text
)
language plpgsql    
as $$
Declare  

begin
    return query(
        select b.id_bill, TO_CHAR(b.date_time :: time, 'hh24:mi:ss'), TO_CHAR(b.date_time :: date, 'dd/mm/yyyy'), b.address, b.total, c.value, b.id_status, b.name, b.email
        from bill b, coupon c
        where b.phone = p_phone and b.id_coupon = c.id_coupon
        order by b.id_bill DESC
    );
end;$$;


CREATE OR REPLACE function delete_product(
	p_id_product int
)
returns int
language plpgsql    
as $$
begin
    if exists (
        select * from product_bill p where p.id_product = p_id_product
    ) then
        return -1;
    else
        delete from product p where p.id_product = p_id_product;
        return 1;
    end if;
end;$$;
