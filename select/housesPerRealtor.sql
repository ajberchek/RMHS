SELECT H.*,R.r_realtorKey
FROM House as H,Realtor as R,Manages as M
WHERE H.h_housekey = M.m_housekey AND M.m_realtor = R.r_realtorKey
GROUP BY R.r_realtorKey
