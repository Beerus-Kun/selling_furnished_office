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



-- create new image --
-- create_image(link)
-- return void
CREATE OR REPLACE function create_image(
	p_link text
)
returns int
language plpgsql    
as $$
Declare  
res integer;  
begin
    insert into image(link)
    values (p_link)
    returning id_image into res;
	return res;
end;$$;

-- delete image --
-- delete_image(id_image)
-- return void
CREATE OR REPLACE function delete_image (
	p_id_image int
)
returns void
language plpgsql    
as $$
--Declare  
--err integer;  
begin
    delete from image
    where id_image = p_id_image
end;$$;
