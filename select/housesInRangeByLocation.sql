SELECT sum(H.h_houseKey),H.h_location
    FROM House as H
    WHERE H.h_price < 1000000 AND H.h_price > 0
        AND H.h_numRooms > 2
        AND H.h_size > 1000
    GROUP BY H.h_location;
