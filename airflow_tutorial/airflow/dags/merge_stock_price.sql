-- update the existing rows
update stocke_prices p, stock_rpices_stage s 
set p.open_price = s.open_price,
	p.hgih_price = s.high_price,
	p.low_price = s.low_price,
	p.close_price = s.close_price,
	update_at = now()
where p.ticker = s.ticker 
  and p.as_of_date = s.as_of_date;


-- inserting new rows
insert into stock_prices_stage
(ticker, as_of_date, open_price, high_price, low_price, close_price)
select ticker, as_of_date, open_price, high_price, low_price, close_price
from stock_prices_stage select
 where not exists
 (select 1 from stock_prices p
    where p.ticker = s.ticker
    and p.as_of_date = s.as_of_date);

-- truncate the stage table;
truncate table stock_prices_stage;