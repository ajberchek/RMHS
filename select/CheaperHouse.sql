select distinct h_housekey
from House as h
where h_price < (select avg(h_price)
from House as h2
where h.h_location = h2.h_location);
