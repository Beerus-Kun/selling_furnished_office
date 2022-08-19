-- create new account --
-- create_account(username, password, id_role, name, gender, email, phone)
-- return -2 (created)| -1 (exists user) | 0 (email or phone no valid) | 1 

-- select create_bill('123', 'name', 'email', 'address', 1, array[2], array[2], 'HBFIDA')

CREATE OR REPLACE function create_bill(
	p_phone text,
    p_name text,
	p_email text,
	p_address text,
    -- total
    p_id_status int,
    p_id_product int[],
    p_quantity int[],
    p_id_coupon text default null
)
returns record
language plpgsql    
as $$
Declare 
ret record;
p_total integer := 0;
p_discount int := (
	select value
	from coupon
	where id_coupon = p_id_coupon and CURRENT_TIMESTAMP < expiration_date and quantity > 0
);
p_id_bill int;
p_price int;
begin
    if p_discount is null then p_discount:=0; p_id_coupon := null; 
	else 
		update coupon
		set quantity = quantity - 1
		where id_coupon = p_id_coupon;
	end if;
	insert into bill (phone, address, id_coupon, id_status, name, email) values
	(p_phone, p_address, p_id_coupon, p_id_status, p_name, p_email) returning id_bill into p_id_bill;
	for i in 1..array_length(p_id_product, 1) loop
		if not exists(
            select * 
            from product p
            where p.id_product = p_id_product[i] and p.quantity > p_quantity[i]
        ) then
            -- return query
            select -1, p.name, p.quantity
            from product p
            where p.id_product = p_id_product[i] into ret;
            return ret;
        end if;
	end loop;

    for i in 1..array_length(p_id_product, 1) loop
		update product
        set quantity = (quantity - p_quantity[i])
        where id_product = p_id_product[i]
        returning current_price into p_price;

        p_total := p_total + p_price * p_quantity[i];

        insert into product_bill (id_bill, id_product, quantity, price, is_rating)
        values (p_id_bill, p_id_product[i], p_quantity[i], p_quantity[i]*p_price, 0::int2);
	end loop;
    if p_discount > p_total then p_discount := p_total; end if;

    update bill b
    set total = p_total - p_discount
    where b.id_bill = p_id_bill;
	
    select p_total - p_discount into ret;
	return ret;
end;$$;



CREATE OR REPLACE function check_bill(
    p_id_product int[],
    p_quantity int[],
    p_id_coupon text default null
)
returns record
language plpgsql    
as $$
Declare  
ret record;
p_total integer := 0;
p_discount int := (
	select value
	from coupon
	where id_coupon = p_id_coupon and CURRENT_TIMESTAMP < expiration_date and quantity > 0
);
p_price int;
begin
    if p_discount is null then p_discount:=0; p_id_coupon := null; 
	else 
		update coupon
		set quantity = quantity - 1
		where id_coupon = p_id_coupon;
	end if;
	for i in 1..array_length(p_id_product, 1) loop
		if not exists(
            select * 
            from product p
            where p.id_product = p_id_product[i] and p.quantity > p_quantity[i]
        ) then
            select -1, p.name, p.quantity
            from product p
            where p.id_product = p_id_product[i] into ret;
            return ret;

        else
            p_price := (
                select current_price
                from product p
                where p.id_product = p_id_product[i]
            );
            p_total := p_total + p_price * p_quantity[i];
        end if;
	end loop;

    if p_discount > p_total then p_discount := p_total; end if;

	select p_total - p_discount into ret;
	return ret;
end;$$;

drop function select_bill(
    text
)

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


CREATE OR REPLACE function select_product_bill(
    p_id_bill text
)
returns table(
    name text,
    image text,
    quantity int,
    price int
)
language plpgsql    
as $$
Declare  

begin
    return query(
        select b.id_bill, TO_CHAR(b.date_time :: time, 'hh24:mi:ss'), TO_CHAR(b.date_time :: date, 'dd/mm/yyyy'), b.address, b.total, c.value, b.id_status, b.name, b.email
        from bill b
		left join coupon c
		on b.id_coupon = c.id_coupon
        where b.phone = p_phone
        order by b.id_bill DESC
    );
