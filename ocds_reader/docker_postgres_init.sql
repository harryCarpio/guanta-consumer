CREATE TABLE IF NOT EXISTS public.read_process
(
    id SERIAL PRIMARY KEY,
    exec uuid,
    start time with time zone NOT NULL,
    "end" time with time zone,
    year integer,
    keyword text COLLATE pg_catalog."default",
    pages integer,
    status text COLLATE pg_catalog."default",
    http_status integer,
    host text COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.log_ocds_header
(
    id SERIAL PRIMARY KEY,
    read_process_id bigint NOT NULL,
    read_timestamp timestamp with time zone,
    http_status integer,
    process_id text,
    page integer,
    CONSTRAINT read_process_fk FOREIGN KEY (read_process_id)
        REFERENCES public.read_process (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.log_ocds_detail
(
    id SERIAL PRIMARY KEY,
    read_process_id bigint NOT NULL,
    read_timestamp timestamp with time zone,
    http_status integer,
    process_id text,
    updated boolean NOT NULL ,
    CONSTRAINT read_process_fk FOREIGN KEY (read_process_id)
        REFERENCES public.read_process (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);