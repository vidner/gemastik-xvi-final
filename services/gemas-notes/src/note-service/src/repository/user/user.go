package userrepo

import (
	"database/sql"
	models "note-service/models/user"

	"github.com/jmoiron/sqlx"
	"github.com/sirupsen/logrus"
)

const getProfileQuery = "SELECT id,username,email FROM User WHERE id=?"
const loginQuery = "SELECT * FROM User WHERE email=? AND password=MD5(?)"
const addUserQuery = "INSERT INTO User(username,password,email) VALUES (?,md5(?),?)"

type UserRepo struct {
	db  *sqlx.DB
	log *logrus.Logger
}

func NewUserRepo(db *sqlx.DB, log *logrus.Logger) *UserRepo {
	return &UserRepo{db: db, log: log}
}

func affected(result sql.Result, r *UserRepo) bool {
	affectedRows, err := result.RowsAffected()
	if err != nil {
		r.log.Errorln(err.Error())
		return false
	}
	if affectedRows > 0 {
		return true
	}
	return false
}

func (r *UserRepo) GetProfile(id int) (*models.User, error) {
	data := models.User{}
	stmt, err := r.db.Preparex(getProfileQuery)
	if err != nil {
		r.log.Errorln(err.Error())
	}
	defer stmt.Close()
	err = stmt.QueryRowx(id).StructScan(&data)
	if err != nil {
		return &data, err
	}
	return &data, nil
}

func (r *UserRepo) LoginCheck(user string, pass string) (*models.User, error) {
	data := models.User{}
	stmt, err := r.db.Preparex(loginQuery)
	if err != nil {
		r.log.Errorln(err.Error())
	}
	defer stmt.Close()
	err = stmt.QueryRowx(user, pass).StructScan(&data)
	if err != nil {
		return &data, err
	}
	return &data, nil
}

func (r *UserRepo) AddUser(user models.User) bool {
	result := r.db.MustExec(addUserQuery, user.Username, user.Password, user.Email)
	return affected(result, r)
}
