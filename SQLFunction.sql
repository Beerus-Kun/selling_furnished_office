-- create new account --
-- create_account(username, password, name, id_role, gender, email, phone)
-- return -1 (exists user) | 0 (email or phone no valid) | 1 

CREATE OR REPLACE function create_account(
	p_username text,
	p_password text,
	p_name text,
	p_id_role integer,
	p_gender smallint default null,
	p_email text default null,
	p_phone text default null
)
returns int
language plpgsql    
as $$
Declare  
err integer;  
begin
    if exists (
		select * 
        from account 
        where username = p_username
	) then
		err = -1;
		return err;
	else
		insert into account(username, password, name, id_role)
		values (p_username, p_password, p_name, p_id_role);
	end if;
	
	if p_id_role = 3 then
        if exists(
            select *
            from customer
            where email = p_email or phone = p_phone
        ) then
            delete from account
            where username = p_username;
            err = 0;
            return err;
        else
            insert into customer(gender, email, phone, username)
            values(p_gender, p_email, p_phone, p_username);
        end if;
	end if;
	err = 1;
	return err;
end;$$;


-- update account --
-- update_account(username, name, gender, email, phone) --
-- return -1 (no exists user) | 0 (email or phone no valid) | 1 

CREATE OR REPLACE function update_account(
	p_username text,
	p_name text,
	p_gender smallint default null,
	p_email text default null,
	p_phone text default null
)
returns int
language plpgsql    
as $$
Declare  
err integer;
begin
    if exists (
		select * 
        from account 
        where username = p_username
	) then
        update account
        Set name = p_name
        where username = p_username;

        if exists(
            select * 
            from customer 
            where username = p_username and email = p_email and phone = p_phone
        ) then
            update customer
            set gender = p_gender
            where username = p_username;
            err = 1;
            return err;
        elsif exists(
            select *
            from customer
            where username <> p_username and (email = p_email or phone = p_phone)
        ) then
            err = 0;
            return err;
        elsif exists(
            select *
            from customer
            where username = p_username
        ) then
            update customer
            set gender = p_gender, email = p_email, phone = p_phone
            where username = p_username;
            err = 1;
            return err;
        else
            err = 1;
            return err;
        end if;
	else
		err = -1;
		return err;
    end if;
end;$$;

-- update password --
-- update_password(username, password) --
-- return -1 | 1

CREATE OR REPLACE function update_password(
	p_username text,
	p_password text
)
returns int
language plpgsql    
as $$
Declare  
err integer;  
begin
    if exists(
        select * 
        from account a
        where a.username = p_username
    ) then
        update account
        set password = p_password
        where username = p_username;
        err = 1;
        return err;
    else
        err = -1;
        return err;
    end if;
end;$$;


-- update code --
-- update_code(username, code) --
-- return -1 | 1

CREATE OR REPLACE function update_code(
	p_username text,
	p_code text
)
returns int
language plpgsql    
as $$
Declare  
err integer;  
begin
    if exists(
        select * 
        from account a
        where a.username = p_username
    ) then
        update account
        set code = p_code, expired_code = CURRENT_TIMESTAMP + interval '10 minutes'
        where username = p_username;
        err = 1;
        return err;
    else
        err = -1;
        return err;
    end if;
end;$$;

-- select account --
-- select_account(username) --
-- return -1 (no exists user) | 1 table select * from

CREATE OR REPLACE function select_account(
	p_username text
)
returns table(
    err integer,
    username text,
    name text,
    id_role integer,
    gender smallint,
    email text,
    phone text
)
language plpgsql    
as $$
Declare  
err integer;
begin
    if exists(
        select *
        from account a
        where a.username = p_username
    ) then
        return query
        select 1, a.username, a.name, a.id_role, c.gender, c.email, c.phone
        from account a
        left join customer c on a.username = c.username
        where a.username = p_username;
    else
        return query
        select select -1, null, null, 0, 0::smallint, null, null;
    end if;

end;$$;


-- select password --
-- select_password(username) --
-- return -1 (no exists user) | 1 table select * from

CREATE OR REPLACE function select_password(
	p_username text
)
returns table(
    err integer,
    password text
)
language plpgsql    
as $$
Declare  
err integer;
begin
    if exists(
        select *
        from account a
        where a.username = p_username
    ) then
        return query
        select 1, a.password
        from account a
        where a.username = p_username;
    else
        return query
        select -1, null;
    end if;

end;$$;

-- select code --
-- select_code(username) --
-- return -1 (no exists user) | 0 (expired) | 1 table select * from

CREATE OR REPLACE function select_code(
	p_username text
)
returns table(
    err integer,
    code text
)
language plpgsql    
as $$
Declare  
err integer;
begin
    if exists(
        select *
        from account a
        where a.username = p_username
    ) then
        
        return query
        select (case 
	        when a.code_expired <= CURRENT_TIMESTAMP 
	        then 0
	        else 1
	        end
        )
        , a.code
        from account a
        where username = p_username;
    else
        return query
        select -1, null;
    end if;

end;$$;