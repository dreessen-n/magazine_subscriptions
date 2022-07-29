-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema magazine_subscriptions
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `magazine_subscriptions` ;

-- -----------------------------------------------------
-- Schema magazine_subscriptions
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `magazine_subscriptions` DEFAULT CHARACTER SET utf8 ;
USE `magazine_subscriptions` ;

-- -----------------------------------------------------
-- Table `magazine_subscriptions`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `magazine_subscriptions`.`users` ;

CREATE TABLE IF NOT EXISTS `magazine_subscriptions`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(50) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `magazine_subscriptions`.`magazines`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `magazine_subscriptions`.`magazines` ;

CREATE TABLE IF NOT EXISTS `magazine_subscriptions`.`magazines` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `description` TEXT(300) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_recipes_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_recipes_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `magazine_subscriptions`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `magazine_subscriptions`.`subscriptions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `magazine_subscriptions`.`subscriptions` ;

CREATE TABLE IF NOT EXISTS `magazine_subscriptions`.`subscriptions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `magazine_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_favorited_reviews_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_favorited_reviews_reviews1_idx` (`magazine_id` ASC) VISIBLE,
  CONSTRAINT `fk_favorited_reviews_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `magazine_subscriptions`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_favorited_reviews_reviews1`
    FOREIGN KEY (`magazine_id`)
    REFERENCES `magazine_subscriptions`.`magazines` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
