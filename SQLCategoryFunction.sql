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


-- create new category --
-- create_category(name, id_type)
-- return void
CREATE OR REPLACE function create_category(
	p_name text,
    p_id_type int
)
returns void
language plpgsql    
as $$  
begin
    insert into category (name, id_type)
    values (p_name, p_id_type);
end;$$;

-- update category --
-- update_category(id_category, name)
-- return void
CREATE OR REPLACE function update_category(
	p_id_category int,
    p_name text
)
returns void
language plpgsql    
as $$
--Declare  
--err integer;  
begin
    update category
    set name = p_name
    where id_category = p_id_category;
end;$$;

-- delete category --
-- delete_category(id_category)
-- return void
CREATE OR REPLACE function (
	p_id_category int
)
returns void
language plpgsql    
as $$
--Declare  
--err integer;  
begin
    delete from category
    where id_category = p_id_category
end;$$;

-- view all category information--
-- select_category(id_type)
-- return table()
CREATE OR REPLACE function select_category(
	p_id_type int default null
)
returns table(
    err int,
    id_category int,
    name text,
    id_type int
)
language plpgsql    
as $$
-- Declare  
-- err integer;  
begin
    if p_id_category is not null then
        return query
        select 1, c.id_category, c.name, c.id_type
        from category c
        where c.id_type = p_id_type
    else
        return query
        select 1, c.id_category, c.name, c.id_type
        from category c
    end if;
end;$$;

-- view all type information --
-- select_type()
-- return table
CREATE OR REPLACE function select_type()
returns table(
    id_type int,
    name text
)
language plpgsql    
as $$
--Declare  
--err integer;  
begin
    select id_type, name
    from product_type
end;$$;