-- ABOVE /BELOW Ratio
select count(signal) from strat_moving_average  where signal ="Below" and ma ="50" and symbol in (select symbol from data_index_constituints where indx="coindex21" );

select count(signal) from strat_moving_average  where signal ="Above" and ma ="50" and symbol in (select symbol from data_index_constituints where indx="coindex21" );



-- Check if all symbols are being tracked
select symbol from data_index_constituints dic where dic.indx ="nasdaq100" and dic.symbol not in (select symbol from tradfi_stocks_symbols tss );


-- delete all
delete from data_asset_momentum;

-- market breath
select * from data_market_breath dmb  where dmb.period ="50" and dmb.indx ="sp500";