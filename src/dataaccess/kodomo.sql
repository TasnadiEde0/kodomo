-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: kodomo
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `imageId` int NOT NULL AUTO_INCREMENT,
  `userId` int DEFAULT NULL,
  `imagePath` varchar(255) DEFAULT NULL,
  `probability` float DEFAULT '0',
  `record_time` date DEFAULT NULL,
  `isDeleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`imageId`),
  KEY `userId` (`userId`),
  CONSTRAINT `fk_image_user` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES (2,33,'/static/images/2e782ce3-8419-4ed1-87c5-6d4dbd52b26b.jpg',0.308748,'2025-01-07',0),(3,33,'/static/images/e4724673-3cec-4259-846a-1eb4a3338464.jpg',0.879186,'2024-12-29',0),(4,33,'/static/images/3eb14a1b-8187-4ed0-ab80-a0154c927ea1.jpg',0.0748691,'2024-10-21',0),(5,34,'/static/images/3d79c32f-d419-4b9c-9c78-a1b7ea58204b.jpg',0.0849899,'2024-12-20',0),(6,34,'/static/images/44a550a0-4736-487a-bde0-8d30e19525fc.jpg',0.646836,'2025-01-20',0),(7,35,'/static/images/758f6dbd-ce55-4a1c-a2af-2572e5dd8e52.jpg',0.0674792,'2025-01-17',0),(8,36,'/static/images/3da76b05-5d9d-4164-a944-00373af56577.jpg',0.896846,'2024-04-23',0),(9,36,'/static/images/22d90e87-f859-41ea-b7a3-4d17f99e5e75.jpg',0.168469,'2025-03-08',0),(10,37,'/static/images/719cb57a-bf66-47ca-8059-55a86bab41a7.jpg',0.956514,'2024-12-02',0),(11,37,'/static/images/e8c55bef-d9e7-404c-9988-d756a673816d.jpg',0.0989641,'2024-12-14',0),(12,37,'/static/images/90a6538e-dbaf-4d75-9de2-d8ef88882e46.jpg',0.629685,'2024-12-25',0);
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `intervals`
--

DROP TABLE IF EXISTS `intervals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intervals` (
  `intervalId` int NOT NULL AUTO_INCREMENT,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `userId` int NOT NULL,
  PRIMARY KEY (`intervalId`),
  KEY `fk_intervals_users` (`userId`),
  CONSTRAINT `fk_intervals_users` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intervals`
--

