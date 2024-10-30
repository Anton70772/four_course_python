-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: clinika
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `hospitalizations`
--

DROP TABLE IF EXISTS `hospitalizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitalizations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `full_name` varchar(255) NOT NULL,
  `passport_data` varchar(255) NOT NULL,
  `workplace` varchar(255) DEFAULT NULL,
  `insurance_policy_number` varchar(50) DEFAULT NULL,
  `insurance_policy_expiry_date` date DEFAULT NULL,
  `insurance_company` varchar(100) DEFAULT NULL,
  `diagnosis` varchar(255) DEFAULT NULL,
  `hospitalization_code` varchar(50) NOT NULL,
  `hospitalization_date_time` datetime DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `hospitalization_purpose` varchar(255) DEFAULT NULL,
  `hospitalization_conditions` varchar(50) DEFAULT NULL,
  `hospitalization_duration` int DEFAULT NULL,
  `additional_information` text,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `hospitalizations_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitalizations`
--

LOCK TABLES `hospitalizations` WRITE;
/*!40000 ALTER TABLE `hospitalizations` DISABLE KEYS */;
INSERT INTO `hospitalizations` VALUES (5,NULL,'Тест Тестович Тестов','12 32 143421','уа1332ав2','123-143-14143',NULL,'мукмкумум','Задрот','0002','2024-05-16 14:46:00','вамукмук','слил катку','',4,'нету'),(7,NULL,'Тест Тестович Тестов','12 32 143421','уа1332ав2','123-143-14143',NULL,'мукмкумум','Задрот','0002','2024-05-16 01:54:00','вамукмук','слил катку','',7,'нету'),(8,NULL,'Тест Тестович Тестов','12 32 143421','уа1332ав2','123-143-14143',NULL,'мукмкумум','Задрот','0002','2024-05-17 15:56:00','вамукмук','слил катку','',3,'нету'),(10,NULL,'Тест Тестович Тестов','12 32 143421','уа1332ав2','123-143-14143',NULL,'мукмкумум','Задрот','0004','2024-05-30 02:16:00','вамукмук','слил катку','',3,'нету'),(12,NULL,'gtbrtgbtr','23423423',NULL,NULL,NULL,NULL,'fbtebtrb','0005','2049-09-09 00:00:00',NULL,NULL,NULL,NULL,NULL),(13,NULL,'кпмукиму','кимуимуим',NULL,NULL,NULL,NULL,'укпиуекиек','0006','2049-09-09 12:32:00',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `hospitalizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_procedures`
--

DROP TABLE IF EXISTS `medical_procedures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_procedures` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `Procedure_date` datetime DEFAULT NULL,
  `Doctor` varchar(100) DEFAULT NULL,
  `Procedure_type` enum('Computed tomography','Ultrasound diagnostics','Electrocardiography','Physiotherapy') DEFAULT NULL,
  `Procedure_name` varchar(255) DEFAULT NULL,
  `Results` text,
  `Recommendations` text,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `medical_procedures_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_procedures`
--

LOCK TABLES `medical_procedures` WRITE;
/*!40000 ALTER TABLE `medical_procedures` DISABLE KEYS */;
INSERT INTO `medical_procedures` VALUES (1,1,'2024-05-07 00:00:00','Дмитрий','Computed tomography','Antibiotic treatment','Patient responded well to treatment','Не есть фастфуд'),(5,NULL,'2024-05-07 00:00:00','Ярослав','Ultrasound diagnostics','Antibiotic treatment','Patient responded well to treatment','Сидеть меньше за компом'),(6,NULL,'2024-05-17 12:35:00','Ярослав','Electrocardiography','всвувсц','укмумкум','цусуцсц'),(8,NULL,'2024-05-10 20:45:00','Ярослав','Physiotherapy','всвувсц','укмумкум','цусуцсц'),(9,NULL,'2024-05-18 12:00:00','Виктор','Physiotherapy','всвувсц','укмумкум','кмукмук'),(10,NULL,'2024-05-23 12:10:00','','Electrocardiography','ваукмкмуку','',''),(11,2,'2049-07-08 12:30:00','Дмитрий','Computed tomography','кпукпу',NULL,NULL);
/*!40000 ALTER TABLE `medical_procedures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Photo` varchar(255) DEFAULT NULL,
  `First_name` varchar(50) NOT NULL,
  `Last_name` varchar(50) NOT NULL,
  `Patronymic` varchar(50) DEFAULT NULL,
  `work_place` varchar(45) DEFAULT NULL,
  `Passport_number` varchar(20) DEFAULT NULL,
  `Date_of_birth` date DEFAULT NULL,
  `Gender` enum('М','Ж') DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Phone_number` varchar(20) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Medical_card_number` varchar(20) DEFAULT NULL,
  `Date_of_issue` date DEFAULT NULL,
  `Last_visit_date` date DEFAULT NULL,
  `Next_visit_date` date DEFAULT NULL,
  `Insurance_policy_number` varchar(20) DEFAULT NULL,
  `Expiry_date_of_policy` date DEFAULT NULL,
  `Diagnosis` varchar(255) DEFAULT NULL,
  `Medical_history` text,
  `insuranceCompany` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'/ava.png','John','Doe','Smith','Удаленка','1234567890','2005-09-21','М','123 Main St, City, Country','+79801231993','john@yandex.ru','MC001','2020-01-01','2023-01-01','2024-01-01','IP001','2025-01-01','Common cold','No significant medical history','ООО \"ХЗ\"'),(2,'/japan.png','Yarik','Durak','Durakov','Валютная удаленка','1234565890','2008-02-06','М','123 Main St, City, Country','+79891236993','yarik@yandex.ru','MC001','2020-01-01','2023-01-01','2024-01-01','IP001','2025-01-01','Common cold','No significant medical history','ООО \"ХЗ\"'),(3,'/ava.png','Anton','Antonov','Antonovich','На багамах','1284567890','2005-09-21','М','123 Main St, City, Country','+79801246993','anton@yandex.ru','MC001','2020-01-01','2023-01-01','2024-01-01','IP001','2025-01-01','Common cold','No significant medical history','ООО \"ХЗ\"'),(4,'/ava.png','Anton','Antonov',NULL,'Удаленка',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'ООО \"ХЗ\"'),(5,'/ava.png','Anton','Antonov',NULL,'Удаленка',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'ООО \"ХЗ\"'),(6,'/ava.png','Anton','Antonov','Smith','Удаленка',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'IP003',NULL,NULL,NULL,'ООО \"ХЗ\"'),(7,'/japan.png','Антон','Полищук','Александрович','Валютная удаленка',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'131-312-31231',NULL,NULL,NULL,'ООО \"ХЗ\"'),(8,'/japan.png','Антон','Полищук','Александрович','Мальдивы',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'123-123-21312',NULL,NULL,NULL,'ООО \"ХЗ\"'),(9,'/japan.png','Test','Test','Александрович','Удаленка',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'343-245-43524',NULL,NULL,NULL,'ООО \"ХЗ\"'),(10,'/ava.png','Антон','Полищук','Александрович','Мальдивы',NULL,'2024-05-22','М','улаулсуощцс','+79301860642','Poli2005shuk@yandex.ru','10001','2024-05-30','2024-05-12','2024-05-09','123-123-21312','2024-05-16','Задрот','вувусцуцусц','ООО \"ХЗ\"'),(11,'/ava.png','Антон','Полищук','Александрович','Мальдивы',NULL,'2024-05-22','М','улаулсуощцс','+79301860642','Poli2005shuk@yandex.ru','10001','2024-05-30','2024-05-12','2024-05-09','123-123-21312','2024-05-16','Задрот','вувусцуцусц','ООО \"ХЗ\"'),(12,'/japan.png','Антон','Полищук','Александрович','Мальдивы','12 31 231231','2024-05-16','М','улаулсуощцс','+79301860642','Poli2005shuk@yandex.ru','1232143123','2024-05-11','2024-05-03','2024-05-22','131-232-14343','2024-05-31','Задрот','цуавуауцацуууцацсц','ООО \"ХЗ\"'),(13,'/zakat.png','Антон','Полищук','Александрович','Багамы','24 32 411321','2024-05-16','М','улаулсуощцс','+79301860642','Poli2005shuk@yandex.ru','М-004','2024-05-16','2024-05-16','2024-05-17','124-345-31414','2024-05-29','Задрот','уауцпмкмкуаукмсукаму','ООО \"ХЗ\"'),(14,'/zakat.png','Test','Test','Александрович','Валютная удаленка','12 31 231231','2024-05-17','М','уа1332ав2','+79007777777','test@test.ru','0005','2024-05-08','2024-05-18','2024-05-11','123-123-21312','2024-05-17','rgvrverver','erfverververvevevrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr','ООО \"ХЗ\"'),(15,'/ava.png','Test','Test','Александрович','Валютная удаленка','12 31 231231','2024-05-16','М','уа1332ав2','+79007777777','test@test.ru','0006','2024-05-05','2024-05-26','2024-05-03','131-312-31231','2024-05-31','укмкумку','5п53ппу','ООО \"ХЗ\"'),(28,NULL,'fverve','erfverve','erverveve',NULL,'24314141','2012-12-12','М',NULL,'12312431','rg3453g3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Birth` date DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `Role` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Anton','admin',NULL,NULL,NULL,NULL),(2,'vwervv',NULL,'test@test.ru','2024-05-14','М',NULL),(18,'dvvvrvrv','admin4543543','test@test.ru','2024-05-05','М',NULL),(20,'Yarik','wewecwecew','test@test.ru','2024-05-05','М',NULL),(21,'Vlad','wewecwecew','test@test.ru','2024-05-05','М',NULL),(22,'Vlados','admin4543543','test@test.ru','2024-05-19','М',NULL),(23,'Полищук Антон Александрович','anton70772','test@test.ru','2024-05-21','М',NULL),(24,'Иванов Антон Александрович','ivanov7072','test@test.ru','2024-05-24','М',NULL),(25,'vwervv','1213','test@test.ru','2024-05-23','М',NULL),(26,'Кто то','admin123','test@test.ru','2024-07-07','М',NULL),(27,'Тест',NULL,'pol@yandex.ru','2024-05-27','М',NULL),(28,'Тест','admin','pol@yandex.ru','2024-05-22','М',NULL),(29,'Тест','vrach','test1@test.ru','2024-05-10','М',NULL),(30,'абвгд','anton77','test2@test.ru','2024-05-17','М',NULL),(31,'rfwrfrf','admin77','test3@yandex.ru','2024-05-05','М','Admin'),(32,'Anton','admin','test@yandex.ru','2024-05-26','М','Admin'),(33,'Anton2','anton70772','test2@yandex.ru','2024-05-11','М','User'),(34,'Yarik','$2b$10$czwN2lC7qj9eJpv1JLSOOOZnYN/QizvhucnVC6w93oCxVUiWb1POu','yarik@yandex.ru','2024-05-25','М','User'),(35,'Vlados','$2b$10$Og2KAYiq.P6DZsw5jE1NhutIyMlYnZmn.SWY6enIS0mylo89OIUQa','vlad@yandex.ru','2024-05-18','М','User'),(36,'Admin','$2b$10$VyXb/yMadu5WfkSCX5pSDu3wc8qyI2cmtCcph9AhtnLgUuRqIOM2W','admin@yandex.ru','2024-05-26','М','User'),(37,'Vlad','vlad77','vlad@yandex.ru','2024-05-19','М','User'),(38,'chmo','71940ce1ce736ef076505386f7caf58cee4b9c735fd70aa26085fd0aca79ce48','chmo@yandex.ru','2024-10-31','М','Admin'),(39,'Chmo','cbec5c0c5ca0ce191fcf6521dcb2c742aee8cd80e040a7cab781ce18e06649ef','','2024-10-21',NULL,''),(40,'phone','45569da57f4b7bf472d7a864ef4781451cae6383fee9fb0ae40c59aa1ce475b7','','2024-04-04',NULL,'');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-30  7:30:01
