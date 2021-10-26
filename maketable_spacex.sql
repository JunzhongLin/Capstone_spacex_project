CREATE TABLE `Spacex` (
	`Date_launch` VARCHAR(10) NOT NULL, 
	`Time_launch_UTC` VARCHAR(14) NOT NULL, 
	`Booster_Version` VARCHAR(14) NOT NULL, 
	`Launch_Site` VARCHAR(12) NOT NULL, 
	`Payload` VARCHAR(61) NOT NULL, 
	`PAYLOAD_MASS__KG_` DECIMAL(38, 0) NOT NULL, 
	`Orbit` VARCHAR(11) NOT NULL, 
	`Customer` VARCHAR(57) NOT NULL, 
	`Mission_Outcome` VARCHAR(32) NOT NULL, 
	`Landing _Outcome` VARCHAR(22) NOT NULL
);
