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

-- create new comment --
-- create_comment(username, id_product, content)
-- return id_comment
CREATE OR REPLACE function create_comment(
	p_username int,
    p_id_product int,
    p_content text
)
returns void
language plpgsql    
as $$
Declare  
id integer;  
begin
    insert into comment(username, id_product, content)
    value(p_username, p_id_product, p_content)
    returning id_comment into id;
    return id;
end;$$;

-- list comment --
-- select_comment(id_product)
-- return void
CREATE OR REPLACE function (
	p_id_product int
)
returns table(
    id_comment int,
    id_role int,
    name text,
    content text
)
language plpgsql    
as $$
--Declare  
--err integer;  
begin
    return query
    select t.id_comment, t.id_role, c.name, t.content
    from (select a.username as username, a.id_role as id_role, c.content as content, c.id_comment as id_comment
    from comment c, account a
    where c.username = a.username and c.id_product = p_id_product) t
    left join customer c
    on c.username = t.username;
end;$$;