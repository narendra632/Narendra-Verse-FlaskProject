-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 16, 2022 at 11:21 AM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 5.6.39

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `narendra-verse`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sr_no` int(50) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone_no` varchar(13) NOT NULL,
  `message` text NOT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sr_no`, `name`, `email`, `phone_no`, `message`, `date`) VALUES
(1, 'trial post', 'trialpost@gmail.com', '1234567890', 'This is trial Post ', '2022-05-07 16:18:38');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_no` int(11) NOT NULL,
  `post_title` text NOT NULL,
  `slug` varchar(30) NOT NULL,
  `post_content` text NOT NULL,
  `post_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `post_img` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_no`, `post_title`, `slug`, `post_content`, `post_date`, `post_img`) VALUES
(1, 'Web Development using Flask_Python', 'first-post', 'Python is a fast, efficient and fun programming language. I started learning and programming python from 1st of January 2022.\r\npython has many implementation across app and web development, AI and machine learning, data analytics, etc.\r\nMany frame-works and modules are used for python programming. One such micro frame-work known as Flask is used extensively for Website Development. In fact this whole website is built using Flask. ', '2022-05-15 18:42:58', 'farm.jpg'),
(2, 'About this Website', 'second-post', 'This website is programmed and designed by me, using a frame-work of Python called Flask. Flask is used extensively to design and program dynamic  web applications. The code written in python-flask works as back-end for the websites. I used Flask to connect my website with database(MySQL) to perform various dynamic functions like fetching, adding and editing data.  All the background images are clicked by me. It took me a lots of efforts and time to build this website as this was my first website building project.', '2022-05-16 11:47:47', 'boy.png'),
(3, 'Modules in Python', 'third-post', 'Python is fun and fast with the help of modules. Modules are basically advanced built function, which you can import in your python program. There are some built-in modules available in your python library but most of them you have to install using PIP. Modules are the spices of your code.', '2022-05-16 12:22:14', 'birdlogo.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sr_no`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sr_no` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `post_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
