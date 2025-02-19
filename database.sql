CREATE TABLE IF NOT EXISTS urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP(0)
);
CREATE TABLE IF NOT EXISTS url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls (id),
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP(0)
);