LOCK TABLES `intervals` WRITE;
/*!40000 ALTER TABLE `intervals` DISABLE KEYS */;
INSERT INTO `intervals` VALUES (13,'2024-03-09','2024-03-14',33),(14,'2024-04-06','2024-04-11',33),(15,'2024-05-04','2024-05-09',33),(16,'2024-06-01','2024-06-06',33),(17,'2024-06-29','2024-07-04',33),(18,'2024-07-27','2024-08-01',33),(19,'2024-08-24','2024-08-29',33),(20,'2024-09-21','2024-09-26',33),(21,'2024-10-19','2024-10-24',33),(22,'2024-11-16','2024-11-21',33),(23,'2024-12-14','2024-12-19',33),(24,'2025-01-11','2025-01-16',33),(25,'2023-05-06','2023-05-11',34),(26,'2023-07-01','2023-07-06',34),(27,'2023-08-26','2023-08-31',34),(28,'2023-10-21','2023-10-26',34),(29,'2023-12-16','2023-12-21',34),(30,'2024-02-10','2024-02-15',34),(31,'2024-04-06','2024-04-11',34),(32,'2024-06-01','2024-06-06',34),(33,'2024-07-27','2024-08-01',34),(34,'2024-09-21','2024-09-26',34),(35,'2024-11-16','2024-11-21',34),(36,'2025-01-11','2025-01-16',34),(37,'2022-05-08','2022-05-13',35),(38,'2022-06-05','2022-06-10',35),(39,'2022-07-03','2022-07-08',35),(40,'2022-07-31','2022-08-05',35),(41,'2022-08-28','2022-09-02',35),(42,'2022-09-25','2022-09-30',35),(43,'2022-10-23','2022-10-28',35),(44,'2022-11-20','2022-11-25',35),(45,'2022-12-18','2022-12-23',35),(46,'2023-01-15','2023-01-20',35),(47,'2023-02-12','2023-02-17',35),(48,'2023-03-12','2023-03-17',35),(49,'2023-04-09','2023-04-14',35),(50,'2023-05-07','2023-05-12',35),(51,'2023-06-04','2023-06-09',35),(52,'2023-07-02','2023-07-07',35),(53,'2023-07-30','2023-08-04',35),(54,'2023-08-27','2023-09-01',35),(55,'2023-09-24','2023-09-29',35),(56,'2023-10-22','2023-10-27',35),(57,'2023-11-19','2023-11-24',35),(58,'2023-12-17','2023-12-22',35),(59,'2024-01-14','2024-01-19',35),(60,'2024-02-11','2024-02-16',35),(61,'2024-03-10','2024-03-15',35),(62,'2024-04-07','2024-04-12',35),(63,'2024-05-05','2024-05-10',35),(64,'2024-06-02','2024-06-07',35),(65,'2024-06-30','2024-07-05',35),(66,'2024-07-28','2024-08-02',35),(67,'2024-08-25','2024-08-30',35),(68,'2024-09-22','2024-09-27',35),(69,'2024-10-20','2024-10-25',35),(70,'2024-11-17','2024-11-22',35),(71,'2024-12-15','2024-12-20',35),(72,'2025-01-12','2025-01-17',35),(73,'2024-06-02','2024-06-07',36),(74,'2024-07-28','2024-08-02',36),(75,'2024-09-22','2024-09-27',36),(76,'2024-11-17','2024-11-22',36),(77,'2025-01-12','2025-01-17',36),(78,'2024-11-17','2024-11-22',37),(79,'2024-12-15','2024-12-20',37),(80,'2025-01-12','2025-01-17',37);
/*!40000 ALTER TABLE `intervals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `userTypeId` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL DEFAULT '',
  `last_name` varchar(50) NOT NULL DEFAULT '',
  `birth_date` datetime(6) DEFAULT NULL,
  `address` varchar(120) NOT NULL DEFAULT '',
  `post_code` varchar(25) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userId`),
  KEY `username` (`username`),
  KEY `fk_users_userTypes` (`userTypeId`),
  CONSTRAINT `fk_users_userTypes` FOREIGN KEY (`userTypeId`) REFERENCES `usertypes` (`userTypeId`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (32,1,'admin','$2b$12$GTrppD9c0uDGgC84TucTa.XSgghZE9ISnZj9zSiBHhFlpRnSxk68.','','','2000-01-01 00:00:00.000000','',NULL,'admin@email.com'),(33,2,'Emma Hill','$2b$12$GTrppD9c0uDGgC84TucTa.XSgghZE9ISnZj9zSiBHhFlpRnSxk68.','','','2000-01-01 00:00:00.000000','',NULL,'EmmaHill@email.com'),(34,2,'Anna Clark','$2b$12$GTrppD9c0uDGgC84TucTa.XSgghZE9ISnZj9zSiBHhFlpRnSxk68.','','','2000-01-01 00:00:00.000000','',NULL,'AnnaClark@email.com'),(35,2,'Ella Brown','$2b$12$GTrppD9c0uDGgC84TucTa.XSgghZE9ISnZj9zSiBHhFlpRnSxk68.','','','2000-01-01 00:00:00.000000','',NULL,'EllaBrown@email.com'),(36,2,'Lucy Davis','$2b$12$GTrppD9c0uDGgC84TucTa.XSgghZE9ISnZj9zSiBHhFlpRnSxk68.','','','2000-01-01 00:00:00.000000','',NULL,'LucyDavis@email.com'),(37,2,'Kate Miller','$2b$12$GTrppD9c0uDGgC84TucTa.XSgghZE9ISnZj9zSiBHhFlpRnSxk68.','','','2000-01-01 00:00:00.000000','',NULL,'KateMiller@email.com');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usertypes`
--

DROP TABLE IF EXISTS `usertypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usertypes` (
  `userTypeId` int NOT NULL AUTO_INCREMENT,
  `userTypeName` varchar(50) NOT NULL,
  PRIMARY KEY (`userTypeId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usertypes`
--

LOCK TABLES `usertypes` WRITE;
/*!40000 ALTER TABLE `usertypes` DISABLE KEYS */;
INSERT INTO `usertypes` VALUES (1,'Admin'),(2,'Regular');
/*!40000 ALTER TABLE `usertypes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-17 14:24:49
