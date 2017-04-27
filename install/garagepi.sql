-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 27, 2017 at 12:44 AM
-- Server version: 5.7.17-0ubuntu0.16.04.2
-- PHP Version: 7.0.15-0ubuntu0.16.04.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `garagepi`
--

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `Name` varchar(15) NOT NULL COMMENT 'Name of Bluetooth device',
  `MAC` char(17) NOT NULL DEFAULT '00:00:00:00:00:00' COMMENT 'MAC ADDRESS',
  `Description` varchar(15) DEFAULT NULL COMMENT 'A description to go with device',
  `Created` datetime NOT NULL COMMENT 'DateTime it was created',
  `Edited` datetime NOT NULL COMMENT 'DateTime it was last edited',
  `PIN` int(4) NOT NULL DEFAULT '0' COMMENT 'PIN code to connect to the device'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Saved BLE Devices';

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
