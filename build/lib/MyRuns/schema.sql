drop table if exists user_token;
create table user_token (
    id integer primary key autoincrement,
    username text not null,
    user_id integer not null,
    access_token text not null unique,
    cookies text unique
);