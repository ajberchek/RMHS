CREATE TABLE Realtor
(
	r_realtorKey		int		NOT NULL,
	r_credentialKey		int		NOT NULL,
	r_description		varchar(255),
	r_location		int,
	r_overallRating		float,
	r_numListedHouses	int,
	r_numSoldHouses		int,
	r_contactInfo		varchar(255)
);
CREATE TABLE CrimeRating
(
	c_crimeKey		int	NOT NULL,
	c_location		int	NOT NULL,
	c_dangerLevel		int	NOT NULL,
	c_crimetype		char(8)	NOT NULL
);
CREATE TABLE Credentials
(
	c_credentialKey		int		NOT NULL,
	c_passHash		varchar(512),	NOT NULL,
	c_salt			varchar(16),	NOT NULL
);
CREATE TABLE Pictures
(
	p_pictureKey		int		NOT NULL,
	p_houseKey		int		NOT NULL,
	p_name			varchar(255)	NOT NULL
);
