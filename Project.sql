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

create table reviews
(
        rv_reviewkey    INT     NOT NULL,
        rv_realtorkey   INT     NOT NULL,
        rv_name         VARCHAR (25)    NOT NULL,
        rv_rating       FLOAT   NULL,
        rv_comment      VARCHAR (25)    NULL
);


create table manages
(
        m_housekey      INT     NOT NULL,
        m_realtor       INT     NOT NULL
);

create table services
(
        sv_housekey     INT     NOT NULL,
        sv_providerkey  INT     NOT NULL
);
