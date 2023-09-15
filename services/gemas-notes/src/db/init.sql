CREATE USER `gemasnotesuser`@`%` IDENTIFIED WITH mysql_native_password BY 'hAP[Vl1~4<?7@Sf1Xd';

USE `gemasnotes`;

DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(150) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO User(email,username,password) VALUES ('checker@gemasnotes.id','checker','a6005967f8e6e0ee346804765900f41f');

DROP TABLE IF EXISTS `Notes`;
CREATE TABLE `Notes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `content` longtext,
  `author` int(11) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user` (`author`),
  CONSTRAINT `fk_user` FOREIGN KEY (`author`) REFERENCES `User` (`id`)
);

DROP TABLE IF EXISTS `rewards`;
CREATE TABLE `rewards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fl4gg` varchar(60),
  PRIMARY KEY (`id`)
);

INSERT INTO rewards(fl4gg) VALUES ('GEMASTIK{e54e6f6ba0c7cbb4eb7a2016e2f17842}');

GRANT SELECT,INSERT,UPDATE,DELETE ON `User` TO `gemasnotesuser`@`%`;
GRANT SELECT,INSERT,UPDATE,DELETE ON `Notes` TO `gemasnotesuser`@`%`;
GRANT SELECT ON `rewards` TO `gemasnotesuser`@`%`;
FLUSH PRIVILEGES;