SELECT H.*,SP.s_name
  FROM House as H,Services as S,ServiceProvider as SP
  WHERE H.h_housekey = S.sv_housekey AND S.sv_providerkey = SP.s_providerkey;
 
