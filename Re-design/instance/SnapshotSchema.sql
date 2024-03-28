CREATE TABLE snapshots (
	id INTEGER NOT NULL, 
	"Detection_img_ref" VARCHAR(100) NOT NULL, 
	"Detection_type" VARCHAR(30) NOT NULL, 
	"Loc" VARCHAR(100) NOT NULL, 
	"Time" DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	"Alert_sentTo" VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("Alert_sentTo") REFERENCES user (username)
)