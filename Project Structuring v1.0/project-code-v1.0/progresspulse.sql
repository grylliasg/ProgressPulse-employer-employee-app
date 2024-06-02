-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 01 Ιουν 2024 στις 17:45:13
-- Έκδοση διακομιστή: 10.4.32-MariaDB
-- Έκδοση PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `progresspulse`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `leaverequests`
--

CREATE TABLE `leaverequests` (
  `LeaveRequestID` int(11) NOT NULL,
  `LeaveStartDate` date NOT NULL,
  `LeaveEndDate` date NOT NULL,
  `LeaveStatus` enum('Υπο εξέταση','Αποδεκτή','Απορριμμένη') NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `LeaveName` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `leaverequests`
--

INSERT INTO `leaverequests` (`LeaveRequestID`, `LeaveStartDate`, `LeaveEndDate`, `LeaveStatus`, `UserID`, `LeaveName`) VALUES
(12, '2024-06-01', '2024-06-13', 'Αποδεκτή', 10, 'LeaveRequest1'),
(13, '2024-07-09', '2024-07-18', 'Υπο εξέταση', 11, 'For Holidays');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `meetings`
--

CREATE TABLE `meetings` (
  `MeetingID` int(11) NOT NULL,
  `MeetingDateTime` datetime NOT NULL,
  `MeetingAgenda` text DEFAULT NULL,
  `TeamID` int(11) DEFAULT NULL,
  `MeetingName` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `meetings`
--

INSERT INTO `meetings` (`MeetingID`, `MeetingDateTime`, `MeetingAgenda`, `TeamID`, `MeetingName`) VALUES
(17, '2024-06-04 00:00:00', 'Important Meeting', 3, 'Meeting1');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `projects`
--

CREATE TABLE `projects` (
  `ProjectID` int(11) NOT NULL,
  `ProjectName` varchar(255) NOT NULL,
  `ProjectDescription` text DEFAULT NULL,
  `ProjectStatus` enum('Σε εξέλιξη','Ολοκληρωμένο') NOT NULL,
  `TeamID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `projects`
--

INSERT INTO `projects` (`ProjectID`, `ProjectName`, `ProjectDescription`, `ProjectStatus`, `TeamID`) VALUES
(17, 'Project1', 'Important Project', 'Σε εξέλιξη', 3),
(19, 'Project2', 'SQL Project', 'Σε εξέλιξη', 3);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `tasks`
--

CREATE TABLE `tasks` (
  `TaskID` int(11) NOT NULL,
  `TaskName` varchar(255) DEFAULT NULL,
  `TaskDescription` text NOT NULL,
  `TaskDeadline` date NOT NULL,
  `TaskStatus` enum('Completed','Uncompleted') NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `ProjectID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `tasks`
--

INSERT INTO `tasks` (`TaskID`, `TaskName`, `TaskDescription`, `TaskDeadline`, `TaskStatus`, `UserID`, `ProjectID`) VALUES
(21, 'Task1', 'Important Task', '2024-06-01', 'Completed', 10, 17),
(22, 'SQL Task', 'Until Monday', '2024-06-10', 'Completed', 11, 19);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `teams`
--

CREATE TABLE `teams` (
  `TeamID` int(11) NOT NULL,
  `TeamName` varchar(255) NOT NULL,
  `TeamDescription` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `teams`
--

INSERT INTO `teams` (`TeamID`, `TeamName`, `TeamDescription`) VALUES
(3, 'Team1', 'First Team'),
(4, 'Team2', 'Second team');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `users`
--

CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `UserRole` enum('employer','employee') NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `Team` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `users`
--

INSERT INTO `users` (`UserID`, `Username`, `Password`, `UserRole`, `name`, `Team`) VALUES
(8, 'af1', '1', 'employer', 'Giorgos', 3),
(9, 'af2', '2', 'employer', 'Nikos', 4),
(10, 'erg1', '1', 'employee', 'Simos', 3),
(11, 'erg2', '1', 'employee', 'Ioanna', 3),
(12, 'erg3', '2', 'employee', 'Petros', 4),
(13, 'erg4', '2', 'employee', 'Dimitris', 4);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `withdrawals`
--

CREATE TABLE `withdrawals` (
  `UserID` int(11) DEFAULT NULL,
  `Status` enum('Εγκεκριμένη','Απορριμμένη','Υπο Εξέταση') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `leaverequests`
--
ALTER TABLE `leaverequests`
  ADD PRIMARY KEY (`LeaveRequestID`),
  ADD KEY `UserID` (`UserID`);

--
-- Ευρετήρια για πίνακα `meetings`
--
ALTER TABLE `meetings`
  ADD PRIMARY KEY (`MeetingID`),
  ADD KEY `TeamID` (`TeamID`);

--
-- Ευρετήρια για πίνακα `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`ProjectID`),
  ADD KEY `TeamID` (`TeamID`);

--
-- Ευρετήρια για πίνακα `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`TaskID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `ProjectID` (`ProjectID`);

--
-- Ευρετήρια για πίνακα `teams`
--
ALTER TABLE `teams`
  ADD PRIMARY KEY (`TeamID`);

--
-- Ευρετήρια για πίνακα `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`),
  ADD KEY `fk_users_team` (`Team`);

--
-- Ευρετήρια για πίνακα `withdrawals`
--
ALTER TABLE `withdrawals`
  ADD KEY `UserID` (`UserID`);

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `leaverequests`
--
ALTER TABLE `leaverequests`
  MODIFY `LeaveRequestID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT για πίνακα `meetings`
--
ALTER TABLE `meetings`
  MODIFY `MeetingID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT για πίνακα `projects`
--
ALTER TABLE `projects`
  MODIFY `ProjectID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT για πίνακα `tasks`
--
ALTER TABLE `tasks`
  MODIFY `TaskID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT για πίνακα `teams`
--
ALTER TABLE `teams`
  MODIFY `TeamID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT για πίνακα `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `leaverequests`
--
ALTER TABLE `leaverequests`
  ADD CONSTRAINT `fk_leaverequests_user` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`);

--
-- Περιορισμοί για πίνακα `meetings`
--
ALTER TABLE `meetings`
  ADD CONSTRAINT `fk_meetings_team` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`TeamID`);

--
-- Περιορισμοί για πίνακα `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `fk_projects_team` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`TeamID`);

--
-- Περιορισμοί για πίνακα `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `fk_tasks_project` FOREIGN KEY (`ProjectID`) REFERENCES `projects` (`ProjectID`),
  ADD CONSTRAINT `fk_tasks_user` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`);

--
-- Περιορισμοί για πίνακα `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_team` FOREIGN KEY (`Team`) REFERENCES `teams` (`TeamID`);

--
-- Περιορισμοί για πίνακα `withdrawals`
--
ALTER TABLE `withdrawals`
  ADD CONSTRAINT `withdrawals_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
