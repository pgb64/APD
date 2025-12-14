-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`DIM_Vivienda`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DIM_Vivienda` (
  `SK_vivienda` INT NOT NULL AUTO_INCREMENT,
  `ID_Vivienda` VARCHAR(20) NULL,
  `Superficie` INT NULL,
  `Plazas` INT NULL,
  `habitaciones` INT NULL,
  PRIMARY KEY (`SK_vivienda`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DIM_Ubicacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DIM_Ubicacion` (
  `SK_Ubicacion` INT NOT NULL AUTO_INCREMENT,
  `Calle` VARCHAR(150) NULL,
  `Escalera` VARCHAR(10) NULL,
  `Planta` VARCHAR(10) NULL,
  `Puerta` VARCHAR(10) NULL,
  `CP` VARCHAR(10) NULL,
  `Num_Municipio` VARCHAR(10) NULL,
  `Municipio` VARCHAR(100) NULL,
  `Provincia` VARCHAR(100) NULL,
  `Latitud` DECIMAL(14,12) NULL,
  `Longitud` DECIMAL(14,12) NULL,
  PRIMARY KEY (`SK_Ubicacion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DIM_Tiempo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DIM_Tiempo` (
  `SK_Tiempo` INT NOT NULL AUTO_INCREMENT,
  `Fecha` DATE NULL,
  `Dia` INT NULL,
  `Mes` INT NULL,
  `Anyo` INT NULL,
  PRIMARY KEY (`SK_Tiempo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Hecho_Alta_Vivienda`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Hecho_Alta_Vivienda` (
  `Existe` INT(1) NULL,
  `SK_Ubicacion` INT NOT NULL,
  `SK_Tiempo` INT NOT NULL,
  `SK_vivienda` INT NOT NULL,
  PRIMARY KEY (`SK_Ubicacion`, `SK_vivienda`, `SK_Tiempo`),
  INDEX `fk_Hecho_Alta_Vivienda_DIM_Ubicación_idx` (`SK_Ubicacion` ASC) VISIBLE,
  INDEX `fk_Hecho_Alta_Vivienda_DIM_Tiempo1_idx` (`SK_Tiempo` ASC) VISIBLE,
  INDEX `fk_Hecho_Alta_Vivienda_DIM_Vivienda1_idx` (`SK_vivienda` ASC) VISIBLE,
  CONSTRAINT `fk_Hecho_Alta_Vivienda_DIM_Ubicación`
    FOREIGN KEY (`SK_Ubicacion`)
    REFERENCES `mydb`.`DIM_Ubicacion` (`SK_Ubicacion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Hecho_Alta_Vivienda_DIM_Tiempo1`
    FOREIGN KEY (`SK_Tiempo`)
    REFERENCES `mydb`.`DIM_Tiempo` (`SK_Tiempo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Hecho_Alta_Vivienda_DIM_Vivienda1`
    FOREIGN KEY (`SK_vivienda`)
    REFERENCES `mydb`.`DIM_Vivienda` (`SK_vivienda`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
