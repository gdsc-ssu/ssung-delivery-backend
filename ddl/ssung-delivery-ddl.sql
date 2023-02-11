-- Active: 1645778042492@@127.0.0.1@3306@ssung

create table senders
(
    `id` INTEGER auto_increment PRIMARY KEY comment '유저 ID',
    `name` VARCHAR(255) UNIQUE not null comment '이름',
    `password` VARCHAR(255) not null comment '비밀번호',
    `address` VARCHAR(200) not null comment '주소',
    `phone_number` VARCHAR(255) not null comment '전화번호',
    `created_at` TIMESTAMP default current_timestamp not null comment '생성시간',
    `modified_at` TIMESTAMP default current_timestamp not null on update current_timestamp comment '변경시간'
);


create table crews
(
    `id` BIGINT auto_increment PRIMARY KEY comment '기사 ID',
    `crew_name` VARCHAR(255) UNIQUE not null comment '기사 이름',
    `password` VARCHAR(255) not null comment '기사 비밀번호',
    `area` VARCHAR(255) not null comment '담당 구역',
    `phone_number` VARCHAR(255) not null comment '기사 전화번호'
    `created_at` TIMESTAMP default current_timestamp not null comment '생성시간',
    `modified_at`TIMESTAMP default current_timestamp not null on update current_timestamp comment '변경시간',
);


create table shippment_histories
(
    `created_at`   TIMESTAMP default current_timestamp not null comment '생성시간',
    `history_id`   BIGINT auto_incrementprimary key, 
    `content_id`   BIGINT not null,
    `location` VARCHAR(255) not null,
    `history_time` TIMESTAMP not null
);


CREATE TABLE `contents` (
	`id`	BIGINT(255) AUTO_INCREMENT primary KEY COMMENT '내용물 ID',
	`is_fragile`	BOOLEAN	NULL	COMMENT '취급주의',
	`is_express`	BOOLEAN	NULL	COMMENT '특송여부',
	`content`	VARCHAR(255)	NOT NULL	COMMENT '택배 내용',
	`type`	VARCHAR(3)	NOT NULL	COMMENT '어떤 물건인지'
);


CREATE TABLE `shipments` (
	`id` BIGINT	NOT NULL auto_increment PRIMARY KEY,
	`content_id`	BIGINT(255) NOT NULL,
    FOREIGN KEY (content_id) REFERENCES contents(id) on update CASCADE on delete CASCADE,
	`crew_id`	INT(255)	NOT NULL	COMMENT '택배 기사',
    FOREIGN KEY (crew_id) REFERENCES crews(id) on update CASCADE on delete CASCADE,
	`sender_id`	INT(255)	NOT NULL	COMMENT '보내는 사람',
    FOREIGN KEY (sender_id) REFERENCES senders(id) on update CASCADE on delete CASCADE,
	`status`	VARCHAR(255) DEFAULT 'ready'	COMMENT '출고 여부',
	`location`	VARCHAR(255)	NULL	COMMENT '택배 현 위치',
	`shipment_detail`	VARCHAR(255)	NULL	COMMENT '배송 시 주의사항',
	`destination`	VARCHAR(255)	NOT NULL	COMMENT '배송 도착지',
	`receiver_name`	VARCHAR(255)	NULL	COMMENT '수신자 이름',
	`receiver_phone_numnber`	VARCHAR(255)	NULL	COMMENT '수신자 연락처',
    `shipment_start_date`	TIMESTAMP	NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`shipment_end_date`	TIMESTAMP	NULL	COMMENT '배송 종료일'
);
