-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: coordistock_db
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activo`
--

DROP TABLE IF EXISTS `activo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_reg` datetime(6) NOT NULL,
  `tipo` tinyint(1) NOT NULL,
  `categoria` varchar(50) NOT NULL,
  `activo` int unsigned DEFAULT NULL,
  `renting` tinyint(1) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `n_serie` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `id_marca_id` bigint NOT NULL,
  `mantenimiento` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `n_serie` (`n_serie`),
  UNIQUE KEY `activo` (`activo`),
  KEY `Activo_id_marca_id_629194b6_fk_Marca_id` (`id_marca_id`),
  CONSTRAINT `Activo_id_marca_id_629194b6_fk_Marca_id` FOREIGN KEY (`id_marca_id`) REFERENCES `marca` (`id`),
  CONSTRAINT `activo_chk_1` CHECK ((`activo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activo`
--

LOCK TABLES `activo` WRITE;
/*!40000 ALTER TABLE `activo` DISABLE KEYS */;
INSERT INTO `activo` VALUES (1,'2025-04-27 23:08:27.415626',1,'PC',12345,0,'ThinkCentre','MJ0GNLSD245',0,1,2,0),(2,'2025-04-27 23:09:47.080791',1,'Laptop',12345678,1,'DELL PRO MAX16','DA4643RHS',1,1,3,0),(3,'2025-04-27 23:11:03.197773',1,'Laptop',12346,0,'HP PAVLION 15','GMDS6384KFD',1,1,1,0),(4,'2025-04-27 23:11:53.617602',0,'Diadema',NULL,0,'H190','FMSM263425 ASLWFKL',1,1,4,0),(5,'2025-04-27 23:15:10.707773',1,'Monitor',12347,0,'VisionPRO32','FVSME532334',1,1,2,0);
/*!40000 ALTER TABLE `activo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrador` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `tipo_documento` varchar(3) NOT NULL,
  `numero_documento` int unsigned NOT NULL,
  `telefono` int unsigned NOT NULL,
  `contrasena` varchar(128) NOT NULL,
  `conf_contrasena` varchar(128) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `Administrador_user_id_949907f5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `administrador_chk_1` CHECK ((`numero_documento` >= 0)),
  CONSTRAINT `administrador_chk_2` CHECK ((`telefono` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agente`
--

DROP TABLE IF EXISTS `agente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `codigo` int unsigned NOT NULL,
  `cargo` varchar(50) NOT NULL,
  `tipo_documento` varchar(3) NOT NULL,
  `numero_documento` int unsigned NOT NULL,
  `email` varchar(50) NOT NULL,
  `telefono` int unsigned NOT NULL,
  `modalidad` varchar(2) NOT NULL,
  `ubicacion` varchar(50) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `id_area_id` bigint NOT NULL,
  `id_terminal_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  UNIQUE KEY `numero_documento` (`numero_documento`),
  KEY `Agente_id_area_id_d06aa28b_fk_Area_id` (`id_area_id`),
  KEY `Agente_id_terminal_id_f0e8a676_fk_Terminal_id` (`id_terminal_id`),
  CONSTRAINT `Agente_id_area_id_d06aa28b_fk_Area_id` FOREIGN KEY (`id_area_id`) REFERENCES `area` (`id`),
  CONSTRAINT `Agente_id_terminal_id_f0e8a676_fk_Terminal_id` FOREIGN KEY (`id_terminal_id`) REFERENCES `terminal` (`id`),
  CONSTRAINT `agente_chk_1` CHECK ((`codigo` >= 0)),
  CONSTRAINT `agente_chk_2` CHECK ((`numero_documento` >= 0)),
  CONSTRAINT `agente_chk_3` CHECK ((`telefono` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agente`
--

LOCK TABLES `agente` WRITE;
/*!40000 ALTER TABLE `agente` DISABLE KEYS */;
INSERT INTO `agente` VALUES (1,'Diego Alejandro Joya Ramos',39353,'Auxiliar T.I','CC',1014657689,'auxsisbg@coordinadora.com',3017590053,'PR','T1 - (BOG)-Terminal Calle13-Cra68d#13',1,1,2),(2,'Laura Valentina Gomez Mora',39354,'Agente Logitico','CC',1014657690,'lgomz@coordinadora.com',3102825873,'RM','Cra81d#13f-54',1,2,2),(3,'Marlon Roger Cano',39355,'In House','CC',1014657691,'mrcano@coordinadora.com',303367757,'ES','Cra54#10',1,3,1);
/*!40000 ALTER TABLE `agente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `area` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `area` varchar(50) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `area` (`area`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area`
--

LOCK TABLES `area` WRITE;
/*!40000 ALTER TABLE `area` DISABLE KEYS */;
INSERT INTO `area` VALUES (1,'T.I',1),(2,'Call center',1),(3,'In house',1);
/*!40000 ALTER TABLE `area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add area',7,'add_area'),(26,'Can change area',7,'change_area'),(27,'Can delete area',7,'delete_area'),(28,'Can view area',7,'view_area'),(29,'Can add marca',8,'add_marca'),(30,'Can change marca',8,'change_marca'),(31,'Can delete marca',8,'delete_marca'),(32,'Can view marca',8,'view_marca'),(33,'Can add movimiento',9,'add_movimiento'),(34,'Can change movimiento',9,'change_movimiento'),(35,'Can delete movimiento',9,'delete_movimiento'),(36,'Can view movimiento',9,'view_movimiento'),(37,'Can add terminal',10,'add_terminal'),(38,'Can change terminal',10,'change_terminal'),(39,'Can delete terminal',10,'delete_terminal'),(40,'Can view terminal',10,'view_terminal'),(41,'Can add Administrador',11,'add_administrador'),(42,'Can change Administrador',11,'change_administrador'),(43,'Can delete Administrador',11,'delete_administrador'),(44,'Can view Administrador',11,'view_administrador'),(45,'Can add agente',12,'add_agente'),(46,'Can change agente',12,'change_agente'),(47,'Can delete agente',12,'delete_agente'),(48,'Can view agente',12,'view_agente'),(49,'Can add activo',13,'add_activo'),(50,'Can change activo',13,'change_activo'),(51,'Can delete activo',13,'delete_activo'),(52,'Can view activo',13,'view_activo'),(53,'Can add detalle_movimiento',14,'add_detalle_movimiento'),(54,'Can change detalle_movimiento',14,'change_detalle_movimiento'),(55,'Can delete detalle_movimiento',14,'delete_detalle_movimiento'),(56,'Can view detalle_movimiento',14,'view_detalle_movimiento'),(57,'Can add Operador',15,'add_operador'),(58,'Can change Operador',15,'change_operador'),(59,'Can delete Operador',15,'delete_operador'),(60,'Can view Operador',15,'view_operador');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$egTazNqXMCglM4uyfRaZ4C$vnayyaHIC3OuY+wCqw+ARr3stnYxET0ejC1n24uR6xE=','2025-04-29 14:34:31.610654',1,'admin','','','dzvio2004@gmail.com',1,1,'2025-04-27 22:58:06.257891');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_movimiento`
--

DROP TABLE IF EXISTS `detalle_movimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_movimiento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `motivo` varchar(300) NOT NULL,
  `nomenclatura` varchar(50) DEFAULT NULL,
  `observaciones` varchar(300) NOT NULL,
  `id_activo_id` bigint NOT NULL,
  `id_agente_id` bigint NOT NULL,
  `id_area_id` bigint NOT NULL,
  `id_movimiento_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Detalle_movimiento_id_activo_id_1cbb86a5_fk_Activo_id` (`id_activo_id`),
  KEY `Detalle_movimiento_id_agente_id_bd4a6759_fk_Agente_id` (`id_agente_id`),
  KEY `Detalle_movimiento_id_area_id_b2e679b8_fk_Area_id` (`id_area_id`),
  KEY `Detalle_movimiento_id_movimiento_id_1f253240_fk_Movimiento_id` (`id_movimiento_id`),
  CONSTRAINT `Detalle_movimiento_id_activo_id_1cbb86a5_fk_Activo_id` FOREIGN KEY (`id_activo_id`) REFERENCES `activo` (`id`),
  CONSTRAINT `Detalle_movimiento_id_agente_id_bd4a6759_fk_Agente_id` FOREIGN KEY (`id_agente_id`) REFERENCES `agente` (`id`),
  CONSTRAINT `Detalle_movimiento_id_area_id_b2e679b8_fk_Area_id` FOREIGN KEY (`id_area_id`) REFERENCES `area` (`id`),
  CONSTRAINT `Detalle_movimiento_id_movimiento_id_1f253240_fk_Movimiento_id` FOREIGN KEY (`id_movimiento_id`) REFERENCES `movimiento` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_movimiento`
--

LOCK TABLES `detalle_movimiento` WRITE;
/*!40000 ALTER TABLE `detalle_movimiento` DISABLE KEYS */;
INSERT INTO `detalle_movimiento` VALUES (1,'Asignación de equipo','T1-CAL-12345','Se entrega en perfectas condiciones',1,2,2,1);
/*!40000 ALTER TABLE `detalle_movimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(13,'app','activo'),(11,'app','administrador'),(12,'app','agente'),(7,'app','area'),(14,'app','detalle_movimiento'),(8,'app','marca'),(9,'app','movimiento'),(15,'app','operador'),(10,'app','terminal'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-27 22:57:28.073701'),(2,'auth','0001_initial','2025-04-27 22:57:28.791530'),(3,'admin','0001_initial','2025-04-27 22:57:28.953458'),(4,'admin','0002_logentry_remove_auto_add','2025-04-27 22:57:28.962355'),(5,'admin','0003_logentry_add_action_flag_choices','2025-04-27 22:57:28.980170'),(6,'app','0001_initial','2025-04-27 22:57:30.112302'),(7,'app','0002_activo_mantenimiento_and_more','2025-04-27 22:57:30.189095'),(8,'app','0003_remove_detalle_movimiento_mantenimiento','2025-04-27 22:57:30.215160'),(9,'contenttypes','0002_remove_content_type_name','2025-04-27 22:57:30.324236'),(10,'auth','0002_alter_permission_name_max_length','2025-04-27 22:57:30.410999'),(11,'auth','0003_alter_user_email_max_length','2025-04-27 22:57:30.467733'),(12,'auth','0004_alter_user_username_opts','2025-04-27 22:57:30.482684'),(13,'auth','0005_alter_user_last_login_null','2025-04-27 22:57:30.571828'),(14,'auth','0006_require_contenttypes_0002','2025-04-27 22:57:30.575091'),(15,'auth','0007_alter_validators_add_error_messages','2025-04-27 22:57:30.585908'),(16,'auth','0008_alter_user_username_max_length','2025-04-27 22:57:30.675809'),(17,'auth','0009_alter_user_last_name_max_length','2025-04-27 22:57:30.784910'),(18,'auth','0010_alter_group_name_max_length','2025-04-27 22:57:30.806214'),(19,'auth','0011_update_proxy_permissions','2025-04-27 22:57:30.826772'),(20,'auth','0012_alter_user_first_name_max_length','2025-04-27 22:57:30.913280'),(21,'sessions','0001_initial','2025-04-27 22:57:30.953958'),(22,'app','0004_movimiento_responsable_content_type_and_more','2025-04-27 22:58:24.676581');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('iawmda9aluuypaaqnjg39owvgzpi5863','.eJxVjEEOwiAQRe_C2hBgVAaX7nuGZmAGqRpISrsy3l2bdKHb_977LzXSupRx7TKPE6uLsurwu0VKD6kb4DvVW9Op1WWeot4UvdOuh8byvO7u30GhXr41svdgPVI2IVl0krIkR5yPHgJghEDiBBx7AmNPJIImEJkzYrQBRb0_64k4Dw:1u9Fdu:xhmtDXg5A1OmXRIj3ELLEMIv9rh3UZc040MM3yW4Z8o','2025-05-11 22:58:54.457346'),('yuwpv7lssz66ns52pqneilrhpa3nisx1','.eJxVjEEOwiAQRe_C2hBgVAaX7nuGZmAGqRpISrsy3l2bdKHb_977LzXSupRx7TKPE6uLsurwu0VKD6kb4DvVW9Op1WWeot4UvdOuh8byvO7u30GhXr41svdgPVI2IVl0krIkR5yPHgJghEDiBBx7AmNPJIImEJkzYrQBRb0_64k4Dw:1u9qit:OcOGnWT3witPWTDSWsSWTiokxaE7wD-WAXOjutrgBC4','2025-05-13 14:34:31.618298');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marca`
--

DROP TABLE IF EXISTS `marca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marca` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `marca` varchar(50) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marca` (`marca`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marca`
--

LOCK TABLES `marca` WRITE;
/*!40000 ALTER TABLE `marca` DISABLE KEYS */;
INSERT INTO `marca` VALUES (1,'HP',1),(2,'Lenovo',1),(3,'Dell',1),(4,'Logitech',1);
/*!40000 ALTER TABLE `marca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimiento`
--

DROP TABLE IF EXISTS `movimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimiento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_mov` datetime(6) NOT NULL,
  `tipo_mov` varchar(50) NOT NULL,
  `id_terminal_id` bigint NOT NULL,
  `responsable_content_type_id` int DEFAULT NULL,
  `responsable_object_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Movimiento_id_terminal_id_2e28f0a8_fk_Terminal_id` (`id_terminal_id`),
  KEY `Movimiento_responsable_content__a3156c98_fk_django_co` (`responsable_content_type_id`),
  CONSTRAINT `Movimiento_id_terminal_id_2e28f0a8_fk_Terminal_id` FOREIGN KEY (`id_terminal_id`) REFERENCES `terminal` (`id`),
  CONSTRAINT `Movimiento_responsable_content__a3156c98_fk_django_co` FOREIGN KEY (`responsable_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `movimiento_chk_1` CHECK ((`responsable_object_id` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimiento`
--

LOCK TABLES `movimiento` WRITE;
/*!40000 ALTER TABLE `movimiento` DISABLE KEYS */;
INSERT INTO `movimiento` VALUES (1,'2025-04-29 14:35:53.638061','Asignación',2,4,1);
/*!40000 ALTER TABLE `movimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operador`
--

DROP TABLE IF EXISTS `operador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operador` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `tipo_documento` varchar(3) NOT NULL,
  `numero_documento` int unsigned NOT NULL,
  `telefono` int unsigned NOT NULL,
  `contrasena` varchar(128) NOT NULL,
  `conf_contrasena` varchar(128) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_documento` (`numero_documento`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `Operador_user_id_17453727_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `operador_chk_1` CHECK ((`numero_documento` >= 0)),
  CONSTRAINT `operador_chk_2` CHECK ((`telefono` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operador`
--

LOCK TABLES `operador` WRITE;
/*!40000 ALTER TABLE `operador` DISABLE KEYS */;
/*!40000 ALTER TABLE `operador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `terminal`
--

DROP TABLE IF EXISTS `terminal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `terminal` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `terminal` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `terminal`
--

LOCK TABLES `terminal` WRITE;
/*!40000 ALTER TABLE `terminal` DISABLE KEYS */;
INSERT INTO `terminal` VALUES (1,'T1 - (BOG)','HUB Logístico','Km 1.5, Vía Parcelas, Cota',1),(2,'T1 - (BOG)','Terminal Calle13','Cra68d#13',1);
/*!40000 ALTER TABLE `terminal` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-29 14:36:44
