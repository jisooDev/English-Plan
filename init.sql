CREATE DATABASE IF NOT EXISTS oknumber_english_plan;
USE oknumber_english_plan;


CREATE TABLE `users` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `uid` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
  `name` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
  `email` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 DEFAULT 'user',
  `active` tinyint(1) DEFAULT '1',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;


CREATE TABLE `user_packages` (
  `record_id` int(100) NOT NULL AUTO_INCREMENT,
  `user_id` int(100) NOT NULL,
  `package_id` int(100) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `active` int(1) DEFAULT '1',
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


CREATE TABLE `exam_config` (
  `practice_id` int(11) NOT NULL,
  `practice_merge` varchar(255) DEFAULT NULL,
  `practice_type` varchar(255) DEFAULT NULL,
  `practice_name` varchar(255) DEFAULT NULL,
  `timer` int(11) DEFAULT NULL,
  `limited_time` tinyint(1) DEFAULT '0',
  `difficulty` varchar(255) DEFAULT NULL,
  `number_of_questions` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`practice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `exam_config` (`practice_id`, `practice_merge`, `practice_type`, `practice_name`, `timer`, `limited_time`, `difficulty`, `number_of_questions`) VALUES
(1, 'listening', 'write_down_what_you_hear', 'Write down what you hear', 30, 1, 'easy', 1),
(2, 'listening', 'write_down_what_you_hear', 'Write down what you hear', 30, 1, 'medium', 1),
(3, 'listening', 'write_down_what_you_hear', 'Write down what you hear', 30, 1, 'difficult', 1),
(4, 'listening', 'listen_select_real_eng_word', 'Choose Real English Words Only', 120, 1, 'easy', 1),
(5, 'listening', 'listen_select_real_eng_word', 'Choose Real English Words Only', 120, 1, 'medium', 1),
(6, 'listening', 'listen_select_real_eng_word', 'Choose Real English Words Only', 120, 1, 'difficult', 1),
(7, 'listening', 'interactive_conversation', 'Interactive Conversation', 480, 1, 'easy', 1),
(8, 'listening', 'interactive_conversation', 'Interactive Conversation', 480, 1, 'medium', 1),
(9, 'listening', 'interactive_conversation', 'Interactive Conversation', 480, 1, 'difficult', 1),
(10, 'reading', 'reading_select_real_eng_word', 'Choose Real English Words Only', 120, 1, 'easy', 1),
(11, 'reading', 'reading_select_real_eng_word', 'Choose Real English Words Only', 120, 1, 'medium', 1),
(12, 'reading', 'reading_select_real_eng_word', 'Choose Real English Words Only', 120, 1, 'difficult', 1),
(13, 'reading', 'reading', 'Interactive Reading : Read the following passage and choose the right answer', 480, 1, 'easy', 1),
(14, 'reading', 'reading', 'Interactive Reading : Read the following passage and choose the right answer', 480, 1, 'medium', 1),
(15, 'reading', 'reading', 'Interactive Reading : Read the following passage and choose the right answer', 480, 1, 'difficult', 1),
(16, 'reading', 'matching', 'Match the right information with the right paragraph', 0, 0, 'easy', 1),
(17, 'reading', 'matching', 'Match the right information with the right paragraph', 0, 0, 'medium', 1),
(18, 'reading', 'matching', 'Match the right information with the right paragraph', 0, 0, 'difficult', 1),
(19, 'readandwrite', 'describe_a_photo', 'Write at least one sentence about the following photo', 60, 1, 'easy', 1),
(20, 'readandwrite', 'describe_a_photo', 'Write at least one sentence about the following photo', 60, 1, 'medium', 1),
(21, 'readandwrite', 'describe_a_photo', 'Write at least one sentence about the following photo', 60, 1, 'difficult', 1),
(22, 'readandwrite', 'short_answer', 'Write at least 50 words on the following topic', 300, 1, 'easy', 1),
(23, 'readandwrite', 'short_answer', 'Write at least 50 words on the following topic', 300, 1, 'medium', 1),
(24, 'readandwrite', 'short_answer', 'Write at least 50 words on the following topic', 300, 1, 'difficult', 1),
(25, 'readandwrite', 'fill_in_blank', 'Fill in The Blank', 180, 1, 'easy', 1),
(26, 'readandwrite', 'fill_in_blank', 'Fill in The Blank', 180, 1, 'medium', 1),
(27, 'readandwrite', 'fill_in_blank', 'Fill in The Blank', 180, 1, 'difficult', 1),
(28, 'talking', 'read_aloud', 'Read the text within 20 seconds', 30, 1, 'easy', 1),
(29, 'talking', 'read_aloud', 'Read the text within 20 seconds', 30, 1, 'medium', 1),
(30, 'talking', 'read_aloud', 'Read the text within 20 seconds', 30, 1, 'difficult', 1);



CREATE TABLE `listening_interactive_conversation` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `audio` longtext,
  `json_data` longtext,
  `difficulty` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `listening_select_words` (
  `id` varchar(255) NOT NULL,
  `answer` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `answer_atob` varchar(255) DEFAULT NULL,
  `data` longtext,
  `difficulty` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `listening_write_down` (
  `id` varchar(255) NOT NULL,
  `difficulty` varchar(255) DEFAULT NULL,
  `data` longtext,
  `answer` longtext,
  `answer_atob` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `readandwrite_describe_photo` (
  `id` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer_atob` longtext CHARACTER SET utf8mb4,
  `difficulty` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `readandwrite_fill_blank` (
  `id` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 NOT NULL,
  `data_atob` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer_atob` longtext CHARACTER SET utf8mb4,
  `difficulty` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `readandwrite_short_answer` (
  `id` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer_atob` longtext CHARACTER SET utf8mb4,
  `difficulty` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `reading_matching` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `json_data` longtext,
  `json_option` longtext,
  `difficulty` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `reading_reading` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `json_data` longtext,
  `difficulty` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `reading_select_words` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `answer` varchar(255) DEFAULT NULL,
  `answer_atob` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `difficulty` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `talking_read_aloud` (
  `id` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer` longtext CHARACTER SET utf8mb4 NOT NULL,
  `answer_atob` longtext NOT NULL,
  `audio` longtext CHARACTER SET utf8mb4 NOT NULL,
  `difficulty` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;