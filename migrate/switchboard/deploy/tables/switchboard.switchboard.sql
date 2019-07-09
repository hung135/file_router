
create table switchboard.switchboard_history (
	id serial not null, 
	project_name varchar(32), 
	incoming_path text, 
	outgoing_path text, 
	file_date timestamp without time zone, 
	file_md5 varchar(32), 
	file_size integer, 
	file_path_extract varchar(32), 
	created_date timestamp without time zone, 
	constraint switchboard_history_pkey primary key (id), 
	constraint switchboard_history_outgoing_path_key unique (outgoing_path)
)

;
ALTER TABLE switchboard.switchboard_history
	OWNER TO operational_dba;