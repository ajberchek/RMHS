SELECT P.p_name
FROM Pictures as P,House as H
WHERE H.h_houseKey = P.p_houseKey
        AND H.h_address = "123 Freedom Lane";
