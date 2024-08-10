CREATE DATABASE  IF NOT EXISTS `bdflask` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bdflask`;

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



DROP TABLE IF EXISTS `albums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `albums` (
  `idAlbum` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(250) DEFAULT NULL,
  `artista` varchar(250) DEFAULT NULL,
  `anio` int DEFAULT NULL,
  `portada` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idAlbum`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `albums`
--

LOCK TABLES `albums` WRITE;
/*!40000 ALTER TABLE `albums` DISABLE KEYS */;
INSERT INTO `albums` VALUES (18,'Uprising','MUSE',2005,NULL),(19,'First band on the moon','The cardinals',1996,NULL),(21,'square rooms','test',1988,'static\\uploads\\upqlogoazul.jpg');
/*!40000 ALTER TABLE `albums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_medicos`
--

DROP TABLE IF EXISTS `tb_medicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_medicos` (
  `id_medico` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `id_roles` int NOT NULL,
  `cedula` varchar(8) NOT NULL,
  `rfc` varchar(11) NOT NULL,
  `contraseña` varchar(45) NOT NULL,
  PRIMARY KEY (`id_medico`),
  UNIQUE KEY `id_medico_UNIQUE` (`id_medico`),
  KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_medicos`
--

LOCK TABLES `tb_medicos` WRITE;
/*!40000 ALTER TABLE `tb_medicos` DISABLE KEYS */;
INSERT INTO `tb_medicos` VALUES (1,'pepe','aguilar',2,'3','sa2d2sa4',''),(2,'baruck','sanchez',4,'1221321','1281321',''),(3,'si','salmonelin@hotmail2',4,'6','2wdsad','2121e'),(4,'lola','martinez@upq',8,'19228183','19291291','contraseña'),(5,'baruck2','elquesea@hotmail',3,'213412','dsada23','sadsadas'),(6,'pikachu','esqere@upq.edu.mx',6,'123921','dsada','memoochoa'),(7,'lola','lola@upq.edu.mx',2,'2131','1238wq','lolo'),(8,'carlos','carlos@upq.edu.mx',3,'214124','dsada232','afsafas'),(9,'armando','hoyos@upq.edu.mx',8,'13282','12e21','popo'),(10,'simon','simonq@upq',2,'13821','wqdqwd','sisis'),(11,'test','test@hotmail.com',3,'123','test','123'),(12,'prueba2','prueba@gmail.com',2,'12312','1234','si');
/*!40000 ALTER TABLE `tb_medicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_pacientes`
--

DROP TABLE IF EXISTS `tb_pacientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_pacientes` (
  `id_paciente` int NOT NULL AUTO_INCREMENT,
  `nombre_med` varchar(45) NOT NULL,
  `paciente` varchar(45) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id_paciente`),
  KEY `nombre_idx` (`nombre_med`),
  CONSTRAINT `nombre` FOREIGN KEY (`nombre_med`) REFERENCES `tb_medicos` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_pacientes`
--

LOCK TABLES `tb_pacientes` WRITE;
/*!40000 ALTER TABLE `tb_pacientes` DISABLE KEYS */;
INSERT INTO `tb_pacientes` VALUES (1,'test','try','2000-10-10'),(2,'test','try','2000-10-10');
/*!40000 ALTER TABLE `tb_pacientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'bdflask'
--

--
-- Dumping routines for database 'bdflask'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-09  0:51:05

