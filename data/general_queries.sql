-- ABOVE /BELOW Ratio
select count(signal) from strat_moving_average  where signal ="Below" and ma ="50" and symbol in (select symbol from data_index_constituints where indx="nasdaq100" );

select count(signal) from strat_moving_average  where signal ="Above" and ma ="50" and symbol in (select symbol from data_index_constituints where indx="sp500" );



-- Check if all symbols are being tracked
select symbol from data_index_constituints dic where dic.indx ="nasdaq100" and dic.symbol not in (select symbol from tradfi_stocks_symbols tss );


-- delete all
delete from data_asset_momentum;