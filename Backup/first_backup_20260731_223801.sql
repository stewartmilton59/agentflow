/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.3.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: agentflow
-- ------------------------------------------------------
-- Server version	12.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `accounts_loginattempt`
--

DROP TABLE IF EXISTS `accounts_loginattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_loginattempt` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `ip_address` char(39) NOT NULL,
  `attempt_count` int(11) NOT NULL,
  `last_attempt` datetime(6) NOT NULL,
  `locked_until` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_loginattempt_username_ip_address_dff4c7b2_uniq` (`username`,`ip_address`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_loginattempt`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `accounts_loginattempt` WRITE;
/*!40000 ALTER TABLE `accounts_loginattempt` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_loginattempt` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `id` uuid NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(17) NOT NULL,
  `role` varchar(20) NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_online` tinyint(1) NOT NULL,
  `last_activity` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES
('pbkdf2_sha256$1200000$sUklvMdT8I4jFOyHNmKQwD$jq4NE/pZ3vWAoZRaqe7IuZ6kBKkY4YV9jBY3+VX4y0w=','2026-07-31 22:17:30.531037',1,'stewart','','',1,'2026-07-31 22:17:23.379485','665b50ca-d929-4696-8b52-7cbbd1c04439','stewartmilton59@gmail.com','','cashier','',1,1,'2026-07-31 22:38:00.974524','2026-07-31 22:17:23.616014','2026-07-31 22:17:30.823639');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` uuid NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` uuid NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `accounts_useractivitylog`
--

DROP TABLE IF EXISTS `accounts_useractivitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_useractivitylog` (
  `id` uuid NOT NULL,
  `action` varchar(20) NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `object_id` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `user_agent` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_useractivitylog_user_id_33f5b02a_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_useractivitylog_user_id_33f5b02a_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_useractivitylog`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `accounts_useractivitylog` WRITE;
/*!40000 ALTER TABLE `accounts_useractivitylog` DISABLE KEYS */;
INSERT INTO `accounts_useractivitylog` VALUES
('5a3d5996-2d0c-4d9b-bf1e-0a457f8a634e','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:24:01.753230','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('318778a0-afc9-45d9-8932-13259814d0c5','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:20:00.154909','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('f6af88ec-a2ad-4448-ae7b-17a11bab9458','view','','','Visited /inventory/products/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:29:03.179431','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('334a18a6-92c4-41ac-8d85-1e6c475e0c8f','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:27:03.445690','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('0b8c7498-419f-498c-9b89-1e9000147724','view','','','Visited /core/backup/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:29:57.420694','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('2f0ec73f-7940-4c58-8f1f-24250397755a','view','','','Visited /pos/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:37:04.944193','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('43c6ebc8-abe8-4ff9-a17c-3c87f66646be','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:36:20.777215','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('b75048c0-f25c-4071-9795-3ca1d8993a9a','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:23:01.406790','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('7a31d89f-e8fa-4806-9197-4dfbbe93b1a9','view','','','Visited /core/backup/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:29:26.163602','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('92cbc328-dcfb-440b-9f40-4e2b05aec674','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:28:03.887766','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('b3ef11b3-6985-4205-a913-563301c1fce3','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:22:00.940837','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('2ea0ba04-9b72-4bf9-8c29-5ee26f44981a','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:25:02.350997','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('cf520993-da2f-4f67-8d29-6a2162acec52','view','','','Visited /','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:17:31.210900','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('b8beba04-1a7b-4da9-88a0-6fa79cc6f33b','view','','','Visited /core/backup/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:35:12.992260','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('10d10f87-6ae8-4dc6-a67f-74008ff2d05e','view','','','Visited /purchases/orders/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:28:33.807610','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('dc1e45cc-fa45-4978-8258-765d88ca2e62','view','','','Visited /core/settings/company/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:29:21.295430','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('b3ed882c-9c76-4fa7-9ac5-8f98da5a51a7','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:35:16.002501','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('62eaabad-ee6d-49a6-b15c-917d20ffb329','view','','','Visited /core/backup/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:37:37.584603','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('a8a0b798-ec00-46cf-bb38-937e14888705','view','','','Visited /inventory/products/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:29:08.846327','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('f03aa0e3-2e6a-4115-8df7-9726cc4c0090','view','','','Visited /sales/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:37:00.478366','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('7b0d42e7-6535-44de-835b-97d6bd0b3d58','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:36:54.786999','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('d2eea92e-7b72-4223-bf1a-9a811a35b87b','view','','','Visited /core/backup/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:29:37.797409','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('09871cbb-c25e-4bc8-b52a-afe082451740','view','','','Visited /inventory/products/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:17:51.125106','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('1a9e9fc9-a2c9-4b4c-a388-b021b19c1f6b','view','','','Visited /inventory/products/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:28:40.061327','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('91fe3778-7321-4fa9-9640-b21d113aa340','view','','','Visited /core/backup/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:32:18.470083','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('f7c14d69-a877-4ded-bbf2-b72a6a00146e','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:17:55.615351','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('d43497c5-2fda-4185-ab39-b8923c64e211','view','','','Visited /pos/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:30:10.361240','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('e1544479-e56d-4891-8696-bf7da50f89f5','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:26:02.757999','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('f2a01261-8b5f-466f-95db-e7010796027a','login','','','User logged in from IP 127.0.0.1','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:17:31.014299','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('163c6900-af9c-407b-93b7-eaccc45a38db','view','','','Visited /core/settings/company/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:32:14.264177','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('7d45c2f9-b36a-4bd3-a8f2-ef0fd22c3782','view','','','Visited /pos-table/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:37:05.025750','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('759049a2-e51e-467c-b853-efde018177ad','view','','','Visited /pos-table/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:30:10.481793','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('0d413087-8370-40a1-83d0-f5b079394eaa','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:18:59.681217','665b50ca-d929-4696-8b52-7cbbd1c04439'),
('efb90b19-0382-4334-824d-f9649354f076','view','','','Visited /core/dashboard/','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0','2026-07-31 22:21:00.531998','665b50ca-d929-4696-8b52-7cbbd1c04439');
/*!40000 ALTER TABLE `accounts_useractivitylog` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `accounts_userprofile`
--

DROP TABLE IF EXISTS `accounts_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_userprofile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address` longtext NOT NULL,
  `emergency_contact` varchar(100) NOT NULL,
  `emergency_phone` varchar(17) NOT NULL,
  `hire_date` date DEFAULT NULL,
  `department` varchar(100) NOT NULL,
  `bio` longtext NOT NULL,
  `theme` varchar(10) NOT NULL,
  `notifications_enabled` tinyint(1) NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  CONSTRAINT `accounts_userprofile_user_id_92240672_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `accounts_userprofile` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile` DISABLE KEYS */;
INSERT INTO `accounts_userprofile` VALUES
(1,NULL,NULL,'','','',NULL,'','','light',1,'665b50ca-d929-4696-8b52-7cbbd1c04439');
/*!40000 ALTER TABLE `accounts_userprofile` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',3,'add_permission'),
(6,'Can change permission',3,'change_permission'),
(7,'Can delete permission',3,'delete_permission'),
(8,'Can view permission',3,'view_permission'),
(9,'Can add group',2,'add_group'),
(10,'Can change group',2,'change_group'),
(11,'Can delete group',2,'delete_group'),
(12,'Can view group',2,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add email address',6,'add_emailaddress'),
(22,'Can change email address',6,'change_emailaddress'),
(23,'Can delete email address',6,'delete_emailaddress'),
(24,'Can view email address',6,'view_emailaddress'),
(25,'Can add email confirmation',7,'add_emailconfirmation'),
(26,'Can change email confirmation',7,'change_emailconfirmation'),
(27,'Can delete email confirmation',7,'delete_emailconfirmation'),
(28,'Can view email confirmation',7,'view_emailconfirmation'),
(29,'Can add social account',8,'add_socialaccount'),
(30,'Can change social account',8,'change_socialaccount'),
(31,'Can delete social account',8,'delete_socialaccount'),
(32,'Can view social account',8,'view_socialaccount'),
(33,'Can add social application',9,'add_socialapp'),
(34,'Can change social application',9,'change_socialapp'),
(35,'Can delete social application',9,'delete_socialapp'),
(36,'Can view social application',9,'view_socialapp'),
(37,'Can add social application token',10,'add_socialtoken'),
(38,'Can change social application token',10,'change_socialtoken'),
(39,'Can delete social application token',10,'delete_socialtoken'),
(40,'Can view social application token',10,'view_socialtoken'),
(41,'Can add User',12,'add_user'),
(42,'Can change User',12,'change_user'),
(43,'Can delete User',12,'delete_user'),
(44,'Can view User',12,'view_user'),
(45,'Can add login attempt',11,'add_loginattempt'),
(46,'Can change login attempt',11,'change_loginattempt'),
(47,'Can delete login attempt',11,'delete_loginattempt'),
(48,'Can view login attempt',11,'view_loginattempt'),
(49,'Can add User Activity Log',13,'add_useractivitylog'),
(50,'Can change User Activity Log',13,'change_useractivitylog'),
(51,'Can delete User Activity Log',13,'delete_useractivitylog'),
(52,'Can view User Activity Log',13,'view_useractivitylog'),
(53,'Can add user profile',14,'add_userprofile'),
(54,'Can change user profile',14,'change_userprofile'),
(55,'Can delete user profile',14,'delete_userprofile'),
(56,'Can view user profile',14,'view_userprofile'),
(57,'Can add company',18,'add_company'),
(58,'Can change company',18,'change_company'),
(59,'Can delete company',18,'delete_company'),
(60,'Can view company',18,'view_company'),
(61,'Can add email template',20,'add_emailtemplate'),
(62,'Can change email template',20,'change_emailtemplate'),
(63,'Can delete email template',20,'delete_emailtemplate'),
(64,'Can view email template',20,'view_emailtemplate'),
(65,'Can add system setting',23,'add_systemsetting'),
(66,'Can change system setting',23,'change_systemsetting'),
(67,'Can delete system setting',23,'delete_systemsetting'),
(68,'Can view system setting',23,'view_systemsetting'),
(69,'Can add activity log',15,'add_activitylog'),
(70,'Can change activity log',15,'change_activitylog'),
(71,'Can delete activity log',15,'delete_activitylog'),
(72,'Can view activity log',15,'view_activitylog'),
(73,'Can add backup',16,'add_backup'),
(74,'Can change backup',16,'change_backup'),
(75,'Can delete backup',16,'delete_backup'),
(76,'Can view backup',16,'view_backup'),
(77,'Can add branch',17,'add_branch'),
(78,'Can change branch',17,'change_branch'),
(79,'Can delete branch',17,'delete_branch'),
(80,'Can view branch',17,'view_branch'),
(81,'Can add document',19,'add_document'),
(82,'Can change document',19,'change_document'),
(83,'Can delete document',19,'delete_document'),
(84,'Can view document',19,'view_document'),
(85,'Can add notification',21,'add_notification'),
(86,'Can change notification',21,'change_notification'),
(87,'Can delete notification',21,'delete_notification'),
(88,'Can view notification',21,'view_notification'),
(89,'Can add payment method',22,'add_paymentmethod'),
(90,'Can change payment method',22,'change_paymentmethod'),
(91,'Can delete payment method',22,'delete_paymentmethod'),
(92,'Can view payment method',22,'view_paymentmethod'),
(93,'Can add category',24,'add_category'),
(94,'Can change category',24,'change_category'),
(95,'Can delete category',24,'delete_category'),
(96,'Can view category',24,'view_category'),
(97,'Can add product',26,'add_product'),
(98,'Can change product',26,'change_product'),
(99,'Can delete product',26,'delete_product'),
(100,'Can view product',26,'view_product'),
(101,'Can add inventory adjustment',25,'add_inventoryadjustment'),
(102,'Can change inventory adjustment',25,'change_inventoryadjustment'),
(103,'Can delete inventory adjustment',25,'delete_inventoryadjustment'),
(104,'Can view inventory adjustment',25,'view_inventoryadjustment'),
(105,'Can add stock alert',27,'add_stockalert'),
(106,'Can change stock alert',27,'change_stockalert'),
(107,'Can delete stock alert',27,'delete_stockalert'),
(108,'Can view stock alert',27,'view_stockalert'),
(109,'Can add stock movement',28,'add_stockmovement'),
(110,'Can change stock movement',28,'change_stockmovement'),
(111,'Can delete stock movement',28,'delete_stockmovement'),
(112,'Can view stock movement',28,'view_stockmovement'),
(113,'Can add purchase order',29,'add_purchaseorder'),
(114,'Can change purchase order',29,'change_purchaseorder'),
(115,'Can delete purchase order',29,'delete_purchaseorder'),
(116,'Can view purchase order',29,'view_purchaseorder'),
(117,'Can add purchase order item',30,'add_purchaseorderitem'),
(118,'Can change purchase order item',30,'change_purchaseorderitem'),
(119,'Can delete purchase order item',30,'delete_purchaseorderitem'),
(120,'Can view purchase order item',30,'view_purchaseorderitem'),
(121,'Can add customer',32,'add_customer'),
(122,'Can change customer',32,'change_customer'),
(123,'Can delete customer',32,'delete_customer'),
(124,'Can view customer',32,'view_customer'),
(125,'Can add loyalty card',33,'add_loyaltycard'),
(126,'Can change loyalty card',33,'change_loyaltycard'),
(127,'Can delete loyalty card',33,'delete_loyaltycard'),
(128,'Can view loyalty card',33,'view_loyaltycard'),
(129,'Can add sale',36,'add_sale'),
(130,'Can change sale',36,'change_sale'),
(131,'Can delete sale',36,'delete_sale'),
(132,'Can view sale',36,'view_sale'),
(133,'Can add payment',35,'add_payment'),
(134,'Can change payment',35,'change_payment'),
(135,'Can delete payment',35,'delete_payment'),
(136,'Can view payment',35,'view_payment'),
(137,'Can add loyalty transaction',34,'add_loyaltytransaction'),
(138,'Can change loyalty transaction',34,'change_loyaltytransaction'),
(139,'Can delete loyalty transaction',34,'delete_loyaltytransaction'),
(140,'Can view loyalty transaction',34,'view_loyaltytransaction'),
(141,'Can add credit record',31,'add_creditrecord'),
(142,'Can change credit record',31,'change_creditrecord'),
(143,'Can delete credit record',31,'delete_creditrecord'),
(144,'Can view credit record',31,'view_creditrecord'),
(145,'Can add sale item',37,'add_saleitem'),
(146,'Can change sale item',37,'change_saleitem'),
(147,'Can delete sale item',37,'delete_saleitem'),
(148,'Can view sale item',37,'view_saleitem'),
(149,'Can add sale return',38,'add_salereturn'),
(150,'Can change sale return',38,'change_salereturn'),
(151,'Can delete sale return',38,'delete_salereturn'),
(152,'Can view sale return',38,'view_salereturn'),
(153,'Can add sale return item',39,'add_salereturnitem'),
(154,'Can change sale return item',39,'change_salereturnitem'),
(155,'Can delete sale return item',39,'delete_salereturnitem'),
(156,'Can view sale return item',39,'view_salereturnitem');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_activitylog`
--

DROP TABLE IF EXISTS `core_activitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_activitylog` (
  `id` uuid NOT NULL,
  `action` varchar(20) NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `object_id` varchar(100) NOT NULL,
  `object_repr` varchar(200) NOT NULL,
  `changes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`changes`)),
  `ip_address` char(39) DEFAULT NULL,
  `user_agent` longtext NOT NULL,
  `url` varchar(500) NOT NULL,
  `method` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_activitylog_user_id_8705e516_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `core_activitylog_user_id_8705e516_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_activitylog`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_activitylog` WRITE;
/*!40000 ALTER TABLE `core_activitylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_activitylog` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_backup`
--

DROP TABLE IF EXISTS `core_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_backup` (
  `id` uuid NOT NULL,
  `name` varchar(200) NOT NULL,
  `backup_type` varchar(20) NOT NULL,
  `file_path` varchar(500) NOT NULL,
  `file_size` bigint(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `started_at` datetime(6) NOT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `error_message` longtext NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_backup_created_by_id_961e3b8d_fk_accounts_user_id` (`created_by_id`),
  CONSTRAINT `core_backup_created_by_id_961e3b8d_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_backup`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_backup` WRITE;
/*!40000 ALTER TABLE `core_backup` DISABLE KEYS */;
INSERT INTO `core_backup` VALUES
('3895e82f-db80-462b-8ec5-4e671a4e75ce','first_backup','database','',0,'running','2026-07-31 22:38:01.192549',NULL,'','665b50ca-d929-4696-8b52-7cbbd1c04439');
/*!40000 ALTER TABLE `core_backup` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_branch`
--

DROP TABLE IF EXISTS `core_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_branch` (
  `id` uuid NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` longtext NOT NULL,
  `is_main_branch` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `manager_id` uuid DEFAULT NULL,
  `company_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `core_branch_manager_id_0d6986fc_fk_accounts_user_id` (`manager_id`),
  KEY `core_branch_company_id_5c90dacf_fk_core_company_id` (`company_id`),
  CONSTRAINT `core_branch_company_id_5c90dacf_fk_core_company_id` FOREIGN KEY (`company_id`) REFERENCES `core_company` (`id`),
  CONSTRAINT `core_branch_manager_id_0d6986fc_fk_accounts_user_id` FOREIGN KEY (`manager_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_branch`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_branch` WRITE;
/*!40000 ALTER TABLE `core_branch` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_branch` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_company`
--

DROP TABLE IF EXISTS `core_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_company` (
  `id` uuid NOT NULL,
  `name` varchar(200) NOT NULL,
  `legal_name` varchar(200) NOT NULL,
  `tax_id` varchar(50) NOT NULL,
  `registration_no` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `website` varchar(200) NOT NULL,
  `address` longtext NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `country` varchar(100) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `favicon` varchar(100) DEFAULT NULL,
  `currency` varchar(3) NOT NULL,
  `currency_symbol` varchar(5) NOT NULL,
  `date_format` varchar(20) NOT NULL,
  `time_format` varchar(20) NOT NULL,
  `timezone` varchar(50) NOT NULL,
  `enable_loyalty` tinyint(1) NOT NULL,
  `enable_prescription` tinyint(1) NOT NULL,
  `enable_multi_branch` tinyint(1) NOT NULL,
  `enable_email_notifications` tinyint(1) NOT NULL,
  `enable_sms_notifications` tinyint(1) NOT NULL,
  `invoice_prefix` varchar(20) NOT NULL,
  `invoice_footer_text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `color_changes_remaining` int(11) NOT NULL,
  `location` varchar(200) NOT NULL,
  `p_o_box` varchar(100) NOT NULL,
  `primary_color` varchar(7) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_company`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_company` WRITE;
/*!40000 ALTER TABLE `core_company` DISABLE KEYS */;
INSERT INTO `core_company` VALUES
('0894eb4f-bffd-4ef9-a9c2-d89cc93ce8fe','agentflow Pharmacy','','','','','','','','','','','','Tanzania','','','TZS','TSh','Y-m-d','H:i','Africa/Dar_es_Salaam',1,1,0,1,0,'INV','','2026-07-31 22:29:21.328689','2026-07-31 22:29:21.328734',5,'','','#0d5c3a');
/*!40000 ALTER TABLE `core_company` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_document`
--

DROP TABLE IF EXISTS `core_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_document` (
  `id` uuid NOT NULL,
  `document_type` varchar(20) NOT NULL,
  `document_number` varchar(100) NOT NULL,
  `file` varchar(100) NOT NULL,
  `related_model` varchar(100) NOT NULL,
  `related_id` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `size` int(11) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_document_created_by_id_27ee15cc_fk_accounts_user_id` (`created_by_id`),
  CONSTRAINT `core_document_created_by_id_27ee15cc_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_document`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_document` WRITE;
/*!40000 ALTER TABLE `core_document` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_document` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_emailtemplate`
--

DROP TABLE IF EXISTS `core_emailtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_emailtemplate` (
  `id` uuid NOT NULL,
  `name` varchar(100) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `body` longtext NOT NULL,
  `variables` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`variables`)),
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_emailtemplate`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_emailtemplate` WRITE;
/*!40000 ALTER TABLE `core_emailtemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_emailtemplate` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_notification`
--

DROP TABLE IF EXISTS `core_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notification` (
  `id` uuid NOT NULL,
  `title` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `notification_type` varchar(20) NOT NULL,
  `priority` varchar(10) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `read_at` datetime(6) DEFAULT NULL,
  `link` varchar(500) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_notification_user_id_6e341aac_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `core_notification_user_id_6e341aac_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notification`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_notification` WRITE;
/*!40000 ALTER TABLE `core_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_notification` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_paymentmethod`
--

DROP TABLE IF EXISTS `core_paymentmethod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_paymentmethod` (
  `id` uuid NOT NULL,
  `bank_name` varchar(200) NOT NULL,
  `account_name` varchar(200) NOT NULL,
  `account_number` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `company_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_paymentmethod_company_id_3f7d771a_fk_core_company_id` (`company_id`),
  CONSTRAINT `core_paymentmethod_company_id_3f7d771a_fk_core_company_id` FOREIGN KEY (`company_id`) REFERENCES `core_company` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_paymentmethod`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_paymentmethod` WRITE;
/*!40000 ALTER TABLE `core_paymentmethod` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_paymentmethod` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `core_systemsetting`
--

DROP TABLE IF EXISTS `core_systemsetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_systemsetting` (
  `id` uuid NOT NULL,
  `setting_key` varchar(100) NOT NULL,
  `setting_value` longtext NOT NULL,
  `setting_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `is_encrypted` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_systemsetting`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `core_systemsetting` WRITE;
/*!40000 ALTER TABLE `core_systemsetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_systemsetting` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(6,'account','emailaddress'),
(7,'account','emailconfirmation'),
(11,'accounts','loginattempt'),
(12,'accounts','user'),
(13,'accounts','useractivitylog'),
(14,'accounts','userprofile'),
(1,'admin','logentry'),
(2,'auth','group'),
(3,'auth','permission'),
(4,'contenttypes','contenttype'),
(15,'core','activitylog'),
(16,'core','backup'),
(17,'core','branch'),
(18,'core','company'),
(19,'core','document'),
(20,'core','emailtemplate'),
(21,'core','notification'),
(22,'core','paymentmethod'),
(23,'core','systemsetting'),
(24,'inventory','category'),
(25,'inventory','inventoryadjustment'),
(26,'inventory','product'),
(27,'inventory','stockalert'),
(28,'inventory','stockmovement'),
(29,'purchases','purchaseorder'),
(30,'purchases','purchaseorderitem'),
(31,'sales','creditrecord'),
(32,'sales','customer'),
(33,'sales','loyaltycard'),
(34,'sales','loyaltytransaction'),
(35,'sales','payment'),
(36,'sales','sale'),
(37,'sales','saleitem'),
(38,'sales','salereturn'),
(39,'sales','salereturnitem'),
(5,'sessions','session'),
(8,'socialaccount','socialaccount'),
(9,'socialaccount','socialapp'),
(10,'socialaccount','socialtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2026-07-31 22:12:48.099520'),
(2,'contenttypes','0002_remove_content_type_name','2026-07-31 22:12:48.952791'),
(3,'auth','0001_initial','2026-07-31 22:12:52.720733'),
(4,'auth','0002_alter_permission_name_max_length','2026-07-31 22:12:53.221227'),
(5,'auth','0003_alter_user_email_max_length','2026-07-31 22:12:53.239378'),
(6,'auth','0004_alter_user_username_opts','2026-07-31 22:12:53.261471'),
(7,'auth','0005_alter_user_last_login_null','2026-07-31 22:12:53.282671'),
(8,'auth','0006_require_contenttypes_0002','2026-07-31 22:12:53.300491'),
(9,'auth','0007_alter_validators_add_error_messages','2026-07-31 22:12:53.329911'),
(10,'auth','0008_alter_user_username_max_length','2026-07-31 22:12:53.349854'),
(11,'auth','0009_alter_user_last_name_max_length','2026-07-31 22:12:53.371357'),
(12,'auth','0010_alter_group_name_max_length','2026-07-31 22:12:54.440896'),
(13,'auth','0011_update_proxy_permissions','2026-07-31 22:12:54.465384'),
(14,'auth','0012_alter_user_first_name_max_length','2026-07-31 22:12:54.475414'),
(15,'accounts','0001_initial','2026-07-31 22:13:01.521035'),
(16,'account','0001_initial','2026-07-31 22:13:04.391885'),
(17,'account','0002_email_max_length','2026-07-31 22:13:04.698892'),
(18,'account','0003_alter_emailaddress_create_unique_verified_email','2026-07-31 22:13:05.203092'),
(19,'account','0004_alter_emailaddress_drop_unique_email','2026-07-31 22:13:05.523920'),
(20,'account','0005_emailaddress_idx_upper_email','2026-07-31 22:13:05.549264'),
(21,'account','0006_emailaddress_lower','2026-07-31 22:13:05.571598'),
(22,'account','0007_emailaddress_idx_email','2026-07-31 22:13:06.533771'),
(23,'account','0008_emailaddress_unique_primary_email_fixup','2026-07-31 22:13:06.570700'),
(24,'account','0009_emailaddress_unique_primary_email','2026-07-31 22:13:06.584320'),
(25,'accounts','0002_fix_employee_id','2026-07-31 22:13:07.134737'),
(26,'accounts','0003_alter_user_role','2026-07-31 22:13:07.161214'),
(27,'admin','0001_initial','2026-07-31 22:13:08.475203'),
(28,'admin','0002_logentry_remove_auto_add','2026-07-31 22:13:08.529378'),
(29,'admin','0003_logentry_add_action_flag_choices','2026-07-31 22:13:08.552936'),
(30,'core','0001_initial','2026-07-31 22:13:14.816932'),
(31,'core','0002_company_color_changes_remaining_company_location_and_more','2026-07-31 22:13:17.033656'),
(32,'core','0003_paymentmethod','2026-07-31 22:13:18.811906'),
(33,'inventory','0001_initial','2026-07-31 22:13:28.846907'),
(34,'inventory','0002_alter_product_reorder_level','2026-07-31 22:13:28.882783'),
(35,'inventory','0003_remove_product_description_and_more','2026-07-31 22:13:30.806160'),
(36,'inventory','0004_product_description_product_is_controlled_and_more','2026-07-31 22:13:33.331852'),
(37,'inventory','0005_product_batch_number_product_expiry_date','2026-07-31 22:13:35.069605'),
(38,'inventory','0006_alter_stockalert_alert_type','2026-07-31 22:13:35.124937'),
(39,'inventory','0007_product_manufacturing_date','2026-07-31 22:13:35.453200'),
(40,'purchases','0001_initial','2026-07-31 22:13:38.983438'),
(41,'purchases','0002_purchaseorder_invoice_number_and_more','2026-07-31 22:13:42.493319'),
(42,'purchases','0003_alter_purchaseorderitem_selling_price_and_more','2026-07-31 22:13:43.662178'),
(43,'purchases','0004_fix_corrupt_decimal_data','2026-07-31 22:13:43.713787'),
(44,'sales','0001_initial','2026-07-31 22:14:05.838038'),
(45,'sales','0002_remove_customer_sales_custo_phone_43e3c6_idx_and_more','2026-07-31 22:14:09.451506'),
(46,'sales','0003_alter_customer_address_alter_customer_city_and_more','2026-07-31 22:14:11.322881'),
(47,'sales','0004_saleitem_batch_number_saleitem_expiry_date_and_more','2026-07-31 22:14:12.251118'),
(48,'sales','0005_remove_sale_prescription_image_and_more','2026-07-31 22:14:14.349962'),
(49,'sales','0006_sale_prescription_image_sale_prescription_number_and_more','2026-07-31 22:14:17.945419'),
(50,'sales','0007_alter_sale_status','2026-07-31 22:14:18.001364'),
(51,'sales','0008_alter_creditrecord_credit_amount_and_more','2026-07-31 22:14:18.115199'),
(52,'sales','0009_fix_corrupt_decimal_data','2026-07-31 22:14:18.159815'),
(53,'sessions','0001_initial','2026-07-31 22:14:18.706771'),
(54,'socialaccount','0001_initial','2026-07-31 22:14:21.950680'),
(55,'socialaccount','0002_token_max_lengths','2026-07-31 22:14:24.011073'),
(56,'socialaccount','0003_extra_data_default_dict','2026-07-31 22:14:24.085645'),
(57,'socialaccount','0004_app_provider_id_settings','2026-07-31 22:14:25.447786'),
(58,'socialaccount','0005_socialtoken_nullable_app','2026-07-31 22:14:26.939612'),
(59,'socialaccount','0006_alter_socialaccount_extra_data','2026-07-31 22:14:27.860158'),
(60,'inventory','0008_alter_product_maximum_stock_and_more','2026-07-31 22:27:31.957620');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES
('op5f7ikj8r3oidn2yjf4kdjcqs6tw8m7','.eJxVzDsOwjAQRdG9uMaWPf5T0rOGyDNjkwBKpHwqxN4hUgqo3z3vJbqyrX23LXXuBhZnEYJHr6lIzpClCznIhB5kJEQ2pJ2zWZx-GRZ61HG3fC_jbVI0jes8oNoTdayLuk5cn5ej_Tvoy9J_dSTwCaNncAYbVArJEXrPuWnDtkVvKliHkQyCYY46AdpaTIlApqF4fwC4rkEG:1wpvXn:qcASQsTVgB7UVqvcXySMym-V82qySpkCQNeC8TZBEVw','2026-08-01 06:17:31.099654');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `inventory_category`
--

DROP TABLE IF EXISTS `inventory_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_category` (
  `id` uuid NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `icon` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `inventory_category_parent_id_557e1977_fk_inventory_category_id` (`parent_id`),
  CONSTRAINT `inventory_category_parent_id_557e1977_fk_inventory_category_id` FOREIGN KEY (`parent_id`) REFERENCES `inventory_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_category`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `inventory_category` WRITE;
/*!40000 ALTER TABLE `inventory_category` DISABLE KEYS */;
INSERT INTO `inventory_category` VALUES
('aefa29ad-e51b-40c5-9894-789eb95b0115','Over-the-Counter Medicine','otc-medicine','Over-the-counter medicines available without a prescription','fas fa-pills',1,'2026-07-31 22:27:11.574891','2026-07-31 22:27:11.574928',NULL);
/*!40000 ALTER TABLE `inventory_category` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `inventory_inventoryadjustment`
--

DROP TABLE IF EXISTS `inventory_inventoryadjustment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_inventoryadjustment` (
  `id` uuid NOT NULL,
  `adjustment_number` varchar(50) NOT NULL,
  `reason` varchar(20) NOT NULL,
  `quantity` int(11) NOT NULL,
  `previous_quantity` int(11) NOT NULL,
  `new_quantity` int(11) NOT NULL,
  `notes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `approved_by_id` uuid DEFAULT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `product_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `adjustment_number` (`adjustment_number`),
  KEY `inventory_inventorya_approved_by_id_0ca917b4_fk_accounts_` (`approved_by_id`),
  KEY `inventory_inventorya_created_by_id_ddaefa76_fk_accounts_` (`created_by_id`),
  KEY `inventory_inventorya_product_id_55e36a51_fk_inventory` (`product_id`),
  CONSTRAINT `inventory_inventorya_approved_by_id_0ca917b4_fk_accounts_` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `inventory_inventorya_created_by_id_ddaefa76_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `inventory_inventorya_product_id_55e36a51_fk_inventory` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_inventoryadjustment`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `inventory_inventoryadjustment` WRITE;
/*!40000 ALTER TABLE `inventory_inventoryadjustment` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_inventoryadjustment` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `inventory_product`
--

DROP TABLE IF EXISTS `inventory_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_product` (
  `id` uuid NOT NULL,
  `name` varchar(200) NOT NULL,
  `generic_name` varchar(200) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `barcode` varchar(50) DEFAULT NULL,
  `product_type` varchar(20) NOT NULL,
  `pack_size` varchar(100) NOT NULL,
  `purchase_price` decimal(12,2) NOT NULL,
  `selling_price` decimal(12,2) DEFAULT NULL,
  `wholesale_price` decimal(12,2) DEFAULT NULL,
  `discount_percent` decimal(5,2) NOT NULL,
  `vat_percent` decimal(5,2) NOT NULL,
  `reorder_level` int(11) NOT NULL,
  `reorder_quantity` int(11) NOT NULL,
  `max_stock_level` int(11) DEFAULT NULL,
  `current_stock` int(11) NOT NULL,
  `minimum_stock` int(11) NOT NULL,
  `maximum_stock` int(11) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `prescription_required` varchar(20) NOT NULL,
  `ingredients` longtext NOT NULL,
  `dosage` varchar(200) NOT NULL,
  `storage_conditions` varchar(200) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `is_prescription` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` uuid DEFAULT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `description` longtext NOT NULL,
  `is_controlled` tinyint(1) NOT NULL,
  `license_number` varchar(100) NOT NULL,
  `requires_license` tinyint(1) NOT NULL,
  `side_effects` longtext NOT NULL,
  `batch_number` varchar(100) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `manufacturing_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  UNIQUE KEY `barcode` (`barcode`),
  KEY `inventory_p_sku_f85905_idx` (`sku`),
  KEY `inventory_p_barcode_3a77e5_idx` (`barcode`),
  KEY `inventory_p_name_f6a6a1_idx` (`name`),
  KEY `inventory_product_created_by_id_acb3b5df_fk_accounts_user_id` (`created_by_id`),
  KEY `inventory_p_is_acti_47a270_idx` (`is_active`),
  KEY `inventory_p_categor_607069_idx` (`category_id`),
  KEY `inventory_p_expiry__8b79d9_idx` (`expiry_date`),
  CONSTRAINT `inventory_product_category_id_c907876e_fk_inventory_category_id` FOREIGN KEY (`category_id`) REFERENCES `inventory_category` (`id`),
  CONSTRAINT `inventory_product_created_by_id_acb3b5df_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_product`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `inventory_product` WRITE;
/*!40000 ALTER TABLE `inventory_product` DISABLE KEYS */;
INSERT INTO `inventory_product` VALUES
('98c061c6-6fee-47b6-b8bc-00752dd3c984','Ambroxol Syrup 100ml','Ambroxol','OTC050','6364684869097','medicine','100ml bottle',1768.99,2476.59,2034.34,10.00,18.00,7,123,NULL,161,10,10000,'bottle','none','Ambroxol','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.365513','2026-07-31 22:27:41.365529','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ambroxol Syrup 100ml (100ml bottle) - Ambroxol for over-the-counter use',0,'',0,'','B0050','2028-11-10','2026-04-23'),
('7e3ae929-3efb-423a-8832-00a1a863500c','Kofein Syrup 100ml','Chlorphenamine/Paracetamol','OTC058','6238463496194','medicine','100ml bottle',1918.02,2493.43,2205.72,0.00,18.00,23,105,NULL,122,10,10000,'bottle','none','Chlorphenamine/Paracetamol','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.712443','2026-07-31 22:27:41.712474','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Kofein Syrup 100ml (100ml bottle) - Chlorphenamine/Paracetamol for over-the-counter use',0,'',0,'','B0058','2027-10-08','2026-03-03'),
('a391f2e9-97b5-4e0f-8ad3-03b2e8361883','Vitamin C 500mg','Ascorbic Acid','OTC059','6768322220181','medicine','100 tablets',1770.47,2301.61,2036.04,0.00,18.00,14,77,NULL,151,10,10000,'tablet','none','Ascorbic Acid','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.744005','2026-07-31 22:27:41.744029','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Vitamin C 500mg (100 tablets) - Ascorbic Acid for over-the-counter use',0,'',0,'','B0059','2029-01-13','2026-06-03'),
('6f908704-d8ff-45c3-8934-0571feb01b1a','Doxycycline 100mg','Doxycycline','OTC017','6442364508902','medicine','20 capsules',1694.88,2203.34,1949.11,5.00,18.00,19,182,NULL,406,10,10000,'capsule','none','Doxycycline','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.002528','2026-07-31 22:27:40.002553','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Doxycycline 100mg (20 capsules) - Doxycycline for over-the-counter use',0,'',0,'','B0017','2028-08-02','2026-03-22'),
('486cf088-0834-456c-a611-083b9355b42e','Panadol Extra','Paracetamol','OTC002','6763595448017','medicine','50 tablets',391.27,508.65,449.96,0.00,18.00,25,189,NULL,35,10,10000,'tablet','none','Paracetamol','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.349269','2026-07-31 22:27:39.349291','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Panadol Extra (50 tablets) - Paracetamol for over-the-counter use',0,'',0,'','B0002','2027-03-01','2026-06-26'),
('5efd278c-2abe-462d-83cd-0c9bf824038c','Saline Solution 500ml','Sodium Chloride','OTC087','6809174117091','medicine','500ml bottle',390.28,487.85,448.82,10.00,18.00,14,180,NULL,228,10,10000,'bottle','none','Sodium Chloride','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.143903','2026-07-31 22:27:43.143921','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Saline Solution 500ml (500ml bottle) - Sodium Chloride for over-the-counter use',0,'',0,'','B0087','2028-08-15','2026-05-24'),
('04281d29-0ef5-45fb-a3e0-0ea9cb3bef82','Piriton 4mg','Chlorphenamine','OTC042','6446273815783','medicine','30 tablets',343.85,464.20,395.43,0.00,18.00,14,179,NULL,240,10,10000,'tablet','none','Chlorphenamine','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.999796','2026-07-31 22:27:40.999812','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Piriton 4mg (30 tablets) - Chlorphenamine for over-the-counter use',0,'',0,'','B0042','2028-02-04','2026-01-14'),
('43fdb4f1-4ec6-47bd-ad2f-0eae86f39240','Paracetamol Syrup 60ml','Paracetamol','OTC010','6743158526982','medicine','60ml bottle',705.95,953.03,811.84,10.00,18.00,16,106,NULL,91,10,10000,'bottle','none','Paracetamol','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.819468','2026-07-31 22:27:39.819496','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Paracetamol Syrup 60ml (60ml bottle) - Paracetamol for over-the-counter use',0,'',0,'','B0010','2027-10-26','2026-03-15'),
('2cf13b48-233b-4e92-a685-11148d769a13','Azithromycin 500mg','Azithromycin','OTC016','6705362105548','medicine','3 tablets',457.16,640.02,525.73,5.00,18.00,21,158,NULL,412,10,10000,'tablet','none','Azithromycin','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.980583','2026-07-31 22:27:39.980602','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Azithromycin 500mg (3 tablets) - Azithromycin for over-the-counter use',0,'',0,'','B0016','2028-07-26','2026-05-21'),
('bf288bd5-67e4-4529-8027-14b412ccd72e','Hydrogen Peroxide 100ml','Hydrogen Peroxide','OTC084','6545699699578','medicine','100ml bottle',844.32,1139.83,970.97,0.00,18.00,22,168,NULL,65,10,10000,'bottle','none','Hydrogen Peroxide','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.853153','2026-07-31 22:27:42.853169','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Hydrogen Peroxide 100ml (100ml bottle) - Hydrogen Peroxide for over-the-counter use',0,'',0,'','B0084','2028-05-07','2026-02-21'),
('7c4f7087-c0ef-4595-b305-16e38306c856','Sodium Chloride 0.9%','Sodium Chloride','OTC089','6967300992787','medicine','500ml bottle',1782.53,2406.42,2049.91,5.00,18.00,5,122,NULL,161,10,10000,'bottle','none','Sodium Chloride','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.214144','2026-07-31 22:27:43.214158','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Sodium Chloride 0.9% (500ml bottle) - Sodium Chloride for over-the-counter use',0,'',0,'','B0089','2027-04-09','2026-02-23'),
('28a3444b-3670-40de-890c-18be57ccc0a5','Senokot 7.5mg','Senna','OTC037','6293379984954','medicine','20 tablets',1860.22,2604.31,2139.25,10.00,18.00,12,118,NULL,429,10,10000,'tablet','none','Senna','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.791886','2026-07-31 22:27:40.791925','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Senokot 7.5mg (20 tablets) - Senna for over-the-counter use',0,'',0,'','B0037','2027-07-13','2026-04-08'),
('c99cd3fd-7fe3-4be9-b3e2-198737547a98','Cortimoxazol 200mg','Promethazine','OTC045','6193024055640','medicine','30 tablets',1246.60,1620.58,1433.59,5.00,18.00,7,110,NULL,129,10,10000,'tablet','none','Promethazine','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.130470','2026-07-31 22:27:41.130486','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Cortimoxazol 200mg (30 tablets) - Promethazine for over-the-counter use',0,'',0,'','B0045','2028-12-19','2026-04-21'),
('dec50a5e-d4b4-415b-9360-1f589d8e9235','Benylin Syrup 100ml','Diphenhydramine','OTC052','6166210246191','medicine','100ml bottle',877.69,1228.77,1009.34,10.00,18.00,17,199,NULL,228,10,10000,'bottle','none','Diphenhydramine','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.427994','2026-07-31 22:27:41.428018','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Benylin Syrup 100ml (100ml bottle) - Diphenhydramine for over-the-counter use',0,'',0,'','B0052','2028-03-27','2026-05-11'),
('6651069c-b5cb-420c-83c8-2418074edc41','Chlorpheniramine 4mg','Chlorphenamine','OTC041','6148338665100','medicine','100 tablets',436.49,567.44,501.96,0.00,18.00,21,187,NULL,281,10,10000,'tablet','none','Chlorphenamine','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:40.931889','2026-07-31 22:27:40.931903','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Chlorpheniramine 4mg (100 tablets) - Chlorphenamine for over-the-counter use',0,'',0,'','B0041','2028-10-09','2026-03-13'),
('56c895a7-f62a-4b68-a25f-2681085df020','Ibuprofen Syrup 100ml','Ibuprofen','OTC011','6223957493142','medicine','100ml bottle',386.96,483.70,445.00,0.00,18.00,18,66,NULL,272,10,10000,'bottle','none','Ibuprofen','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:39.849644','2026-07-31 22:27:39.849692','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ibuprofen Syrup 100ml (100ml bottle) - Ibuprofen for over-the-counter use',0,'',0,'','B0011','2028-07-02','2026-05-24'),
('f482bff6-a495-4fcc-aaa4-298418720952','Fucidin Ointment 15g','Fusidic Acid','OTC076','6546688090938','medicine','15g tube',1330.09,1729.12,1529.60,10.00,18.00,14,58,NULL,108,10,10000,'tube','none','Fusidic Acid','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.402948','2026-07-31 22:27:42.402964','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Fucidin Ointment 15g (15g tube) - Fusidic Acid for over-the-counter use',0,'',0,'','B0076','2027-09-30','2026-03-09'),
('a9218a0c-c6d4-441c-aa0c-2a1a8903ad23','Calcium 500mg','Calcium Carbonate','OTC070','6211585443515','medicine','100 tablets',1407.97,1900.76,1619.17,5.00,18.00,12,142,NULL,390,10,10000,'tablet','none','Calcium Carbonate','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.226386','2026-07-31 22:27:42.226409','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Calcium 500mg (100 tablets) - Calcium Carbonate for over-the-counter use',0,'',0,'','B0070','2027-11-07','2026-05-14'),
('f7492d72-04e8-401f-aa67-2d26e4182220','Omeprazole 20mg','Omeprazole','OTC022','6564458546356','medicine','30 capsules',592.24,829.14,681.08,5.00,18.00,19,113,NULL,147,10,10000,'capsule','none','Omeprazole','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.240334','2026-07-31 22:27:40.240357','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Omeprazole 20mg (30 capsules) - Omeprazole for over-the-counter use',0,'',0,'','B0022','2027-05-19','2026-05-17'),
('bb945c47-0a05-435e-bd6b-2fa49596d680','Ranitidine 150mg','Ranitidine','OTC024','6168300472052','medicine','50 tablets',1185.27,1659.38,1363.06,10.00,18.00,5,149,NULL,268,10,10000,'tablet','none','Ranitidine','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.290213','2026-07-31 22:27:40.290228','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ranitidine 150mg (50 tablets) - Ranitidine for over-the-counter use',0,'',0,'','B0024','2028-03-19','2026-05-21'),
('a0baf3be-2d3c-4e4e-93b1-30c35c1e9b47','Paracetamol Syrup 100ml','Paracetamol','OTC009','6818172762479','medicine','100ml bottle',632.72,854.17,727.63,10.00,18.00,25,167,NULL,53,10,10000,'bottle','none','Paracetamol','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.762313','2026-07-31 22:27:39.762371','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Paracetamol Syrup 100ml (100ml bottle) - Paracetamol for over-the-counter use',0,'',0,'','B0009','2027-10-29','2026-02-25'),
('c888e26c-e8d7-4157-a5e1-31e5fb6c0400','Vitamin E 400IU','Tocopherol','OTC064','6597707816158','medicine','60 capsules',702.11,947.85,807.43,10.00,18.00,23,147,NULL,456,10,10000,'capsule','none','Tocopherol','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.937526','2026-07-31 22:27:41.937561','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Vitamin E 400IU (60 capsules) - Tocopherol for over-the-counter use',0,'',0,'','B0064','2027-12-24','2026-05-01'),
('10248b57-9cf0-4a4d-9f73-3395a300b441','Rennie Tablets','Calcium Carbonate','OTC095','6201991584928','medicine','24 tablets',1601.36,2081.77,1841.56,0.00,18.00,25,75,NULL,343,10,10000,'tablet','none','Calcium Carbonate','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.365069','2026-07-31 22:27:43.365084','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Rennie Tablets (24 tablets) - Calcium Carbonate for over-the-counter use',0,'',0,'','B0095','2027-09-25','2026-03-13'),
('db34ca78-a497-481a-917d-33ab69285ffe','Dettol Antiseptic 200ml','Chloroxylenol','OTC083','6861977213598','medicine','200ml bottle',1956.20,2640.87,2249.63,5.00,18.00,17,190,NULL,73,10,10000,'bottle','none','Chloroxylenol','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.801747','2026-07-31 22:27:42.801791','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Dettol Antiseptic 200ml (200ml bottle) - Chloroxylenol for over-the-counter use',0,'',0,'','B0083','2028-12-14','2026-02-26'),
('ab24aab8-89f2-4263-b572-39fd559cca46','Iodine Solution 30ml','Povidone Iodine','OTC085','6588017414546','medicine','30ml bottle',1261.46,1766.04,1450.68,0.00,18.00,13,190,NULL,116,10,10000,'bottle','none','Povidone Iodine','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.089976','2026-07-31 22:27:43.089991','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Iodine Solution 30ml (30ml bottle) - Povidone Iodine for over-the-counter use',0,'',0,'','B0085','2027-03-24','2026-06-19'),
('509ca58c-469f-4d0c-a29e-3a5820de09aa','ORS Sachets','Oral Rehydration Salts','OTC032','6762635097563','medicine','20 sachets',1333.19,1799.81,1533.17,5.00,18.00,11,117,NULL,400,10,10000,'sachet','none','Oral Rehydration Salts','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.578231','2026-07-31 22:27:40.578251','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'ORS Sachets (20 sachets) - Oral Rehydration Salts for over-the-counter use',0,'',0,'','B0032','2027-05-17','2026-05-10'),
('320ca72c-56d5-49bb-97af-3d5d4ef16099','Gaviscon Extra 500ml','Alginic Acid','OTC096','6973271539679','medicine','500ml bottle',813.03,1016.29,934.98,5.00,18.00,16,145,NULL,375,10,10000,'bottle','none','Alginic Acid','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.388118','2026-07-31 22:27:43.388140','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Gaviscon Extra 500ml (500ml bottle) - Alginic Acid for over-the-counter use',0,'',0,'','B0096','2027-07-17','2026-06-18'),
('dfa47d96-55e1-4429-b90f-41d3f45d23a0','Activated Charcoal 250mg','Charcoal','OTC091','6523362647197','medicine','30 capsules',859.24,1117.01,988.13,10.00,18.00,6,131,NULL,497,10,10000,'capsule','none','Charcoal','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:43.254750','2026-07-31 22:27:43.254764','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Activated Charcoal 250mg (30 capsules) - Charcoal for over-the-counter use',0,'',0,'','B0091','2028-05-08','2026-05-04'),
('3ca233d7-02d6-456b-968b-42b750372f36','Famotidine 20mg','Famotidine','OTC094','6451990349323','medicine','30 tablets',1581.68,2214.35,1818.93,10.00,18.00,22,59,NULL,456,10,10000,'tablet','none','Famotidine','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.344998','2026-07-31 22:27:43.345024','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Famotidine 20mg (30 tablets) - Famotidine for over-the-counter use',0,'',0,'','B0094','2027-12-30','2026-01-23'),
('01fa3f99-6bf1-4d42-b78a-43484d05405e','Diclofenac 50mg','Diclofenac Sodium','OTC007','6329159142739','medicine','100 tablets',947.20,1278.72,1089.28,0.00,18.00,24,93,NULL,447,10,10000,'tablet','none','Diclofenac Sodium','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.714634','2026-07-31 22:27:39.714650','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Diclofenac 50mg (100 tablets) - Diclofenac Sodium for over-the-counter use',0,'',0,'','B0007','2028-11-08','2026-04-25'),
('fc35d45b-dbfc-46a8-aef9-44000aa2a220','Calendula Cream 50g','Calendula','OTC081','6941811753545','medicine','50g tube',1962.73,2453.41,2257.14,0.00,18.00,10,170,NULL,448,10,10000,'tube','none','Calendula','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:42.636584','2026-07-31 22:27:42.636602','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Calendula Cream 50g (50g tube) - Calendula for over-the-counter use',0,'',0,'','B0081','2028-12-18','2026-04-25'),
('7460d440-3c91-4c81-8c97-4c6020ca0d0f','Lactulose Syrup 200ml','Lactulose','OTC036','6956217530058','medicine','200ml bottle',711.85,889.81,818.63,10.00,18.00,24,89,NULL,369,10,10000,'bottle','none','Lactulose','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.721615','2026-07-31 22:27:40.721633','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Lactulose Syrup 200ml (200ml bottle) - Lactulose for over-the-counter use',0,'',0,'','B0036','2027-08-31','2026-02-09'),
('bfcf2b02-77b8-4989-bd29-51772a56d417','Aspirin 300mg','Acetylsalicylic Acid','OTC005','6424493543665','medicine','100 tablets',455.48,569.35,523.80,5.00,18.00,23,99,NULL,294,10,10000,'tablet','none','Acetylsalicylic Acid','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.635804','2026-07-31 22:27:39.635820','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Aspirin 300mg (100 tablets) - Acetylsalicylic Acid for over-the-counter use',0,'',0,'','B0005','2028-05-12','2026-01-23'),
('9c444807-5653-441e-8772-533ccd1fb071','Bisolvon Syrup 100ml','Bromhexine','OTC049','6591979363867','medicine','100ml bottle',1869.92,2617.89,2150.41,10.00,18.00,19,116,NULL,333,10,10000,'bottle','none','Bromhexine','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.297934','2026-07-31 22:27:41.297954','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Bisolvon Syrup 100ml (100ml bottle) - Bromhexine for over-the-counter use',0,'',0,'','B0049','2028-04-25','2026-05-23'),
('07e092d6-4550-45e1-9065-555860f6af92','Mupirocin Ointment 15g','Mupirocin','OTC078','6395959373593','medicine','15g tube',1315.28,1709.86,1512.57,0.00,18.00,6,92,NULL,78,10,10000,'tube','none','Mupirocin','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.505497','2026-07-31 22:27:42.505515','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Mupirocin Ointment 15g (15g tube) - Mupirocin for over-the-counter use',0,'',0,'','B0078','2028-04-07','2026-05-27'),
('648fa5b0-3cbb-4430-8f4c-5723f2c6c05f','Acetaminophen 650mg','Paracetamol','OTC100','6424591345661','medicine','100 tablets',685.48,925.40,788.30,0.00,18.00,17,120,NULL,74,10,10000,'tablet','none','Paracetamol','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.497840','2026-07-31 22:27:43.497861','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Acetaminophen 650mg (100 tablets) - Paracetamol for over-the-counter use',0,'',0,'','B0100','2028-06-05','2026-04-18'),
('adb54dd6-1b44-41cf-ac86-59f75fd9ed08','Gaviscon 500ml','Alginic Acid','OTC029','6108901504899','medicine','500ml bottle',1521.38,2129.93,1749.59,0.00,18.00,7,187,NULL,363,10,10000,'bottle','none','Alginic Acid','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.506650','2026-07-31 22:27:40.506690','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Gaviscon 500ml (500ml bottle) - Alginic Acid for over-the-counter use',0,'',0,'','B0029','2027-06-11','2026-03-07'),
('51651bec-5d3b-48b4-93dd-5ca0746378be','Bacitracin Ointment 15g','Bacitracin','OTC077','6851924991536','medicine','15g tube',779.89,1091.85,896.87,5.00,18.00,25,200,NULL,381,10,10000,'tube','none','Bacitracin','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.424928','2026-07-31 22:27:42.424942','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Bacitracin Ointment 15g (15g tube) - Bacitracin for over-the-counter use',0,'',0,'','B0077','2027-11-19','2026-05-04'),
('7fa888e3-60f1-46da-a0ab-5cea8f5c64b5','Ichthammol Ointment 30g','Ichthammol','OTC080','6455342117469','medicine','30g tube',1424.05,1993.67,1637.66,5.00,18.00,5,73,NULL,61,10,10000,'tube','none','Ichthammol','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.606765','2026-07-31 22:27:42.606785','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ichthammol Ointment 30g (30g tube) - Ichthammol for over-the-counter use',0,'',0,'','B0080','2028-04-20','2026-01-29'),
('8a9c7258-db1d-4281-b5b5-6126853a2c52','Bismuth Subsalicylate 262mg','Bismuth Subsalicylate','OTC097','6289708635239','medicine','48 tablets',1287.52,1673.78,1480.65,10.00,18.00,24,111,NULL,145,10,10000,'tablet','none','Bismuth Subsalicylate','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.410806','2026-07-31 22:27:43.410823','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Bismuth Subsalicylate 262mg (48 tablets) - Bismuth Subsalicylate for over-the-counter use',0,'',0,'','B0097','2027-06-26','2026-06-12'),
('627da278-85b5-4753-b73e-629004b46ba3','Panadol Extra','Paracetamol','OTC001','6345864938384','medicine','20 tablets',251.94,340.12,289.73,0.00,18.00,22,72,NULL,77,10,10000,'tablet','none','Paracetamol','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:38.532492','2026-07-31 22:27:38.532512','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Panadol Extra (20 tablets) - Paracetamol for over-the-counter use',0,'',0,'','B0001','2028-11-12','2026-05-28'),
('d3a16acc-2794-44b2-91c8-6885612b83bd','Vitamin B12 1000mcg','Cyanocobalamin','OTC065','6334022245021','medicine','30 tablets',1942.41,2525.13,2233.77,5.00,18.00,15,121,NULL,273,10,10000,'tablet','none','Cyanocobalamin','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.008726','2026-07-31 22:27:42.008749','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Vitamin B12 1000mcg (30 tablets) - Cyanocobalamin for over-the-counter use',0,'',0,'','B0065','2027-02-26','2026-04-03'),
('80d61d10-64a7-4fa7-803a-6ab3c2e9bbd5','Piriton Syrup 100ml','Chlorphenamine','OTC044','6328865551724','medicine','100ml bottle',1907.00,2574.45,2193.05,5.00,18.00,19,163,NULL,300,10,10000,'bottle','none','Chlorphenamine','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.114557','2026-07-31 22:27:41.114575','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Piriton Syrup 100ml (100ml bottle) - Chlorphenamine for over-the-counter use',0,'',0,'','B0044','2028-03-18','2026-03-14'),
('409a9653-2fd0-43f9-ace8-6aeeec7fc4e0','Ciprofloxacin 500mg','Ciprofloxacin','OTC015','6362241791770','medicine','20 tablets',943.39,1226.41,1084.90,0.00,18.00,7,174,NULL,77,10,10000,'tablet','none','Ciprofloxacin','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.958421','2026-07-31 22:27:39.958440','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ciprofloxacin 500mg (20 tablets) - Ciprofloxacin for over-the-counter use',0,'',0,'','B0015','2027-02-16','2026-02-07'),
('c459a679-aa21-4688-82c7-6c29ad616e96','ORS Sachets Orange','Oral Rehydration Salts','OTC033','6566580698915','medicine','10 sachets',1932.06,2415.08,2221.87,0.00,18.00,5,135,NULL,483,10,10000,'sachet','none','Oral Rehydration Salts','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.648862','2026-07-31 22:27:40.648889','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'ORS Sachets Orange (10 sachets) - Oral Rehydration Salts for over-the-counter use',0,'',0,'','B0033','2027-10-12','2026-04-23'),
('8ec01ee0-d475-4afe-b5d1-6fc77fce7a01','Amoxicillin 500mg','Amoxicillin','OTC012','6709761138617','medicine','21 capsules',1158.67,1564.20,1332.47,0.00,18.00,22,118,NULL,325,10,10000,'capsule','none','Amoxicillin','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.869757','2026-07-31 22:27:39.869774','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Amoxicillin 500mg (21 capsules) - Amoxicillin for over-the-counter use',0,'',0,'','B0012','2028-02-22','2026-06-30'),
('80d6b461-b5b3-44b0-8287-713d6762c04b','Cetirizine 10mg','Cetirizine','OTC038','6319998677633','medicine','30 tablets',983.04,1376.26,1130.50,5.00,18.00,14,108,NULL,75,10,10000,'tablet','none','Cetirizine','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.820999','2026-07-31 22:27:40.821022','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Cetirizine 10mg (30 tablets) - Cetirizine for over-the-counter use',0,'',0,'','B0038','2029-01-15','2026-03-07'),
('02793a23-5038-4bf0-a8a2-75768febe7ff','Miconazole Cream 20g','Miconazole Nitrate','OTC074','6674562228753','medicine','20g tube',1052.77,1368.60,1210.69,10.00,18.00,19,126,NULL,411,10,10000,'tube','none','Miconazole Nitrate','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.372016','2026-07-31 22:27:42.372030','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Miconazole Cream 20g (20g tube) - Miconazole Nitrate for over-the-counter use',0,'',0,'','B0074','2028-08-21','2026-03-27'),
('f25173f3-8692-4cdf-9d91-7eb7093b9e67','Mucinex 600mg','Guaifenesin','OTC054','6525326422970','medicine','20 tablets',758.55,1061.97,872.33,10.00,18.00,10,169,NULL,132,10,10000,'tablet','none','Guaifenesin','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.527657','2026-07-31 22:27:41.527670','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Mucinex 600mg (20 tablets) - Guaifenesin for over-the-counter use',0,'',0,'','B0054','2028-06-10','2026-04-07'),
('6d97aa83-8a7d-44e0-a772-7f8036996527','Diphenoxylate 2.5mg','Diphenoxylate','OTC098','6381146714497','medicine','20 tablets',675.59,912.05,776.93,0.00,18.00,19,123,NULL,93,10,10000,'tablet','none','Diphenoxylate','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.460018','2026-07-31 22:27:43.460037','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Diphenoxylate 2.5mg (20 tablets) - Diphenoxylate for over-the-counter use',0,'',0,'','B0098','2028-09-16','2026-01-13'),
('e152eb8d-5ebb-4fb1-9017-82b8e73022fe','Paracetamol 500mg','Paracetamol','OTC055','6804735188129','medicine','100 tablets',255.50,319.38,293.82,0.00,18.00,19,96,NULL,293,10,10000,'tablet','none','Paracetamol','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.563916','2026-07-31 22:27:41.563953','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Paracetamol 500mg (100 tablets) - Paracetamol for over-the-counter use',0,'',0,'','B0055','2028-10-26','2026-03-15'),
('f8ebec81-e062-4851-98a7-82d8c59597f6','Promethazine Syrup 100ml','Promethazine','OTC046','6366486458768','medicine','100ml bottle',607.18,758.98,698.26,0.00,18.00,19,156,NULL,432,10,10000,'bottle','none','Promethazine','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.199898','2026-07-31 22:27:41.199915','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Promethazine Syrup 100ml (100ml bottle) - Promethazine for over-the-counter use',0,'',0,'','B0046','2027-09-15','2026-03-03'),
('09527349-afaa-4410-b32e-83920b5629f8','Loperamide 2mg','Loperamide','OTC030','6370064409283','medicine','20 capsules',471.44,589.30,542.16,5.00,18.00,10,162,NULL,155,10,10000,'capsule','none','Loperamide','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.534585','2026-07-31 22:27:40.534621','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Loperamide 2mg (20 capsules) - Loperamide for over-the-counter use',0,'',0,'','B0030','2028-06-29','2026-03-30'),
('baf2593b-7254-455a-8cec-8661d1f41fb4','Claritin 10mg','Loratadine','OTC040','6216128430402','medicine','10 tablets',734.22,991.20,844.35,10.00,18.00,16,130,NULL,469,10,10000,'tablet','none','Loratadine','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.908661','2026-07-31 22:27:40.908680','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Claritin 10mg (10 tablets) - Loratadine for over-the-counter use',0,'',0,'','B0040','2027-05-26','2026-01-31'),
('82ec9bda-ab9d-4167-921b-8b3ac2ce84fd','Metoclopramide 10mg','Metoclopramide','OTC093','6182267355023','medicine','50 tablets',1135.01,1475.51,1305.26,5.00,18.00,15,151,NULL,486,10,10000,'tablet','none','Metoclopramide','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.325073','2026-07-31 22:27:43.325095','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Metoclopramide 10mg (50 tablets) - Metoclopramide for over-the-counter use',0,'',0,'','B0093','2028-07-19','2026-03-04'),
('eb9f1175-3a73-4a47-b440-8d0df4ed994a','Calpol Syrup 100ml','Paracetamol','OTC057','6346316204099','medicine','100ml bottle',1734.69,2168.36,1994.89,0.00,18.00,25,60,NULL,29,10,10000,'bottle','none','Paracetamol','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.685343','2026-07-31 22:27:41.685369','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Calpol Syrup 100ml (100ml bottle) - Paracetamol for over-the-counter use',0,'',0,'','B0057','2028-05-23','2026-01-17'),
('cf8f657f-9bc5-477b-8d6b-8e06e286e9e4','Ibuprofen 200mg','Ibuprofen','OTC004','6204710990461','medicine','50 tablets',889.13,1111.41,1022.50,5.00,18.00,24,117,NULL,410,10,10000,'tablet','none','Ibuprofen','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.615747','2026-07-31 22:27:39.615765','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ibuprofen 200mg (50 tablets) - Ibuprofen for over-the-counter use',0,'',0,'','B0004','2027-09-05','2026-04-02'),
('62f894f6-dac8-4550-bcba-8ef55e1db3fe','Iron Tablets 200mg','Ferrous Sulphate','OTC068','6920324285791','medicine','100 tablets',1287.44,1802.42,1480.56,5.00,18.00,16,166,NULL,303,10,10000,'tablet','none','Ferrous Sulphate','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.159011','2026-07-31 22:27:42.159046','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Iron Tablets 200mg (100 tablets) - Ferrous Sulphate for over-the-counter use',0,'',0,'','B0068','2028-05-26','2026-02-12'),
('6a239159-d921-407c-9182-94c1dd24cfe2','Vitamin C Effervescent','Ascorbic Acid','OTC060','6890022600581','medicine','20 tablets',1587.48,2222.47,1825.60,0.00,18.00,23,112,NULL,314,10,10000,'tablet','none','Ascorbic Acid','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.774830','2026-07-31 22:27:41.774855','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Vitamin C Effervescent (20 tablets) - Ascorbic Acid for over-the-counter use',0,'',0,'','B0060','2027-12-13','2026-05-13'),
('7c181d5e-af02-4ae2-a568-95226aba4882','Amoxicillin Suspension 100ml','Amoxicillin','OTC013','6390853813771','medicine','100ml bottle',1090.20,1526.28,1253.73,0.00,18.00,21,77,NULL,170,10,10000,'bottle','none','Amoxicillin','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.892851','2026-07-31 22:27:39.892874','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Amoxicillin Suspension 100ml (100ml bottle) - Amoxicillin for over-the-counter use',0,'',0,'','B0013','2027-05-22','2026-02-24'),
('c5be4d91-1382-428a-a4e1-95e6b3003a06','Pantoprazole 40mg','Pantoprazole','OTC026','6683482989002','medicine','30 tablets',302.74,423.84,348.15,0.00,18.00,21,70,NULL,49,10,10000,'tablet','none','Pantoprazole','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.335627','2026-07-31 22:27:40.335658','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Pantoprazole 40mg (30 tablets) - Pantoprazole for over-the-counter use',0,'',0,'','B0026','2027-12-15','2026-05-23'),
('0749b116-76d3-4e5f-900c-963f8b5427a3','Nux Vomica 200ml','Homeopathic','OTC099','6857736637113','medicine','200ml bottle',907.75,1225.46,1043.91,10.00,18.00,14,100,NULL,246,10,10000,'bottle','none','Homeopathic','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.478237','2026-07-31 22:27:43.478252','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Nux Vomica 200ml (200ml bottle) - Homeopathic for over-the-counter use',0,'',0,'','B0099','2027-04-13','2026-04-29'),
('7006a079-3584-49ba-a3b6-9a3d0941cd2b','Brufen 400mg','Ibuprofen','OTC003','6988022315787','medicine','100 tablets',1406.35,1757.94,1617.30,10.00,18.00,15,121,NULL,249,10,10000,'tablet','none','Ibuprofen','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.593469','2026-07-31 22:27:39.593487','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Brufen 400mg (100 tablets) - Ibuprofen for over-the-counter use',0,'',0,'','B0003','2027-09-10','2026-05-23'),
('15e15b20-bc14-4e9a-b9fa-9ad428c2f190','Losec 20mg','Omeprazole','OTC023','6813181846360','medicine','14 capsules',1964.70,2455.88,2259.40,0.00,18.00,7,110,NULL,433,10,10000,'capsule','none','Omeprazole','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.271247','2026-07-31 22:27:40.271280','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Losec 20mg (14 capsules) - Omeprazole for over-the-counter use',0,'',0,'','B0023','2028-04-25','2026-02-14'),
('de651f60-7013-4f49-be33-9c5538d497c7','Robitussin Syrup 100ml','Guaifenesin','OTC053','6925916252414','medicine','100ml bottle',1176.00,1587.60,1352.40,10.00,18.00,22,189,NULL,214,10,10000,'bottle','none','Guaifenesin','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.497893','2026-07-31 22:27:41.497908','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Robitussin Syrup 100ml (100ml bottle) - Guaifenesin for over-the-counter use',0,'',0,'','B0053','2028-09-08','2026-03-25'),
('0ad3f263-869b-4d86-b20c-9e4f88f4a6ba','Savlon Antiseptic 200ml','Chlorhexidine/Cetrimide','OTC082','6202946308354','medicine','200ml bottle',1398.55,1957.97,1608.33,5.00,18.00,18,135,NULL,112,10,10000,'bottle','none','Chlorhexidine/Cetrimide','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.668961','2026-07-31 22:27:42.668981','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Savlon Antiseptic 200ml (200ml bottle) - Chlorhexidine/Cetrimide for over-the-counter use',0,'',0,'','B0082','2027-11-08','2026-03-04'),
('f1ef31af-b255-4554-b5c6-a45731677df9','Aspirin Cardio 100mg','Acetylsalicylic Acid','OTC006','6190130840140','medicine','30 tablets',666.98,900.42,767.03,0.00,18.00,17,121,NULL,358,10,10000,'tablet','none','Acetylsalicylic Acid','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.683191','2026-07-31 22:27:39.683211','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Aspirin Cardio 100mg (30 tablets) - Acetylsalicylic Acid for over-the-counter use',0,'',0,'','B0006','2027-03-15','2026-05-04'),
('c088db0e-747e-49a4-b2e8-a6b70c3bd635','Dulcolax 5mg','Bisacodyl','OTC035','6239284873367','medicine','20 tablets',1909.47,2482.31,2195.89,5.00,18.00,16,60,NULL,38,10,10000,'tablet','none','Bisacodyl','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.699669','2026-07-31 22:27:40.699689','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Dulcolax 5mg (20 tablets) - Bisacodyl for over-the-counter use',0,'',0,'','B0035','2028-08-08','2026-06-22'),
('3fedac3a-9eb8-4aba-93cd-a91fe8510abe','Multivitamin Tablets','Multivitamin','OTC061','6961424120992','medicine','100 tablets',817.87,1022.34,940.55,5.00,18.00,22,159,NULL,415,10,10000,'tablet','none','Multivitamin','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:41.843131','2026-07-31 22:27:41.843157','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Multivitamin Tablets (100 tablets) - Multivitamin for over-the-counter use',0,'',0,'','B0061','2029-01-10','2026-06-22'),
('19461415-2864-449e-a7f6-a99cd2237f21','Pharcon 500mg','Paracetamol','OTC056','6470770979513','medicine','100 tablets',870.27,1218.38,1000.81,5.00,18.00,18,114,NULL,214,10,10000,'tablet','none','Paracetamol','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.598069','2026-07-31 22:27:41.598100','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Pharcon 500mg (100 tablets) - Paracetamol for over-the-counter use',0,'',0,'','B0056','2027-10-21','2026-03-27'),
('6f0ab2f4-671e-461c-8864-aab2d0dad073','Omega-3 Fish Oil','Omega-3 Fatty Acids','OTC071','6148422798459','medicine','60 capsules',1650.68,2145.88,1898.28,5.00,18.00,9,175,NULL,27,10,10000,'capsule','none','Omega-3 Fatty Acids','Take as directed','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:42.252663','2026-07-31 22:27:42.252709','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Omega-3 Fish Oil (60 capsules) - Omega-3 Fatty Acids for over-the-counter use',0,'',0,'','B0071','2027-12-03','2026-06-19'),
('6e5032da-bd16-4f3f-99ec-b2807dd07190','Oral Rehydration Salts 5','ORS','OTC090','6690328426008','medicine','5 sachets',1551.62,2017.11,1784.36,5.00,18.00,15,191,NULL,316,10,10000,'sachet','none','ORS','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.232833','2026-07-31 22:27:43.232848','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Oral Rehydration Salts 5 (5 sachets) - ORS for over-the-counter use',0,'',0,'','B0090','2028-09-20','2026-03-01'),
('ee1da714-5931-4a76-8322-b2912ef320ce','Ceftriaxone 1g Injection','Ceftriaxone','OTC021','6158965931802','medicine','1 vial',925.54,1295.76,1064.37,0.00,18.00,6,153,NULL,240,10,10000,'vial','none','Ceftriaxone','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:40.147486','2026-07-31 22:27:40.147512','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ceftriaxone 1g Injection (1 vial) - Ceftriaxone for over-the-counter use',0,'',0,'','B0021','2028-12-02','2026-01-16'),
('512b1216-8179-49e8-b6f5-b423b735d829','Vitamin D3 1000IU','Cholecalciferol','OTC063','6987408586371','medicine','60 tablets',560.93,757.26,645.07,10.00,18.00,19,161,NULL,242,10,10000,'tablet','none','Cholecalciferol','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.906330','2026-07-31 22:27:41.906351','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Vitamin D3 1000IU (60 tablets) - Cholecalciferol for over-the-counter use',0,'',0,'','B0063','2027-07-03','2026-02-15'),
('52c9c53d-8af7-4bea-a387-b5fc7d07967c','Esmoprazole 20mg','Esomeprazole','OTC027','6230583221679','medicine','28 capsules',339.86,441.82,390.84,0.00,18.00,23,60,NULL,324,10,10000,'capsule','none','Esomeprazole','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.406083','2026-07-31 22:27:40.406120','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Esmoprazole 20mg (28 capsules) - Esomeprazole for over-the-counter use',0,'',0,'','B0027','2027-04-08','2026-02-07'),
('0c2e9085-7d9c-46ea-8069-b81e4ad733ea','Fexofenadine 120mg','Fexofenadine','OTC047','6817893352516','medicine','30 tablets',1212.51,1576.26,1394.39,0.00,18.00,18,106,NULL,216,10,10000,'tablet','none','Fexofenadine','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.231571','2026-07-31 22:27:41.231595','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Fexofenadine 120mg (30 tablets) - Fexofenadine for over-the-counter use',0,'',0,'','B0047','2029-01-10','2026-07-01'),
('16e1f121-fac8-46d5-b777-bde47b69c80f','Buscopan 10mg','Hyoscine Butylbromide','OTC034','6875463562649','medicine','20 tablets',530.94,743.32,610.58,0.00,18.00,8,69,NULL,154,10,10000,'tablet','none','Hyoscine Butylbromide','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.676451','2026-07-31 22:27:40.676468','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Buscopan 10mg (20 tablets) - Hyoscine Butylbromide for over-the-counter use',0,'',0,'','B0034','2028-11-10','2026-03-15'),
('da671485-b904-400f-a035-c05796ae80e8','Zinc Sulphate 20mg','Zinc','OTC067','6422522208302','medicine','30 tablets',1205.57,1506.96,1386.41,10.00,18.00,12,128,NULL,384,10,10000,'tablet','none','Zinc','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.075990','2026-07-31 22:27:42.076037','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Zinc Sulphate 20mg (30 tablets) - Zinc for over-the-counter use',0,'',0,'','B0067','2028-11-19','2026-05-07'),
('f40f47ac-b7d2-43de-b699-c0b1ebe6d961','Flagyl Syrup 100ml','Metronidazole','OTC019','6178728590908','medicine','100ml bottle',1492.07,1939.69,1715.88,0.00,18.00,13,174,NULL,382,10,10000,'bottle','none','Metronidazole','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.104033','2026-07-31 22:27:40.104074','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Flagyl Syrup 100ml (100ml bottle) - Metronidazole for over-the-counter use',0,'',0,'','B0019','2027-04-10','2026-02-21'),
('8753450c-aebb-4c3c-bbc1-c14f7bccb91e','Ranitidine Syrup 100ml','Ranitidine','OTC025','6306823277527','medicine','100ml bottle',1066.89,1493.65,1226.92,0.00,18.00,6,198,NULL,166,10,10000,'bottle','none','Ranitidine','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.313104','2026-07-31 22:27:40.313140','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Ranitidine Syrup 100ml (100ml bottle) - Ranitidine for over-the-counter use',0,'',0,'','B0025','2028-05-07','2026-04-18'),
('4b44c62d-6391-412e-9027-c16edc67d6c4','Silver Sulfadiazine Cream 25g','Silver Sulfadiazine','OTC079','6235030135894','medicine','25g tube',1888.72,2549.77,2172.03,5.00,18.00,17,119,NULL,403,10,10000,'tube','none','Silver Sulfadiazine','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.535120','2026-07-31 22:27:42.535134','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Silver Sulfadiazine Cream 25g (25g tube) - Silver Sulfadiazine for over-the-counter use',0,'',0,'','B0079','2028-09-28','2026-03-05'),
('eff8e0a1-69c1-4ea1-ac3f-c344259fcb32','Cod Liver Oil','Vitamin A/D','OTC072','6475553953855','medicine','100 capsules',782.60,1095.64,899.99,0.00,18.00,13,172,NULL,313,10,10000,'capsule','none','Vitamin A/D','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.283724','2026-07-31 22:27:42.283773','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Cod Liver Oil (100 capsules) - Vitamin A/D for over-the-counter use',0,'',0,'','B0072','2027-02-09','2026-05-16'),
('aaea7e12-ca45-411d-a655-c7577b63dfcc','Vitamin A 10000IU','Retinol','OTC066','6891310598800','medicine','100 capsules',1258.24,1572.80,1446.98,10.00,18.00,22,111,NULL,25,10,10000,'capsule','none','Retinol','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.043102','2026-07-31 22:27:42.043159','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Vitamin A 10000IU (100 capsules) - Retinol for over-the-counter use',0,'',0,'','B0066','2028-08-19','2026-03-20'),
('ac9e367e-6934-4831-8702-cf658fbfaab5','Voltaren Gel 75g','Diclofenac Diethylamine','OTC008','6459422681391','medicine','75g tube',977.34,1270.54,1123.94,0.00,18.00,6,130,NULL,256,10,10000,'tube','none','Diclofenac Diethylamine','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.736126','2026-07-31 22:27:39.736146','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Voltaren Gel 75g (75g tube) - Diclofenac Diethylamine for over-the-counter use',0,'',0,'','B0008','2027-07-14','2026-06-18'),
('58f73080-6973-4848-bd6d-d521517fb702','Vitamin B Complex','Vitamin B Complex','OTC062','6563210400205','medicine','100 tablets',1526.43,1908.04,1755.39,0.00,18.00,18,142,NULL,279,10,10000,'tablet','none','Vitamin B Complex','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.878477','2026-07-31 22:27:41.878514','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Vitamin B Complex (100 tablets) - Vitamin B Complex for over-the-counter use',0,'',0,'','B0062','2027-04-08','2026-02-27'),
('df155e37-7abe-422f-9f55-d7e4da73596f','Diphenhydramine Syrup 100ml','Diphenhydramine','OTC043','6239820136955','medicine','100ml bottle',868.51,1172.49,998.79,10.00,18.00,17,94,NULL,229,10,10000,'bottle','none','Diphenhydramine','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.068388','2026-07-31 22:27:41.068409','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Diphenhydramine Syrup 100ml (100ml bottle) - Diphenhydramine for over-the-counter use',0,'',0,'','B0043','2028-12-10','2026-05-14'),
('43decd5a-edc5-42ba-8050-df0a181f067d','Metronidazole 400mg','Metronidazole','OTC018','6744335435865','medicine','100 tablets',660.08,891.11,759.09,0.00,18.00,23,106,NULL,146,10,10000,'tablet','none','Metronidazole','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.074391','2026-07-31 22:27:40.074446','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Metronidazole 400mg (100 tablets) - Metronidazole for over-the-counter use',0,'',0,'','B0018','2027-05-31','2026-02-11'),
('08057036-dfe9-4c1a-be97-e497150c9dd8','Loratadine 10mg','Loratadine','OTC039','6408264090646','medicine','30 tablets',595.51,803.94,684.84,10.00,18.00,22,134,NULL,357,10,10000,'tablet','none','Loratadine','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.886453','2026-07-31 22:27:40.886485','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Loratadine 10mg (30 tablets) - Loratadine for over-the-counter use',0,'',0,'','B0039','2027-02-21','2026-04-04'),
('21252309-a0f4-4fb4-a6cc-e6c139d2c3ee','Hydrocortisone Cream 15g','Hydrocortisone','OTC073','6263860419795','medicine','15g tube',1207.09,1508.86,1388.15,5.00,18.00,7,113,NULL,225,10,10000,'tube','none','Hydrocortisone','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.316903','2026-07-31 22:27:42.316933','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Hydrocortisone Cream 15g (15g tube) - Hydrocortisone for over-the-counter use',0,'',0,'','B0073','2027-04-04','2026-02-08'),
('0ef4abf8-c06b-4948-837e-e6c22ea7e679','Dextromethorphan Syrup 100ml','Dextromethorphan','OTC051','6263803069319','medicine','100ml bottle',854.69,1068.36,982.89,10.00,18.00,9,104,NULL,191,10,10000,'bottle','none','Dextromethorphan','Take as directed','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:41.395363','2026-07-31 22:27:41.395380','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Dextromethorphan Syrup 100ml (100ml bottle) - Dextromethorphan for over-the-counter use',0,'',0,'','B0051','2027-11-02','2026-05-04'),
('6b63e4bd-3178-4bfc-b79f-e87724753e9e','Betadine 10% 30ml','Povidone Iodine','OTC086','6768425855938','medicine','30ml bottle',1630.62,2038.28,1875.21,0.00,18.00,14,191,NULL,244,10,10000,'bottle','none','Povidone Iodine','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.128929','2026-07-31 22:27:43.128948','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Betadine 10% 30ml (30ml bottle) - Povidone Iodine for over-the-counter use',0,'',0,'','B0086','2027-11-18','2026-05-02'),
('0433afd2-9e74-4ca4-b23e-e95356b8b905','Co-trimoxazole 480mg','Trimethoprim/Sulfamethoxazole','OTC020','6960037124392','medicine','20 tablets',1681.73,2354.42,1933.99,10.00,18.00,11,74,NULL,87,10,10000,'tablet','none','Trimethoprim/Sulfamethoxazole','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.125576','2026-07-31 22:27:40.125602','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Co-trimoxazole 480mg (20 tablets) - Trimethoprim/Sulfamethoxazole for over-the-counter use',0,'',0,'','B0020','2028-08-02','2026-03-03'),
('804474d6-2eed-4113-9a92-e97b7eac5edf','Antacid Suspension 200ml','Aluminium/Magnesium Hydroxide','OTC028','6387482374357','medicine','200ml bottle',1395.72,1884.22,1605.08,5.00,18.00,12,117,NULL,356,10,10000,'bottle','none','Aluminium/Magnesium Hydroxide','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:40.433847','2026-07-31 22:27:40.433872','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Antacid Suspension 200ml (200ml bottle) - Aluminium/Magnesium Hydroxide for over-the-counter use',0,'',0,'','B0028','2028-04-01','2026-05-11'),
('800b536f-502d-462e-af05-ea37ef5bc180','Domperidone 10mg','Domperidone','OTC092','6237597951504','medicine','30 tablets',1559.83,2027.78,1793.80,5.00,18.00,8,162,NULL,217,10,10000,'tablet','none','Domperidone','Take as directed','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.276205','2026-07-31 22:27:43.276226','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Domperidone 10mg (30 tablets) - Domperidone for over-the-counter use',0,'',0,'','B0092','2028-02-22','2026-02-24'),
('2ac070f8-496f-4bec-ae24-f05cead19a6b','Imodium 2mg','Loperamide','OTC031','6428799513174','medicine','6 capsules',1539.67,1924.59,1770.62,0.00,18.00,9,117,NULL,433,10,10000,'capsule','none','Loperamide','Take as directed','Store below 25°C, protect from light and moisture','',1,1,0,'2026-07-31 22:27:40.556835','2026-07-31 22:27:40.556860','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Imodium 2mg (6 capsules) - Loperamide for over-the-counter use',0,'',0,'','B0031','2028-10-15','2026-01-14'),
('8a572f6c-a79d-48fc-a7b6-f06f15098e2b','Augmentin 625mg','Amoxicillin/Clavulanate','OTC014','6939124570476','medicine','14 tablets',1447.25,1881.42,1664.34,0.00,18.00,24,132,NULL,279,10,10000,'tablet','none','Amoxicillin/Clavulanate','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:39.937747','2026-07-31 22:27:39.937762','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Augmentin 625mg (14 tablets) - Amoxicillin/Clavulanate for over-the-counter use',0,'',0,'','B0014','2028-11-12','2026-05-22'),
('6ca2f9e2-3713-4f5a-9e23-f096818c23f8','Clotrimazole Cream 20g','Clotrimazole','OTC075','6941588491630','medicine','20g tube',1471.07,1838.84,1691.73,0.00,18.00,13,70,NULL,311,10,10000,'tube','none','Clotrimazole','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.391124','2026-07-31 22:27:42.391138','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Clotrimazole Cream 20g (20g tube) - Clotrimazole for over-the-counter use',0,'',0,'','B0075','2027-12-06','2026-05-10'),
('3ebe9670-298d-4cda-94fe-f48807fd3501','Folic Acid 5mg','Folic Acid','OTC069','6230204286982','medicine','100 tablets',672.15,873.80,772.97,0.00,18.00,11,105,NULL,148,10,10000,'tablet','none','Folic Acid','5ml 3 times daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:42.208709','2026-07-31 22:27:42.208725','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Folic Acid 5mg (100 tablets) - Folic Acid for over-the-counter use',0,'',0,'','B0069','2027-12-07','2026-02-15'),
('67d751cb-ebc5-4a4c-9159-f7c86e5f88b1','Desloratadine 5mg','Desloratadine','OTC048','6598737437558','medicine','30 tablets',1151.06,1496.38,1323.72,10.00,18.00,21,193,NULL,285,10,10000,'tablet','none','Desloratadine','2 tablets twice daily','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:41.267076','2026-07-31 22:27:41.267125','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Desloratadine 5mg (30 tablets) - Desloratadine for over-the-counter use',0,'',0,'','B0048','2029-01-09','2026-05-29'),
('baedd97a-224c-42a2-ab27-fc654026c370','Nasal Saline Spray','Sodium Chloride','OTC088','6707552271685','medicine','50ml spray',1188.60,1545.18,1366.89,10.00,18.00,11,180,NULL,447,10,10000,'spray','none','Sodium Chloride','1 tablet 3 times daily after meals','Store below 25°C, protect from light and moisture','',1,0,0,'2026-07-31 22:27:43.167467','2026-07-31 22:27:43.167485','aefa29ad-e51b-40c5-9894-789eb95b0115',NULL,'Nasal Saline Spray (50ml spray) - Sodium Chloride for over-the-counter use',0,'',0,'','B0088','2028-03-28','2026-05-26');
/*!40000 ALTER TABLE `inventory_product` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `inventory_stockalert`
--

DROP TABLE IF EXISTS `inventory_stockalert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_stockalert` (
  `id` uuid NOT NULL,
  `alert_type` varchar(20) NOT NULL,
  `message` longtext NOT NULL,
  `current_value` int(11) NOT NULL,
  `threshold_value` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `resolved_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` uuid NOT NULL,
  `resolved_by_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_stockalert_resolved_by_id_86b761c0_fk_accounts_user_id` (`resolved_by_id`),
  KEY `inventory_s_status_95e312_idx` (`status`),
  KEY `inventory_s_alert_t_af1483_idx` (`alert_type`),
  KEY `inventory_s_product_24631a_idx` (`product_id`,`alert_type`,`status`),
  CONSTRAINT `inventory_stockalert_product_id_11f4588d_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `inventory_stockalert_resolved_by_id_86b761c0_fk_accounts_user_id` FOREIGN KEY (`resolved_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_stockalert`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `inventory_stockalert` WRITE;
/*!40000 ALTER TABLE `inventory_stockalert` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_stockalert` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `inventory_stockmovement`
--

DROP TABLE IF EXISTS `inventory_stockmovement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_stockmovement` (
  `id` uuid NOT NULL,
  `movement_type` varchar(20) NOT NULL,
  `quantity` int(11) NOT NULL,
  `previous_quantity` int(11) NOT NULL,
  `new_quantity` int(11) NOT NULL,
  `unit_price` decimal(12,2) DEFAULT NULL,
  `total_amount` decimal(12,2) DEFAULT NULL,
  `reference_type` varchar(50) NOT NULL,
  `reference_id` varchar(100) NOT NULL,
  `notes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `product_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_stockmovem_created_by_id_9a39cb99_fk_accounts_` (`created_by_id`),
  KEY `inventory_s_product_cbdc37_idx` (`product_id`),
  KEY `inventory_s_movemen_018f99_idx` (`movement_type`),
  KEY `inventory_s_referen_5aaa1a_idx` (`reference_type`,`reference_id`),
  KEY `inventory_s_created_05ebf5_idx` (`created_at`),
  CONSTRAINT `inventory_stockmovem_created_by_id_9a39cb99_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `inventory_stockmovem_product_id_4eccfd0a_fk_inventory` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_stockmovement`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `inventory_stockmovement` WRITE;
/*!40000 ALTER TABLE `inventory_stockmovement` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_stockmovement` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `purchases_purchaseorder`
--

DROP TABLE IF EXISTS `purchases_purchaseorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases_purchaseorder` (
  `id` uuid NOT NULL,
  `po_number` varchar(50) NOT NULL,
  `order_date` datetime(6) NOT NULL,
  `notes` longtext NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `invoice_number` varchar(100) DEFAULT NULL,
  `supplier_name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `po_number` (`po_number`),
  KEY `purchases_p_po_numb_ba9e90_idx` (`po_number`),
  KEY `purchases_p_status_7fddca_idx` (`status`),
  KEY `purchases_purchaseor_created_by_id_ba3716cb_fk_accounts_` (`created_by_id`),
  CONSTRAINT `purchases_purchaseor_created_by_id_ba3716cb_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases_purchaseorder`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `purchases_purchaseorder` WRITE;
/*!40000 ALTER TABLE `purchases_purchaseorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchases_purchaseorder` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `purchases_purchaseorderitem`
--

DROP TABLE IF EXISTS `purchases_purchaseorderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases_purchaseorderitem` (
  `id` uuid NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` uuid NOT NULL,
  `purchase_order_id` uuid NOT NULL,
  `batch_number` varchar(100) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `markup_percent` decimal(5,2) NOT NULL,
  `selling_price` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchases_purchaseor_product_id_7bc01b58_fk_inventory` (`product_id`),
  KEY `purchases_purchaseor_purchase_order_id_1144ab48_fk_purchases` (`purchase_order_id`),
  CONSTRAINT `purchases_purchaseor_product_id_7bc01b58_fk_inventory` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `purchases_purchaseor_purchase_order_id_1144ab48_fk_purchases` FOREIGN KEY (`purchase_order_id`) REFERENCES `purchases_purchaseorder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases_purchaseorderitem`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `purchases_purchaseorderitem` WRITE;
/*!40000 ALTER TABLE `purchases_purchaseorderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchases_purchaseorderitem` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_creditrecord`
--

DROP TABLE IF EXISTS `sales_creditrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_creditrecord` (
  `id` uuid NOT NULL,
  `credit_number` varchar(50) NOT NULL,
  `customer_name` varchar(200) NOT NULL,
  `credit_amount` decimal(12,2) NOT NULL,
  `amount_paid` decimal(12,2) NOT NULL,
  `remaining_balance` decimal(12,2) NOT NULL,
  `due_date` date DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `notes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `customer_id` uuid DEFAULT NULL,
  `sale_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `credit_number` (`credit_number`),
  KEY `sales_credi_status_ec08a6_idx` (`status`),
  KEY `sales_credi_due_dat_a1e84f_idx` (`due_date`),
  KEY `sales_credi_custome_704679_idx` (`customer_id`),
  KEY `sales_creditrecord_created_by_id_c3ac2e3a_fk_accounts_user_id` (`created_by_id`),
  KEY `sales_creditrecord_sale_id_0420ac1f_fk_sales_sale_id` (`sale_id`),
  CONSTRAINT `sales_creditrecord_created_by_id_c3ac2e3a_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `sales_creditrecord_customer_id_7872471f_fk_sales_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `sales_customer` (`id`),
  CONSTRAINT `sales_creditrecord_sale_id_0420ac1f_fk_sales_sale_id` FOREIGN KEY (`sale_id`) REFERENCES `sales_sale` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_creditrecord`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_creditrecord` WRITE;
/*!40000 ALTER TABLE `sales_creditrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_creditrecord` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_customer`
--

DROP TABLE IF EXISTS `sales_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_customer` (
  `id` uuid NOT NULL,
  `customer_code` varchar(50) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `phone_number_2` varchar(20) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address` longtext NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `customer_type` varchar(20) NOT NULL,
  `discount_percent` decimal(5,2) NOT NULL,
  `credit_limit` decimal(12,2) NOT NULL,
  `current_balance` decimal(12,2) NOT NULL,
  `loyalty_points` int(11) NOT NULL,
  `total_spent` decimal(12,2) NOT NULL,
  `notes` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `fin` varchar(50) NOT NULL,
  `tin` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_code` (`customer_code`),
  UNIQUE KEY `sales_customer_fin_e210880c_uniq` (`fin`),
  UNIQUE KEY `sales_customer_first_name_8669a2f1_uniq` (`first_name`),
  UNIQUE KEY `sales_customer_phone_number_ed7bcc34_uniq` (`phone_number`),
  UNIQUE KEY `sales_customer_tin_a063628d_uniq` (`tin`),
  KEY `sales_custo_custome_c546c5_idx` (`customer_code`),
  KEY `sales_custo_email_b3bee2_idx` (`email`),
  KEY `sales_customer_created_by_id_f119df9d_fk_accounts_user_id` (`created_by_id`),
  KEY `sales_custo_phone_n_2cfbb3_idx` (`phone_number`),
  CONSTRAINT `sales_customer_created_by_id_f119df9d_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_customer`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_customer` WRITE;
/*!40000 ALTER TABLE `sales_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_customer` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_loyaltycard`
--

DROP TABLE IF EXISTS `sales_loyaltycard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_loyaltycard` (
  `id` uuid NOT NULL,
  `card_number` varchar(50) NOT NULL,
  `points_balance` int(11) NOT NULL,
  `points_earned` int(11) NOT NULL,
  `points_redeemed` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `issued_date` datetime(6) NOT NULL,
  `expiry_date` datetime(6) DEFAULT NULL,
  `customer_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_number` (`card_number`),
  UNIQUE KEY `customer_id` (`customer_id`),
  CONSTRAINT `sales_loyaltycard_customer_id_a2396900_fk_sales_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `sales_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_loyaltycard`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_loyaltycard` WRITE;
/*!40000 ALTER TABLE `sales_loyaltycard` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_loyaltycard` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_loyaltytransaction`
--

DROP TABLE IF EXISTS `sales_loyaltytransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_loyaltytransaction` (
  `id` uuid NOT NULL,
  `transaction_type` varchar(20) NOT NULL,
  `points` int(11) NOT NULL,
  `balance_after` int(11) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `loyalty_card_id` uuid NOT NULL,
  `sale_id` uuid DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_loyaltytransac_loyalty_card_id_61a94b01_fk_sales_loy` (`loyalty_card_id`),
  KEY `sales_loyaltytransaction_sale_id_8de9bdc8_fk_sales_sale_id` (`sale_id`),
  CONSTRAINT `sales_loyaltytransac_loyalty_card_id_61a94b01_fk_sales_loy` FOREIGN KEY (`loyalty_card_id`) REFERENCES `sales_loyaltycard` (`id`),
  CONSTRAINT `sales_loyaltytransaction_sale_id_8de9bdc8_fk_sales_sale_id` FOREIGN KEY (`sale_id`) REFERENCES `sales_sale` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_loyaltytransaction`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_loyaltytransaction` WRITE;
/*!40000 ALTER TABLE `sales_loyaltytransaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_loyaltytransaction` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_payment`
--

DROP TABLE IF EXISTS `sales_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_payment` (
  `id` uuid NOT NULL,
  `payment_number` varchar(50) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `reference_number` varchar(100) DEFAULT NULL,
  `notes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `sale_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_number` (`payment_number`),
  KEY `sales_payment_created_by_id_6b1d0cba_fk_accounts_user_id` (`created_by_id`),
  KEY `sales_payment_sale_id_c2196611_fk_sales_sale_id` (`sale_id`),
  CONSTRAINT `sales_payment_created_by_id_6b1d0cba_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `sales_payment_sale_id_c2196611_fk_sales_sale_id` FOREIGN KEY (`sale_id`) REFERENCES `sales_sale` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_payment`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_payment` WRITE;
/*!40000 ALTER TABLE `sales_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_payment` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_sale`
--

DROP TABLE IF EXISTS `sales_sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_sale` (
  `id` uuid NOT NULL,
  `invoice_number` varchar(50) NOT NULL,
  `customer_name` varchar(200) NOT NULL,
  `sale_date` datetime(6) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `discount_amount` decimal(12,2) NOT NULL,
  `discount_percent` decimal(5,2) NOT NULL,
  `tax_amount` decimal(12,2) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `amount_paid` decimal(12,2) NOT NULL,
  `change_amount` decimal(12,2) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `credit_amount` decimal(12,2) NOT NULL,
  `has_credit` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `notes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `customer_id` uuid DEFAULT NULL,
  `prescription_image` varchar(100) DEFAULT NULL,
  `prescription_number` varchar(100) NOT NULL,
  `prescription_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `sales_sale_invoice_78d822_idx` (`invoice_number`),
  KEY `sales_sale_status_532843_idx` (`status`),
  KEY `sales_sale_sale_da_2fd927_idx` (`sale_date`),
  KEY `sales_sale_has_cre_409ada_idx` (`has_credit`),
  KEY `sales_sale_created_by_id_f6773268_fk_accounts_user_id` (`created_by_id`),
  KEY `sales_sale_customer_id_2d66a408_fk_sales_customer_id` (`customer_id`),
  CONSTRAINT `sales_sale_created_by_id_f6773268_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `sales_sale_customer_id_2d66a408_fk_sales_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `sales_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_sale`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_sale` WRITE;
/*!40000 ALTER TABLE `sales_sale` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_sale` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_saleitem`
--

DROP TABLE IF EXISTS `sales_saleitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_saleitem` (
  `id` uuid NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `discount_percent` decimal(5,2) NOT NULL,
  `discount_amount` decimal(12,2) NOT NULL,
  `tax_amount` decimal(12,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `original_price` decimal(12,2) NOT NULL,
  `prescription_required` tinyint(1) NOT NULL,
  `prescription_verified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` uuid NOT NULL,
  `sale_id` uuid NOT NULL,
  `batch_number` varchar(100) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `pack_size` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_salei_sale_id_17278e_idx` (`sale_id`,`product_id`),
  KEY `sales_saleitem_product_id_aeb6c9cd_fk_inventory_product_id` (`product_id`),
  CONSTRAINT `sales_saleitem_product_id_aeb6c9cd_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `sales_saleitem_sale_id_56e67045_fk_sales_sale_id` FOREIGN KEY (`sale_id`) REFERENCES `sales_sale` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_saleitem`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_saleitem` WRITE;
/*!40000 ALTER TABLE `sales_saleitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_saleitem` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_salereturn`
--

DROP TABLE IF EXISTS `sales_salereturn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_salereturn` (
  `id` uuid NOT NULL,
  `return_number` varchar(50) NOT NULL,
  `return_date` datetime(6) NOT NULL,
  `reason` varchar(20) NOT NULL,
  `notes` longtext NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `refund_processed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `approved_by_id` uuid DEFAULT NULL,
  `created_by_id` uuid DEFAULT NULL,
  `customer_id` uuid DEFAULT NULL,
  `sale_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `return_number` (`return_number`),
  KEY `sales_salereturn_approved_by_id_aa18400b_fk_accounts_user_id` (`approved_by_id`),
  KEY `sales_salereturn_created_by_id_1703b72b_fk_accounts_user_id` (`created_by_id`),
  KEY `sales_salereturn_customer_id_c189181c_fk_sales_customer_id` (`customer_id`),
  KEY `sales_salereturn_sale_id_452d3375_fk_sales_sale_id` (`sale_id`),
  CONSTRAINT `sales_salereturn_approved_by_id_aa18400b_fk_accounts_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `sales_salereturn_created_by_id_1703b72b_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `sales_salereturn_customer_id_c189181c_fk_sales_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `sales_customer` (`id`),
  CONSTRAINT `sales_salereturn_sale_id_452d3375_fk_sales_sale_id` FOREIGN KEY (`sale_id`) REFERENCES `sales_sale` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_salereturn`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_salereturn` WRITE;
/*!40000 ALTER TABLE `sales_salereturn` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_salereturn` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `sales_salereturnitem`
--

DROP TABLE IF EXISTS `sales_salereturnitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_salereturnitem` (
  `id` uuid NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `reason` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` uuid NOT NULL,
  `sale_item_id` uuid NOT NULL,
  `sale_return_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_salereturnitem_product_id_28aa7726_fk_inventory_product_id` (`product_id`),
  KEY `sales_salereturnitem_sale_item_id_6c546f11_fk_sales_saleitem_id` (`sale_item_id`),
  KEY `sales_salereturnitem_sale_return_id_7640c06f_fk_sales_sal` (`sale_return_id`),
  CONSTRAINT `sales_salereturnitem_product_id_28aa7726_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `sales_salereturnitem_sale_item_id_6c546f11_fk_sales_saleitem_id` FOREIGN KEY (`sale_item_id`) REFERENCES `sales_saleitem` (`id`),
  CONSTRAINT `sales_salereturnitem_sale_return_id_7640c06f_fk_sales_sal` FOREIGN KEY (`sale_return_id`) REFERENCES `sales_salereturn` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_salereturnitem`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `sales_salereturnitem` WRITE;
/*!40000 ALTER TABLE `sales_salereturnitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_salereturnitem` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`extra_data`)),
  `user_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`settings`)),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-08-01  1:38:01
