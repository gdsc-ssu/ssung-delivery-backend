create table contents (
  created_at TIMESTAMP default current_timestamp not null comment '생성시간', 
  modified_at TIMESTAMP default current_timestamp not null on update current_timestamp comment '변경시간', 
  content_id BIGINT auto_increment comment '내용물 ID', 
  fragile BOOLEAN null comment '취급주의', 
  express BOOLEAN null comment '특송여부', 
  name VARCHAR(255) not null comment '택배 내용', 
  type VARCHAR(255) not null comment '어떤 물건인지', 

  constraint PK_CONTENTS primary key (content_id)
);

create table users (
  id BIGINT auto_increment PRIMARY KEY comment '유저 ID', 
  user_name VARCHAR(255) UNIQUE not null comment '이름', 
  password VARCHAR(255) not null comment '비밀번호', 
  address VARCHAR(200) not null comment '주소', 
  phone_number VARCHAR(255) not null comment '전화번호', 
  created_at TIMESTAMP default current_timestamp not null comment '생성시간', 
  modified_at TIMESTAMP default current_timestamp not null on update current_timestamp comment '변경시간'
);

create table crews (
  id BIGINT auto_increment PRIMARY KEY comment '기사 ID', 
  crew_name VARCHAR(255) UNIQUE not null comment '기사 이름', 
  password VARCHAR(255) not null comment '기사 비밀번호', 
  area VARCHAR(255) not null comment '담당 구역', 
  phone_number VARCHAR(255) not null comment '기사 전화번호', 
  created_at TIMESTAMP default current_timestamp not null comment '생성시간', 
  modified_at TIMESTAMP default current_timestamp not null on update current_timestamp comment '변경시간'
);

create table shippment_histories (
  created_at TIMESTAMP default current_timestamp not null comment '생성시간', 
  history_id BIGINT auto_increment primary key, 
  content_id BIGINT not null, 
  location VARCHAR(255) not null, 
  history_time TIMESTAMP not null
);

create table shippments (
  created_at TIMESTAMP default current_timestamp not null comment '생성시간', 
  modified_at TIMESTAMP default current_timestamp not null on update current_timestamp comment '변경시간', 
  shippment_id BIGINT auto_increment comment '배송 ID' primary key, 
  content_id BIGINT not null comment '배송물 정보', 
  crew_id BIGINT not null comment '택배 기사', 
  user_id BIGINT not null comment '보내는 사람', 
  shipment_start_date DATE not null comment '배송 시작일', 
  shipment_end_date DATETIME not null comment '배송 종료일', 
  status VARCHAR(255) null comment '출고 여부', 
  location VARCHAR(255) null comment '택배 현 위치', 
  shippment_detail VARCHAR(255) null comment '배송 시 주의사항', 
  destination VARCHAR(255) not null comment '배송 도착지', 
  recever_name VARCHAR(255) null comment '수신자 이름', 
  receiver_phone_numnber VARCHAR(255) null comment '수신자 연락처', 
  
  constraint content_id foreign key (content_id) references contents (content_id), 
  constraint crew_id foreign key (crew_id) references crews (id), 
  constraint user_id foreign key (user_id) references users (id)
);
