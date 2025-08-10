SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `crmdb`
--

-- --------------------------------------------------------

--
-- Структура таблицы `auth_log`
--

CREATE TABLE IF NOT EXISTS `auth_log` (
  `id` int(11) NOT NULL,
  `time_in` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `login` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы documents
--

CREATE TABLE IF NOT EXISTS documents (
  id int(11) NOT NULL,
  title varchar(255) DEFAULT NULL,
  author varchar(255) DEFAULT NULL,
  created timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  created_by int NULL,
  updated timestamp NULL,
  updated_by int NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы document_files
--

CREATE TABLE IF NOT EXISTS document_files (
  id int(11) NOT NULL,
  doc_id int NOT NULL,
  index_num int NOT NULL DEFAULT 0,
  title varchar(255) NOT NULL,
  file_name varchar(255) NOT NULL,
  file_content BINARY NULL,
  content TEXT NULL,
  created timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  created_by int NULL,
  updated timestamp NULL,
  updated_by int NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Структура таблицы file_pages
--

CREATE TABLE IF NOT EXISTS file_pages (
  id int(11) NOT NULL,
  doc_file_id int NOT NULL,
  page_num int NOT NULL DEFAULT 0,
  title varchar(255) DEFAULT NULL,
  file_name varchar(255) DEFAULT NULL,
  file_content BINARY NULL,
  content TEXT NULL,
  created timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  created_by int NULL,
  updated timestamp NULL,
  updated_by int NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  id int(11) NOT NULL PRIMARY_KEY IDENTITY(1,1),
  login varchar(32) NOT NULL,
  passw varchar(32) NOT NULL,
  role enum('user','admin','superadmin') NOT NULL,
  admin int(11) DEFAULT NULL,
  name varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `login` (`login`),
  ADD UNIQUE KEY `exten` (`exten`),

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `auth_log`
--
ALTER TABLE `auth_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `call_history`
--
ALTER TABLE `call_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `call_remind`
--
ALTER TABLE `call_remind`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `clients`
--
ALTER TABLE `clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
