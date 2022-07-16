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


-- create new coupon --
-- create_coupon(id_coupone, months, value, amount)
-- return void
CREATE OR REPLACE function create_coupon(
	p_id_coupon text,
    p_month int,
    p_value int,
    p_amount int
)
returns void
language plpgsql    
as $$
-- Declare  
-- mon_txt text;  
begin
    insert into coupon(id_coupon, expiration_date, value, quantity)
    values(p_id_coupon, CURRENT_TIMESTAMP + interval '1 month' * p_month, p_value, p_amount);
end;$$;


-- select coupon --
-- select_coupon(id_coupon)
-- return -1 || 1
CREATE OR REPLACE function select_coupon(
	p_id_coupon text
)
returns table(
    err int,
    value int
)
language plpgsql    
as $$
-- Declare  
-- err integer;  
begin
    if exists(
        select *
        from coupon
        where id_coupon = p_id_coupon and CURRENT_TIMESTAMP < expiration_date and quantity > 0
    ) then
        return query
        select 1, c.value
        from coupon c
        where id_coupon = p_id_coupon;
    else
        return query
		select -1, 0;
	end if;
end;$$;
