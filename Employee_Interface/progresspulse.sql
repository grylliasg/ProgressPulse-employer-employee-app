-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: localhost:3307
-- Χρόνος δημιουργίας: 22 Μάη 2024 στις 19:30:27
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
(1, '2024-07-01', '2024-07-31', 'Απορριμμένη', 1, 'Summer'),
(3, '2024-08-06', '2024-09-10', 'Υπο εξέταση', 1, 'baby birth'),
(5, '2024-05-22', '2024-05-22', 'Υπο εξέταση', 1, '');

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
(1, '2024-08-31 00:00:00', 'textttt', 1, 'Meeting 1');

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
(1, 'Project 1', 'Proj Descr 1', 'Ολοκληρωμένο', 1);

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
(1, 'Task 1', 'Descrip Task 1', '2024-08-21', 'Completed', 1, 1),
(2, 'Task 2', 'Descr Task 2', '2024-08-08', 'Uncompleted', 1, 1),
(3, 'Task 3', 'Des Task 3', '2024-06-12', 'Uncompleted', 1, 1);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `teamchatmessages`
--

CREATE TABLE `teamchatmessages` (
  `MessageID` int(11) NOT NULL,
  `MessageText` text NOT NULL,
  `MessageDateTime` datetime NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `TeamID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `teammembers`
--

CREATE TABLE `teammembers` (
  `TeamMemberID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `TeamID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `teams`
--

CREATE TABLE `teams` (
  `TeamID` int(11) NOT NULL,
  `TeamName` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `teams`
--

INSERT INTO `teams` (`TeamID`, `TeamName`) VALUES
(1, 'Team1 ');

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
(1, 'grylliasg', 'sim', 'employee', 'Simos Yeah', 1),
(2, 'io', 'i', 'employee', 'Ioanna Yeah', NULL),
(3, 'petergiann', 'pet', 'employee', 'Petros Yeah', NULL);

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
-- Ευρετήρια για πίνακα `teamchatmessages`
--
ALTER TABLE `teamchatmessages`
  ADD PRIMARY KEY (`MessageID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `TeamID` (`TeamID`);

--
-- Ευρετήρια για πίνακα `teammembers`
--
ALTER TABLE `teammembers`
  ADD PRIMARY KEY (`TeamMemberID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `TeamID` (`TeamID`);

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
  ADD KEY `Team` (`Team`);

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `leaverequests`
--
ALTER TABLE `leaverequests`
  MODIFY `LeaveRequestID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT για πίνακα `meetings`
--
ALTER TABLE `meetings`
  MODIFY `MeetingID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `projects`
--
ALTER TABLE `projects`
  MODIFY `ProjectID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `tasks`
--
ALTER TABLE `tasks`
  MODIFY `TaskID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT για πίνακα `teamchatmessages`
--
ALTER TABLE `teamchatmessages`
  MODIFY `MessageID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `teammembers`
--
ALTER TABLE `teammembers`
  MODIFY `TeamMemberID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `teams`
--
ALTER TABLE `teams`
  MODIFY `TeamID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `leaverequests`
--
ALTER TABLE `leaverequests`
  ADD CONSTRAINT `leaverequests_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`);

--
-- Περιορισμοί για πίνακα `meetings`
--
ALTER TABLE `meetings`
  ADD CONSTRAINT `meetings_ibfk_1` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`TeamID`);

--
-- Περιορισμοί για πίνακα `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`TeamID`);

--
-- Περιορισμοί για πίνακα `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  ADD CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`ProjectID`) REFERENCES `projects` (`ProjectID`);

--
-- Περιορισμοί για πίνακα `teamchatmessages`
--
ALTER TABLE `teamchatmessages`
  ADD CONSTRAINT `teamchatmessages_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  ADD CONSTRAINT `teamchatmessages_ibfk_2` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`TeamID`);

--
-- Περιορισμοί για πίνακα `teammembers`
--
ALTER TABLE `teammembers`
  ADD CONSTRAINT `teammembers_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  ADD CONSTRAINT `teammembers_ibfk_2` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`TeamID`);

--
-- Περιορισμοί για πίνακα `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`Team`) REFERENCES `teams` (`TeamID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
