CREATE TABLE  IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    _user text NOT NULL,
    _pass text NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
    id integer PRIMARY KEY AUTOINCREMENT,
    filename text NOT NULL,
    create_config text NOT NULL
);

CREATE TABLE IF NOT EXISTS actions(
    id integer PRIMARY KEY AUTOINCREMENT,
    task_name text NOT NULL,
    report_name text NOT NULL,
    time_create integer NOT NULL,
    time_action integer NOT NULL,
    format_action text NOT NULL,
    report_conf text NOT NULL
)
