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
-- create_product(id_category, name, discription, quantity, listed_price, image_arr)
-- return void
CREATE OR REPLACE function create_product(
    p_id_category int,
    p_name text,
    p_description text,
    p_quantity int,
    p_listed_price int,
	p_id_image int[]
)
returns int
language plpgsql    
as $$
Declare  
id integer;  
begin
    insert into product(id_category, name, description, quantity, listed_price, current_price, id_image)
    values (p_id_category, p_name, p_description, p_quantity, p_listed_price, p_listed_price, p_id_image)
    returning id_product into id;
    return id;
end;$$;


-- return query
-- 	select id_image 
-- 	from image
-- 	where id_image = any(ar);