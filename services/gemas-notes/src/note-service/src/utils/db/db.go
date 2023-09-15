package db

import (
	"encoding/json"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
)

type DBConfig struct {
	Db DBData `json:"db"`
}

type DBData struct {
	DBType string `json:"type"`
	DBHost string `json:"host"`
	DBPort int    `json:"port"`
	User   string `json:"username"`
	Pass   string `json:"password"`
	DBName string `json:"database"`
}

func Connect_db(config []byte) *sqlx.DB {
	data := DBConfig{}
	_ = json.Unmarshal([]byte(config), &data)
	connection_string := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s", data.Db.User, data.Db.Pass, data.Db.DBHost, data.Db.DBPort, data.Db.DBName)

	db, err := sqlx.Open(data.Db.DBType, connection_string)

	if err != nil {
		log.Fatalln(err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatalln(err)
	}
	return db
}
