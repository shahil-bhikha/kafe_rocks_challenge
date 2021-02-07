create database kafe_rocks;
create table if not exists kafe_rocks.metroboard (
    `id` bigint not null auto_increment,
    `board_name` varchar(255) not null,
    `category` varchar(255),
    `author` varchar(255),
    `content` text,
    `votes` int,
    `date` datetime,
    `comments` text,
    `created_at` datetime not null,
    `updated_at` datetime not null,
    
    primary key (id)
);