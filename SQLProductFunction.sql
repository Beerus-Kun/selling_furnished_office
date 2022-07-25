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
    set id_category = p_id_category, name = p_name, quantity = p_quantity, description = p_description, listed_price = p_listed_price, image = p_image
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
    quantity int,
    listed_price int,
    current_price int,
    score float,
    review_turn int,
    image text
)
language plpgsql    
as $$
--Declare  
--err integer;  
begin
	if p_id_category is null then
		return query
		select * from product
		order by id_category, id_product;
	else
		return query
		select * 
		from product p
		where p.id_category = p_id_category
		order by p.id_product;
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