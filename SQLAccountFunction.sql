-- create new account --
-- create_account(username, password, id_role, name, gender, email, phone)
-- return -2 (created)| -1 (exists user) | 0 (email or phone no valid) | 1 
CREATE OR REPLACE function create_account(
	p_username text,
	p_password text,
	p_id_role integer,
    p_name text default null,
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
	end if;
	
	if p_id_role = 3 then
        if exists(
            select *
            from customer c
            where c.phone = p_phone and c.username is not null
        ) then
            err = -2;
            return err;
        elsif exists(
            select *
            from customer c
            where c.email = p_email and c.phone <> p_phone
        ) then
            err = 0;
            return err;
        elsif exists(
			select *
            from customer c
            where c.phone = p_phone
		) then
			insert into account(username, password, id_role)
            values (p_username, p_password, p_id_role);
			update customer c
			set gender = p_gender, email = p_email, username = p_username, name = p_name
			where c.phone = p_phone;
        else
            insert into account(username, password, id_role)
            values (p_username, p_password, p_id_role);
            insert into customer(gender, email, phone, username, name)
            values(p_gender, p_email, p_phone, p_username, p_name);
        end if;
    else
        insert into account(username, password, id_role)
        values (p_username, p_password, p_id_role);
	end if;
	err = 1;
	return err;
end;$$;

-- create temp customer --
-- create_temp_customer(phone)
CREATE OR REPLACE function create_temp_customer(
	p_phone text
)
returns int
language plpgsql    
as $$
Declare  
err integer;  
begin
    if not exists(
        select *
        from customer c
        where c.phone = p_phone
    ) then
        insert into customer (phone) values (p_phone);
    end if;

end;$$;

-- check username new account --
-- check_username(username)
-- return -1 | 1
CREATE OR REPLACE function check_username(
	p_username text
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
        err = 1;
        return err;
	end if;
end;$$;

-- check phone new account --
-- check_phone(phone)
-- return -1 | 1
CREATE OR REPLACE function check_phone(
	p_phone text
)
returns int
language plpgsql    
as $$
Declare  
err integer;  
begin
    if exists (
		select * 
        from customer 
        where phone = p_phone and username is not null
	) then
		err = -1;
		return err;
    else
        err = 1;
        return err;
	end if;
end;$$;

-- check email new account --
-- check_email(email)
-- return -1 | 1
CREATE OR REPLACE function check_email(
	p_email text
)
returns int
language plpgsql    
as $$
Declare  
err integer;  
begin
    if exists (
		select * 
        from customer 
        where email = p_email
	) then
		err = -1;
		return err;
    else
        err = 1;
        return err;
	end if;
end;$$;

-- update account --
-- update_account(name, gender, email, phone) --
-- return -1 (no exists user) | 0 (email no valid) | 1 
CREATE OR REPLACE function update_account(
	p_phone text,
	p_name text default null,
	p_gender smallint default null,
	p_email text default null
)
returns int
language plpgsql    
as $$
Declare  
err integer;
begin
    if exists (
		select * 
        from customer c 
        where c.email = p_email and c.phone <> p_phone
	) then
        err = 0;
        return err;
    elsif exists(
        select * 
        from customer c
        where c.phone = p_phone
    ) then
        update customer
        Set name = p_name, gender = p_gender, email = p_email
        where phone = p_phone;
        err =1;
        return err;
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

-- select customer account --
-- select_account(phone) --
-- return -1 (no exists user) | 1 table select * from
CREATE OR REPLACE function select_account(
	p_username text
)
returns table(
    err integer,
    name text,
    gender smallint,
    email text,
    phone text,
    id_role int
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
        select 1, c.name, c.gender, c.email, c.phone, a.id_role
        from account a
        left join customer c
        on a.username = c.username
        where a.username = p_username;
    else
        return query
        select -1, null, 0::smallint, null, null, 0;
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
