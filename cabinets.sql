-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: cabinets
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `meter_data`
--

DROP TABLE IF EXISTS `meter_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meter_data` (
  `id` int NOT NULL,
  `meter_model` varchar(255) NOT NULL,
  `voltage_value` float DEFAULT NULL,
  `power_value` float DEFAULT NULL,
  `current_value` float DEFAULT NULL,
  `pt1` int DEFAULT NULL,
  `pt2` int DEFAULT NULL,
  `ct1` int DEFAULT NULL,
  `ct2` int DEFAULT NULL,
  `time_step` datetime NOT NULL,
  `count` bigint NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`count`)
) ENGINE=InnoDB AUTO_INCREMENT=401 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meter_data`
--

LOCK TABLES `meter_data` WRITE;
/*!40000 ALTER TABLE `meter_data` DISABLE KEYS */;
INSERT INTO `meter_data` VALUES (1,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:30:08',1),(2,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:30:09',2),(3,'PM800',233.25,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:10',3),(4,'PM800',233.143,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:11',4),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:30:12',5),(5,'PAC4200',233.401,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:12',6),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:30:13',7),(6,'PAC4200',233.225,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:13',8),(3,'PM800',232.981,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:14',9),(4,'PM800',233.008,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:15',10),(5,'PAC4200',233.413,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:16',11),(6,'PAC4200',233.33,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:17',12),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:30:18',13),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:30:19',14),(3,'PM800',233.13,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:20',15),(4,'PM800',233.148,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:21',16),(5,'PAC4200',233.444,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:22',17),(6,'PAC4200',233.28,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:23',18),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:30:24',19),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:30:25',20),(3,'PM800',233.057,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:26',21),(4,'PM800',233.023,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:27',22),(5,'PAC4200',233.402,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:28',23),(6,'PAC4200',233.224,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:29',24),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:30:30',25),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:30:31',26),(3,'PM800',233.051,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:32',27),(4,'PM800',233.12,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:33',28),(5,'PAC4200',233.41,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:34',29),(6,'PAC4200',233.214,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:35',30),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:30:36',31),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:30:37',32),(3,'PM800',233.176,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:38',33),(4,'PM800',233.148,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:39',34),(5,'PAC4200',233.572,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:40',35),(6,'PAC4200',233.363,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:41',36),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:30:42',37),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:30:43',38),(3,'PM800',233.212,43.0058,0.139676,NULL,NULL,NULL,NULL,'2023-09-20 11:30:44',39),(4,'PM800',233.241,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:45',40),(5,'PAC4200',233.466,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:46',41),(6,'PAC4200',233.313,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:47',42),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:30:48',43),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:30:49',44),(3,'PM800',233.154,45.4957,0.147002,NULL,NULL,NULL,NULL,'2023-09-20 11:30:50',45),(4,'PM800',233.292,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:51',46),(5,'PAC4200',233.796,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:52',47),(6,'PAC4200',233.565,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:53',48),(1,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:30:54',49),(2,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:30:55',50),(3,'PM800',233.251,45.0174,0.160365,NULL,NULL,NULL,NULL,'2023-09-20 11:30:56',51),(4,'PM800',233.168,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:57',52),(5,'PAC4200',233.477,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:58',53),(6,'PAC4200',233.33,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:30:59',54),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:31:00',55),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:31:01',56),(3,'PM800',233.192,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:02',57),(4,'PM800',233.276,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:03',58),(5,'PAC4200',233.593,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:04',59),(6,'PAC4200',233.323,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:05',60),(1,'EPM5500P',233.1,20,0.1,220,220,25,5,'2023-09-20 11:31:06',61),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:31:07',62),(3,'PM800',233.257,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:08',63),(4,'PM800',233.319,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:09',64),(5,'PAC4200',233.514,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:10',65),(6,'PAC4200',233.349,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:11',66),(1,'EPM5500P',233.1,20,0.1,220,220,25,5,'2023-09-20 11:31:12',67),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:31:13',68),(3,'PM800',233.216,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:14',69),(4,'PM800',233.271,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:15',70),(5,'PAC4200',233.636,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:16',71),(6,'PAC4200',233.412,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:17',72),(1,'EPM5500P',233.1,25,0.125,220,220,25,5,'2023-09-20 11:31:18',73),(2,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:31:19',74),(3,'PM800',233.288,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:20',75),(4,'PM800',233.276,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:21',76),(5,'PAC4200',233.654,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:22',77),(6,'PAC4200',233.417,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:23',78),(1,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:31:24',79),(2,'EPM5500P',233.5,15,0.07,220,220,25,5,'2023-09-20 11:31:25',80),(3,'PM800',233.255,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:26',81),(4,'PM800',233.303,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:27',82),(5,'PAC4200',233.702,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:28',83),(6,'PAC4200',233.43,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:29',84),(1,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:31:30',85),(2,'EPM5500P',233.4,20,0.1,220,220,25,5,'2023-09-20 11:31:31',86),(3,'PM800',233.17,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:32',87),(4,'PM800',233.192,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:33',88),(5,'PAC4200',233.375,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:34',89),(6,'PAC4200',233.187,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:35',90),(1,'EPM5500P',232.9,0,0,220,220,25,5,'2023-09-20 11:31:36',91),(2,'EPM5500P',233.2,20,0.105,220,220,25,5,'2023-09-20 11:31:37',92),(3,'PM800',232.853,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:38',93),(4,'PM800',232.899,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:39',94),(5,'PAC4200',233.392,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:40',95),(6,'PAC4200',233.148,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:41',96),(1,'EPM5500P',232.8,0,0,220,220,25,5,'2023-09-20 11:31:42',97),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:31:43',98),(3,'PM800',233.292,39.3827,0.102333,NULL,NULL,NULL,NULL,'2023-09-20 11:31:44',99),(4,'PM800',233.478,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:45',100),(5,'PAC4200',233.712,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:46',101),(6,'PAC4200',233.516,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:47',102),(1,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:31:48',103),(2,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:31:49',104),(3,'PM800',233.295,42.8156,0.131193,NULL,NULL,NULL,NULL,'2023-09-20 11:31:50',105),(4,'PM800',233.391,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:51',106),(5,'PAC4200',233.679,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:52',107),(6,'PAC4200',233.509,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:53',108),(1,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:31:54',109),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:31:55',110),(3,'PM800',233.255,39.9356,0.109399,NULL,NULL,NULL,NULL,'2023-09-20 11:31:56',111),(4,'PM800',233.236,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:57',112),(5,'PAC4200',233.514,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:58',113),(6,'PAC4200',233.32,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:31:59',114),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:32:00',115),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:32:01',116),(3,'PM800',233.113,39.9054,0.107595,NULL,NULL,NULL,NULL,'2023-09-20 11:32:02',117),(4,'PM800',233.118,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:03',118),(5,'PAC4200',233.521,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:04',119),(6,'PAC4200',233.254,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:05',120),(1,'EPM5500P',232.9,0,0,220,220,25,5,'2023-09-20 11:32:06',121),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:32:07',122),(3,'PM800',233.016,40.0419,0.104635,NULL,NULL,NULL,NULL,'2023-09-20 11:32:08',123),(4,'PM800',233.017,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:09',124),(5,'PAC4200',233.435,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:10',125),(6,'PAC4200',233.268,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:11',126),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:32:12',127),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:32:13',128),(3,'PM800',233.211,38.8134,0.106336,NULL,NULL,NULL,NULL,'2023-09-20 11:32:14',129),(4,'PM800',233.211,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:15',130),(5,'PAC4200',233.525,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:16',131),(6,'PAC4200',233.374,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:17',132),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:32:18',133),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:32:19',134),(3,'PM800',233.199,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:20',135),(4,'PM800',233.172,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:21',136),(5,'PAC4200',233.521,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:22',137),(6,'PAC4200',233.367,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:23',138),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:32:24',139),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:32:25',140),(3,'PM800',233.179,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:26',141),(4,'PM800',233.21,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:27',142),(5,'PAC4200',233.48,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:28',143),(6,'PAC4200',233.288,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:29',144),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:32:30',145),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:32:31',146),(3,'PM800',233.14,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:32',147),(4,'PM800',233.141,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:33',148),(5,'PAC4200',233.489,23.4453,0.100413,NULL,NULL,NULL,NULL,'2023-09-20 11:32:34',149),(6,'PAC4200',233.191,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:35',150),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:32:36',151),(2,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:32:37',152),(3,'PM800',232.94,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:38',153),(4,'PM800',232.885,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:39',154),(5,'PAC4200',233.018,35.4021,0.151929,NULL,NULL,NULL,NULL,'2023-09-20 11:32:40',155),(6,'PAC4200',232.899,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:41',156),(1,'EPM5500P',232.6,0,0,220,220,25,5,'2023-09-20 11:32:42',157),(2,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:32:43',158),(3,'PM800',232.864,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:44',159),(4,'PM800',232.902,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:45',160),(5,'PAC4200',233.259,44.116,0.189129,NULL,NULL,NULL,NULL,'2023-09-20 11:32:46',161),(6,'PAC4200',233.073,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:47',162),(1,'EPM5500P',232.8,0,0,220,220,25,5,'2023-09-20 11:32:48',163),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:32:49',164),(3,'PM800',232.955,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:50',165),(4,'PM800',232.945,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:51',166),(5,'PAC4200',233.203,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:52',167),(6,'PAC4200',232.947,2.0172,0.00865946,NULL,NULL,NULL,NULL,'2023-09-20 11:32:53',168),(1,'EPM5500P',232.8,0,0,220,220,25,5,'2023-09-20 11:32:54',169),(2,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:32:55',170),(3,'PM800',232.807,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:56',171),(4,'PM800',232.893,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:57',172),(5,'PAC4200',233.289,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:32:58',173),(6,'PAC4200',233.131,25.7114,0.110288,NULL,NULL,NULL,NULL,'2023-09-20 11:32:59',174),(1,'EPM5500P',232.9,0,0,220,220,25,5,'2023-09-20 11:33:00',175),(2,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:33:01',176),(3,'PM800',232.889,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:02',177),(4,'PM800',232.95,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:03',178),(5,'PAC4200',233.458,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:04',179),(6,'PAC4200',233.301,36.4777,0.156354,NULL,NULL,NULL,NULL,'2023-09-20 11:33:05',180),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:33:06',181),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:33:07',182),(3,'PM800',233.166,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:08',183),(4,'PM800',233.203,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:09',184),(5,'PAC4200',233.618,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:10',185),(6,'PAC4200',233.292,54.1398,0.232069,NULL,NULL,NULL,NULL,'2023-09-20 11:33:11',186),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:33:12',187),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:33:13',188),(3,'PM800',233.074,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:14',189),(4,'PM800',233.162,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:15',190),(5,'PAC4200',233.389,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:16',191),(6,'PAC4200',233.224,65.1793,0.27947,NULL,NULL,NULL,NULL,'2023-09-20 11:33:17',192),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:33:18',193),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:33:19',194),(3,'PM800',233.017,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:20',195),(4,'PM800',233.068,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:21',196),(5,'PAC4200',233.243,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:22',197),(6,'PAC4200',233.019,68.1939,0.292654,NULL,NULL,NULL,NULL,'2023-09-20 11:33:23',198),(1,'EPM5500P',232.9,0,0,220,220,25,5,'2023-09-20 11:33:24',199),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:33:25',200),(3,'PM800',233.072,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:26',201),(4,'PM800',233.107,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:27',202),(5,'PAC4200',233.568,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:28',203),(6,'PAC4200',233.385,67.2638,0.288209,NULL,NULL,NULL,NULL,'2023-09-20 11:33:29',204),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:33:30',205),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:33:31',206),(3,'PM800',233.085,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:32',207),(4,'PM800',233.033,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:33',208),(5,'PAC4200',233.394,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:34',209),(6,'PAC4200',233.16,66.2647,0.284203,NULL,NULL,NULL,NULL,'2023-09-20 11:33:35',210),(1,'EPM5500P',232.9,0,0,220,220,25,5,'2023-09-20 11:33:36',211),(2,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:33:37',212),(3,'PM800',232.954,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:38',213),(4,'PM800',233.022,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:39',214),(5,'PAC4200',233.4,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:40',215),(6,'PAC4200',233.184,65.9479,0.282816,NULL,NULL,NULL,NULL,'2023-09-20 11:33:41',216),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:33:42',217),(2,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:33:43',218),(3,'PM800',233.062,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:44',219),(4,'PM800',233.116,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:45',220),(5,'PAC4200',233.506,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:46',221),(6,'PAC4200',233.335,65.4283,0.280405,NULL,NULL,NULL,NULL,'2023-09-20 11:33:47',222),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:33:48',223),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:33:49',224),(3,'PM800',233.197,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:50',225),(4,'PM800',233.221,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:51',226),(5,'PAC4200',233.556,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:52',227),(6,'PAC4200',233.225,64.8537,0.278074,NULL,NULL,NULL,NULL,'2023-09-20 11:33:53',228),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:33:54',229),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:33:55',230),(3,'PM800',233.091,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:56',231),(4,'PM800',233.131,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:57',232),(5,'PAC4200',233.375,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:33:58',233),(6,'PAC4200',233.209,64.7035,0.277448,NULL,NULL,NULL,NULL,'2023-09-20 11:33:59',234),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:34:00',235),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:34:01',236),(3,'PM800',233.025,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:02',237),(4,'PM800',233.048,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:03',238),(5,'PAC4200',233.329,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:05',239),(6,'PAC4200',233.263,65.7118,0.281707,NULL,NULL,NULL,NULL,'2023-09-20 11:34:06',240),(1,'EPM5500P',232.9,0,0,220,220,25,5,'2023-09-20 11:34:07',241),(2,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:34:09',242),(3,'PM800',232.956,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:11',243),(4,'PM800',232.893,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:12',244),(5,'PAC4200',233.385,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:14',245),(1,'EPM5500P',232.9,0,0,220,220,25,5,'2023-09-20 11:34:14',246),(6,'PAC4200',233.299,65.9006,0.282473,NULL,NULL,NULL,NULL,'2023-09-20 11:34:16',247),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:34:16',248),(3,'PM800',233.138,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:18',249),(4,'PM800',233.127,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:20',250),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:34:20',251),(5,'PAC4200',233.583,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:22',252),(2,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:34:22',253),(6,'PAC4200',233.411,64.5384,0.276501,NULL,NULL,NULL,NULL,'2023-09-20 11:34:24',254),(3,'PM800',233.211,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:24',255),(4,'PM800',233.24,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:26',256),(1,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:34:26',257),(5,'PAC4200',233.648,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:28',258),(2,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:34:28',259),(6,'PAC4200',233.559,65.1265,0.278844,NULL,NULL,NULL,NULL,'2023-09-20 11:34:30',260),(3,'PM800',233.335,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:30',261),(4,'PM800',233.344,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:32',262),(1,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:34:32',263),(5,'PAC4200',233.779,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:34',264),(2,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:34:34',265),(6,'PAC4200',233.559,66.2669,0.283727,NULL,NULL,NULL,NULL,'2023-09-20 11:34:36',266),(3,'PM800',233.379,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:36',267),(4,'PM800',233.316,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:38',268),(1,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:34:38',269),(5,'PAC4200',233.725,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:40',270),(2,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:34:40',271),(3,'PM800',233.406,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:42',272),(6,'PAC4200',233.627,67.2961,0.288049,NULL,NULL,NULL,NULL,'2023-09-20 11:34:42',273),(4,'PM800',233.615,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:44',274),(1,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:34:44',275),(5,'PAC4200',233.986,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:46',276),(2,'EPM5500P',233.8,0,0,220,220,25,5,'2023-09-20 11:34:46',277),(6,'PAC4200',233.764,64.2757,0.274959,NULL,NULL,NULL,NULL,'2023-09-20 11:34:48',278),(3,'PM800',233.591,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:48',279),(4,'PM800',233.525,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:50',280),(1,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:34:50',281),(5,'PAC4200',233.867,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:52',282),(2,'EPM5500P',233.7,0,0,220,220,25,5,'2023-09-20 11:34:52',283),(3,'PM800',233.482,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:54',284),(6,'PAC4200',233.613,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:54',285),(4,'PM800',233.431,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:56',286),(1,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:34:56',287),(5,'PAC4200',233.737,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:34:58',288),(2,'EPM5500P',233.7,0,0,220,220,25,5,'2023-09-20 11:34:58',289),(6,'PAC4200',233.51,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:00',290),(3,'PM800',233.33,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:00',291),(1,'EPM5500P',233,0,0,220,220,25,5,'2023-09-20 11:35:22',292),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:35:23',293),(3,'PM800',233.129,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:24',294),(4,'PM800',233.196,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:25',295),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:35:26',296),(5,'PAC4200',233.443,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:26',297),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:35:27',298),(6,'PAC4200',233.33,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:27',299),(3,'PM800',233.098,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:28',300),(4,'PM800',233.138,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:29',301),(5,'PAC4200',233.521,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:30',302),(6,'PAC4200',233.361,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:31',303),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:35:32',304),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:35:33',305),(3,'PM800',233.182,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:34',306),(4,'PM800',233.208,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:35',307),(5,'PAC4200',233.65,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:36',308),(6,'PAC4200',233.424,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:37',309),(1,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:35:38',310),(2,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:35:39',311),(3,'PM800',233.367,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:40',312),(4,'PM800',233.487,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:41',313),(5,'PAC4200',233.775,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:42',314),(6,'PAC4200',233.595,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:43',315),(1,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:35:44',316),(2,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:35:45',317),(3,'PM800',233.418,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:46',318),(4,'PM800',233.377,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:47',319),(5,'PAC4200',233.613,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:48',320),(6,'PAC4200',233.493,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:49',321),(1,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:35:50',322),(2,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:35:51',323),(3,'PM800',233.32,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:52',324),(4,'PM800',233.352,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:53',325),(5,'PAC4200',233.742,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:54',326),(6,'PAC4200',233.486,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:55',327),(1,'EPM5500P',233.2,0,0,220,220,25,5,'2023-09-20 11:35:56',328),(2,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:35:57',329),(3,'PM800',233.195,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:58',330),(4,'PM800',233.151,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:35:59',331),(5,'PAC4200',233.4,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:00',332),(6,'PAC4200',233.224,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:01',333),(1,'EPM5500P',233.1,0,0,220,220,25,5,'2023-09-20 11:36:02',334),(2,'EPM5500P',233.3,0,0,220,220,25,5,'2023-09-20 11:36:03',335),(3,'PM800',233.163,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:04',336),(4,'PM800',233.306,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:05',337),(5,'PAC4200',234.044,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:06',338),(6,'PAC4200',233.827,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:07',339),(1,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:36:08',340),(2,'EPM5500P',233.9,0,0,220,220,25,5,'2023-09-20 11:36:09',341),(3,'PM800',233.709,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:10',342),(4,'PM800',233.682,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:11',343),(5,'PAC4200',234.075,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:12',344),(6,'PAC4200',233.826,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:13',345),(1,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:36:14',346),(2,'EPM5500P',233.8,0,0,220,220,25,5,'2023-09-20 11:36:15',347),(3,'PM800',233.597,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:16',348),(4,'PM800',233.638,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:17',349),(5,'PAC4200',233.852,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:18',350),(6,'PAC4200',233.77,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:19',351),(1,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:36:20',352),(2,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:36:21',353),(3,'PM800',233.512,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:22',354),(4,'PM800',233.581,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:23',355),(5,'PAC4200',233.919,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:24',356),(6,'PAC4200',233.805,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:25',357),(1,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:36:26',358),(2,'EPM5500P',234.1,0,0,220,220,25,5,'2023-09-20 11:36:27',359),(3,'PM800',233.622,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:28',360),(4,'PM800',233.768,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:29',361),(5,'PAC4200',234.139,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:30',362),(6,'PAC4200',233.943,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:31',363),(1,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:36:32',364),(2,'EPM5500P',233.9,0,0,220,220,25,5,'2023-09-20 11:36:33',365),(3,'PM800',233.692,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:34',366),(4,'PM800',233.795,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:35',367),(5,'PAC4200',234.025,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:36',368),(6,'PAC4200',233.818,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:37',369),(1,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:36:38',370),(2,'EPM5500P',233.8,0,0,220,220,25,5,'2023-09-20 11:36:39',371),(3,'PM800',233.623,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:40',372),(4,'PM800',233.664,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:41',373),(5,'PAC4200',234.037,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:42',374),(6,'PAC4200',233.793,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:43',375),(1,'EPM5500P',233.5,0,0,220,220,25,5,'2023-09-20 11:36:44',376),(2,'EPM5500P',233.8,0,0,220,220,25,5,'2023-09-20 11:36:45',377),(3,'PM800',233.593,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:46',378),(4,'PM800',233.534,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:47',379),(5,'PAC4200',233.823,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:48',380),(6,'PAC4200',233.602,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:49',381),(1,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:36:50',382),(2,'EPM5500P',233.7,0,0,220,220,25,5,'2023-09-20 11:36:51',383),(3,'PM800',233.456,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:52',384),(4,'PM800',233.501,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:53',385),(5,'PAC4200',233.848,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:54',386),(6,'PAC4200',233.667,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:55',387),(1,'EPM5500P',233.4,0,0,220,220,25,5,'2023-09-20 11:36:56',388),(2,'EPM5500P',233.7,0,0,220,220,25,5,'2023-09-20 11:36:57',389),(3,'PM800',233.519,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:58',390),(4,'PM800',233.526,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:36:59',391),(5,'PAC4200',233.95,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:37:00',392),(6,'PAC4200',233.782,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:37:01',393),(1,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:37:02',394),(2,'EPM5500P',233.8,0,0,220,220,25,5,'2023-09-20 11:37:03',395),(3,'PM800',233.532,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:37:04',396),(4,'PM800',233.629,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:37:05',397),(5,'PAC4200',234.036,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:37:06',398),(6,'PAC4200',233.831,0,0,NULL,NULL,NULL,NULL,'2023-09-20 11:37:07',399),(1,'EPM5500P',233.6,0,0,220,220,25,5,'2023-09-20 11:37:08',400);
/*!40000 ALTER TABLE `meter_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-20 19:43:18
