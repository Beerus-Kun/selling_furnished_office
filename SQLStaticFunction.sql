CREATE OR REPLACE function month_turnover(
    p_first_day date
)
returns table(
    date text,
    sum bigint
)
language plpgsql    
as $$

begin
    return query
    select TO_CHAR(date_time :: date, 'dd/mm/yyyy'), sum(total)
    from bill
    where 
    date_time >= p_first_day and 
    date_time <= (date_trunc('month', p_first_day::date) + 
    interval '1 month' - interval '1 day')::date 
    and id_status = 5
    group by date(date_time)
    order by date;
end;$$;

CREATE OR REPLACE function year_turnover(
    p_first_day date
)
returns table(
    month numeric,
    sum bigint
)
language plpgsql    
as $$

begin
    return query
    select EXTRACT(month from date_time) as month, sum(total)
    from bill
    where 
    date_time >= p_first_day and 
    date_time <= (p_first_day::date + interval '1 year' - interval '1 day')::date and 
    id_status = 5
    group by EXTRACT(month from date_time)
    order by month;
end;$$;


CREATE OR REPLACE function month_status(
    p_first_day date
)
returns table(
    cancel bigint,
    bought bigint,
    transported bigint,
	received bigint
)
language plpgsql    
as $$

begin
    return query
    select count(id_bill) FILTER (WHERE id_status = 0) AS cancel,
    count(id_bill) FILTER (WHERE id_status = 1 or id_status=2) AS bought, 
    count(id_bill) FILTER (WHERE id_status = 4 or id_status = 3) AS transported,
    count(id_bill) FILTER (WHERE id_status = 5) AS received
    from bill
    where 
    date_time >= p_first_day and date_time <= (p_first_day::date + interval '1 month' - interval '1 day')::date;
end;$$;


CREATE OR REPLACE function get_admin_year(
)
returns table(
    year int
)
language plpgsql    
as $$

begin
    return query
    select DISTINCT extract(year from date_time)::int
    from bill;
end;$$;

CREATE OR REPLACE function get_admin_month(
    p_year int
)
returns table(
    month int
)
language plpgsql    
as $$

begin
    return query
    select DISTINCT extract(month from date_time)::int
    from bill
    where extract(year from date_time) = p_year;
end;$$;

CREATE OR REPLACE function total_month_turnover(
    p_first_day date
)
returns bigint
language plpgsql    
as $$

begin
    return 
    (select sum(total)
    from bill
    where 
    date_time >= p_first_day and 
    date_time <= (date_trunc('month', p_first_day::date) + 
    interval '1 month' - interval '1 day')::date 
    and id_status = 5);
end;$$;

CREATE OR REPLACE function total_year_turnover(
    p_first_day date
)
returns bigint
language plpgsql    
as $$

begin
    return 
    (select sum(total)
    from bill
    where 
    date_time >= p_first_day and 
    date_time <= (p_first_day::date + interval '1 year' - interval '1 day')::date and 
    id_status = 5);
end;$$;