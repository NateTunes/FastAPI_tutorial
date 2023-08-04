create table posts (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	title VARCHAR NOT NULL,
	content VARCHAR NOT NULL,
    published BOOLEAN NOT NULL DEFAULT FALSE,
    ceated_at timestamptz NOT NULL DEFAULT NOW()
);
insert into posts (title, content) values ('title 1', 'content 1');
