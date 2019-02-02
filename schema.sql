drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
    title string not null,
    text string not null,
    voice tinyint not null,
    led tinyint not null,
    created datetime
);