end;$$;

CREATE OR REPLACE function cancel_bill(
    p_id_bill int,
    p_phone text
)
returns int
language plpgsql    
as $$
Declare  

begin
    if exists(
        select *
        from bill b
        where b.id_bill = p_id_bill and b.phone = p_phone and b.id_status <3 and b.id_status > 0
    ) then
        update bill
        set id_status = 0
        where id_bill = p_id_bill;
		with tempt as (
			select id_product, quantity
			from product_bill
			where id_bill = p_id_bill
		)
		
		update product
		SET quantity = product.quantity + t.quantity
		FROM tempt t
		WHERE product.id_product = t.id_product;
-- 			INNER JOIN
-- 			product p
-- 			ON p.id_product = t.id_product;
		return 1;
    else
        return -1;
    end if;
end;$$;


CREATE OR REPLACE function manager_select_bill(
    p_type int
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
    if p_type = 1 then
        return query(
            select b.id_bill, TO_CHAR(b.date_time :: time, 'hh24:mi:ss'), TO_CHAR(b.date_time :: date, 'dd/mm/yyyy'), b.address, b.total, c.value, b.id_status, b.name, b.email
            from bill b
		    left join coupon c
		    on b.id_coupon = c.id_coupon
            where b.id_status = 1 or b.id_status = 2
            order by b.id_bill
        );
    elsif p_type = 2 then
        return query(
            select b.id_bill, TO_CHAR(b.date_time :: time, 'hh24:mi:ss'), TO_CHAR(b.date_time :: date, 'dd/mm/yyyy'), b.address, b.total, c.value, b.id_status, b.name, b.email
            from bill b
		    left join coupon c
		    on b.id_coupon = c.id_coupon
            where b.id_status = 3 or b.id_status = 4
            order by b.id_bill
        );
    elsif p_type = 3 then
        return query(
            select b.id_bill, TO_CHAR(b.date_time :: time, 'hh24:mi:ss'), TO_CHAR(b.date_time :: date, 'dd/mm/yyyy'), b.address, b.total, c.value, b.id_status, b.name, b.email
            from bill b
		    left join coupon c
		    on b.id_coupon = c.id_coupon
            where b.id_status = 5
            order by b.id_bill
        );
    else
        return query(
            select b.id_bill, TO_CHAR(b.date_time :: time, 'hh24:mi:ss'), TO_CHAR(b.date_time :: date, 'dd/mm/yyyy'), b.address, b.total, c.value, b.id_status, b.name, b.email
            from bill b
		    left join coupon c
		    on b.id_coupon = c.id_coupon
            where b.id_status = 0
            order by b.id_bill
        );
    end if;
end;$$;


CREATE OR REPLACE function manager_next_step_bill(
    p_id_bill int
)
returns int
language plpgsql    
as $$
Declare  
p_current int := (
	select id_status
	from bill b
	where b.id_bill = p_id_bill
);
begin
    if p_current = 1 or p_current = 2
    then
        update bill
        set id_status = id_status + 2
        where id_bill = p_id_bill;
    elsif p_current = 3 or p_current = 4
    then
        update bill
        set id_status = 5
        where id_bill = p_id_bill;

    end if;
end;$$;


CREATE OR REPLACE function manager_cancel_bill(
    p_id_bill int
)
returns int
language plpgsql    
as $$
Declare  

begin
    if exists(
        select *
        from bill b
        where b.id_bill = p_id_bill and b.id_status > 0 and b.id_status < 5
    ) then
        update bill
        set id_status = 0
        where id_bill = p_id_bill;
		with tempt as (
			select id_product, quantity
			from product_bill
			where id_bill = p_id_bill
		)
		
		update product
		SET quantity = product.quantity + t.quantity
		FROM tempt t
		WHERE product.id_product = t.id_product;
-- 			INNER JOIN
-- 			product p
-- 			ON p.id_product = t.id_product;
		return 1;
    else
        return -1;
    end if;
end;$$;