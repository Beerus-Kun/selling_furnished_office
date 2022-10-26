CREATE OR REPLACE function create_comment(
	p_username text,
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
    values(p_username, p_id_product, p_content);
end;$$;

-- list comment --
-- select_comment(id_product)
-- return void
CREATE OR REPLACE function select_comment(
	p_id_product int
)
returns table(
    id_comment int,
    id_role int,
    name text,
    content text,
    username text
)
language plpgsql    
as $$
--Declare  
--err integer;  
begin
    return query
    select t.id_comment, t.id_role, c.name, t.content, t.username
    from (select a.username as username, a.id_role as id_role, c.content as content, c.id_comment as id_comment
    from comment c, account a
    where c.username = a.username and c.id_product = p_id_product) t
    left join customer c
    on c.username = t.username
	order by t.id_comment;
end;$$;