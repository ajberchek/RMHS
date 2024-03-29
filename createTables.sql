CREATE TABLE Realtor
(
	r_realtorKey		INT		NOT NULL,
	r_credentialKey		INT		NOT NULL,
	r_description		VARCHAR(255),
	r_location		INT,
	r_overallRating		float,
	r_numListedHouses	INT,
	r_numSoldHouses		INT,
	r_contactInfo		VARCHAR(255)
);
CREATE TABLE CrimeRating
(
	c_crimeKey		INT	NOT NULL,
	c_location		INT	NOT NULL,
	c_dangerLevel		INT	NOT NULL,
	c_crimetype		char(8)	NOT NULL
);
CREATE TABLE Credentials
(
	c_credentialKey		VARCHAR (25)	NOT NULL,
	c_passHash		VARCHAR(512),	NOT NULL,
	c_salt			VARCHAR(16),	NOT NULL
);
CREATE TABLE Pictures
(
	p_pictureKey		INT		NOT NULL,
	p_houseKey		INT		NOT NULL,
	p_name			VARCHAR(255)	NOT NULL
);
create table House
(
        h_housekey      INT   NOT NULL,
        h_constructionyear      DATE    NOT NULL,
        h_petFriendly   VARCHAR (10)    NOT NULL,
        h_numRooms      INT  NOT NULL,
        h_numBath       INT  NOT NULL,
        h_size          INT  NOT NULL,
        h_appliances    VARCHAR (25)    NOT NULL,
        h_sellStatus    VARCHAR (25)    NOT NULL,
        h_price         INT  NOT NULL,
        h_garage        VARCHAR (10)    NOT NULL,
        h_description   VARCHAR (25)    NOT NULL,
        h_additionlInfo VARCHAR (25)    NOT NULL,
        h_address       VARCHAR (25)    NOT NULL,
        h_location      INT  NOT NULL
);
create table ServiceProvider
(
        s_providerKey   INT  NOT NULL,
        s_name          VARCHAR (25)    NOT NULL,
        s_serviceType   VARCHAR (25)    NOT NULL,
        s_location      INT  NOT NULL,
        s_contactInfo   VARCHAR (25)    NOT NULL
);
create table Reviews
(
        rv_reviewkey    INT     NOT NULL,
        rv_realtorkey   INT     NOT NULL,
        rv_name         VARCHAR (25)    NOT NULL,
        rv_rating       FLOAT   NULL,
        rv_comment      VARCHAR (25)    NULL
);
create table Manages
(
        m_housekey      INT     NOT NULL,
        m_realtor       INT     NOT NULL
);
create table Services
(
        sv_housekey     INT     NOT NULL,
        sv_providerkey  INT     NOT NULL
);
