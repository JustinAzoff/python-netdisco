BEGIN TRANSACTION;
CREATE TABLE blacklist_pending (
	p_id INTEGER NOT NULL, 
	ip VARCHAR(15), 
	reason VARCHAR, 
	time VARCHAR, 
	PRIMARY KEY (p_id)
);
CREATE TABLE users (
	username VARCHAR(50) NOT NULL, 
	password VARCHAR, 
	creation TIMESTAMP, 
	last_on TIMESTAMP, 
	port_control BOOLEAN, 
	admin BOOLEAN, 
	fullname VARCHAR, 
	note VARCHAR, 
	PRIMARY KEY (username)
);
CREATE TABLE device (
	ip VARCHAR(15) NOT NULL, 
	creation TIMESTAMP, 
	dns VARCHAR, 
	description VARCHAR, 
	uptime INTEGER, 
	contact VARCHAR, 
	name VARCHAR, 
	location VARCHAR, 
	layers VARCHAR(8), 
	ports INTEGER, 
	mac VARCHAR(20), 
	serial VARCHAR, 
	model VARCHAR, 
	ps1_type VARCHAR, 
	ps2_type VARCHAR, 
	ps1_status VARCHAR, 
	ps2_status VARCHAR, 
	fan VARCHAR, 
	slots INTEGER, 
	vendor VARCHAR, 
	os VARCHAR, 
	os_ver VARCHAR, 
	log VARCHAR, 
	snmp_ver INTEGER, 
	snmp_comm VARCHAR, 
	vtp_domain VARCHAR, 
	last_discover TIMESTAMP, 
	last_macsuck TIMESTAMP, 
	last_arpnip TIMESTAMP, 
	PRIMARY KEY (ip)
);
INSERT INTO "device" VALUES('10.1.2.2',NULL,'foo',NULL,NULL,NULL,'foo switch',NULL,'00000010',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
CREATE TABLE device_port (
	ip VARCHAR(15) NOT NULL, 
	port VARCHAR NOT NULL, 
	creation TIMESTAMP, 
	descr VARCHAR, 
	up VARCHAR, 
	up_admin VARCHAR, 
	type VARCHAR, 
	duplex VARCHAR, 
	duplex_admin VARCHAR, 
	speed VARCHAR, 
	name VARCHAR, 
	mac VARCHAR(20), 
	mtu INTEGER, 
	stp VARCHAR, 
	remote_ip VARCHAR(15), 
	remote_port VARCHAR, 
	remote_type VARCHAR, 
	remote_id VARCHAR, 
	vlan VARCHAR, 
	lastchange INTEGER, 
    pvid integer,
	PRIMARY KEY (ip, port), 
	 FOREIGN KEY(ip) REFERENCES device (ip)
);
INSERT INTO "device_port" VALUES('10.1.2.2','FastEthernet0/1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1);
INSERT INTO "device_port" VALUES('10.1.2.2','FastEthernet0/2',NULL,NULL,NULL,'down',NULL,NULL,NULL,NULL,'VMWare',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1);
CREATE TABLE blacklist (
	b_id INTEGER NOT NULL, 
	ip VARCHAR(15), 
	switch VARCHAR(15), 
	port VARCHAR, 
	reason VARCHAR, 
	time TIMESTAMP, 
	blacklisttime TIMESTAMP, 
	enable BOOLEAN, 
	PRIMARY KEY (b_id), 
	 FOREIGN KEY(switch) REFERENCES device (ip), 
	 FOREIGN KEY(port) REFERENCES device_port (port)
);
CREATE TABLE admin (
	job INTEGER NOT NULL, 
	entered TIMESTAMP, 
	started TIMESTAMP, 
	finished TIMESTAMP, 
	device VARCHAR(15), 
	port VARCHAR, 
	action VARCHAR, 
	subaction VARCHAR, 
	status VARCHAR, 
	username VARCHAR, 
	userip VARCHAR(15), 
	log VARCHAR, 
	debug BOOLEAN, 
	PRIMARY KEY (job), 
	 FOREIGN KEY(device) REFERENCES device (ip), 
	 FOREIGN KEY(username) REFERENCES users (username), 
	 FOREIGN KEY(port) REFERENCES device_port (port)
);
CREATE TABLE device_port_log (
	id INTEGER NOT NULL, 
	ip VARCHAR(15), 
	port VARCHAR, 
	reason VARCHAR, 
	log VARCHAR, 
	username VARCHAR, 
	userip VARCHAR(15), 
	action VARCHAR, 
	creation TIMESTAMP, 
	PRIMARY KEY (id), 
	 FOREIGN KEY(ip) REFERENCES device_port (ip), 
	 FOREIGN KEY(port) REFERENCES device_port (port)
);
CREATE TABLE device_ip (
	ip VARCHAR(15) NOT NULL, 
	alias VARCHAR(15) NOT NULL, 
	port VARCHAR, 
	dns VARCHAR, 
	creation TIMESTAMP, 
	PRIMARY KEY (ip, alias), 
	 FOREIGN KEY(ip) REFERENCES device (ip)
);
CREATE TABLE oui (
	oui VARCHAR(8) NOT NULL, 
	company VARCHAR, 
	PRIMARY KEY (oui)
);
CREATE TABLE node (
	mac VARCHAR(20) NOT NULL, 
	switch VARCHAR(20) NOT NULL, 
	port VARCHAR(20) NOT NULL, 
	active BOOLEAN, 
	oui VARCHAR(8), 
	time_first TIMESTAMP, 
	time_last TIMESTAMP, 
	time_recent TIMESTAMP, 
	PRIMARY KEY (mac, switch, port), 
	 FOREIGN KEY(oui) REFERENCES oui (oui), 
	 FOREIGN KEY(switch) REFERENCES device_port (ip), 
	 FOREIGN KEY(port) REFERENCES device_port (port)
);
INSERT INTO "node" VALUES('00:11:22:33:44:55','10.1.2.2','FastEthernet0/1',NULL,NULL,NULL,'2009-03-26 12:00:00',NULL);
INSERT INTO "node" VALUES('00:11:22:33:44:FF','10.1.2.2','FastEthernet0/2',NULL,NULL,NULL,'2009-03-26 12:00:00',NULL);
CREATE TABLE node_ip (
	mac VARCHAR(20) NOT NULL, 
	ip VARCHAR(20) NOT NULL, 
	active BOOLEAN, 
	time_first TIMESTAMP, 
	time_last TIMESTAMP, 
	PRIMARY KEY (mac, ip), 
	 FOREIGN KEY(mac) REFERENCES node (mac)
);
INSERT INTO "node_ip" VALUES('00:11:22:33:44:55','10.1.2.100',1,NULL,'2009-03-26 12:00:00');
INSERT INTO "node_ip" VALUES('00:11:22:33:44:FF','10.1.2.101',1,NULL,'2009-03-26 12:00:00');
CREATE TABLE node_nbt (
	mac VARCHAR(20) NOT NULL, 
	ip VARCHAR(15), 
	nbname VARCHAR, 
	domain VARCHAR, 
	server BOOLEAN, 
	nbuser VARCHAR, 
	active BOOLEAN, 
	time_first TIMESTAMP, 
	time_last TIMESTAMP, 
	PRIMARY KEY (mac), 
	 FOREIGN KEY(mac) REFERENCES node (mac), 
	 FOREIGN KEY(ip) REFERENCES node_ip (ip)
);
CREATE TABLE device_port_vlan (
    ip inet NOT NULL,
    port text,
    vlan integer,
    native boolean DEFAULT false,
    creation TIMESTAMP,
    last_discover TIMESTAMP
);

COMMIT;
