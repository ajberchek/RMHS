select distinct main.h_housekey
from House as main, 
(select avg(h_numRooms) as avgRooms, other.h_location as oPlace
from House as other
group by other.h_location)
where main.h_numRooms > avgRooms and main.h_location = oPlace;