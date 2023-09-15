package notesrepo

import (
	"database/sql"
	"fmt"
	models "note-service/models/notes"

	"github.com/jmoiron/sqlx"
	"github.com/sirupsen/logrus"
)

const simpleNote = "SELECT Notes.id, title, User.email as author, date FROM Notes, User WHERE Notes.author=User.id ORDER BY Notes.id DESC"
const simpleNoteFilter = "SELECT Notes.id, title, User.email as author, date FROM Notes, User WHERE Notes.author=User.id AND Notes.title LIKE ?"
const detailNote = "SELECT Notes.id as id, title, User.email as author, date, content, tags FROM Notes, User WHERE Notes.author=User.id AND Notes.id=?"
const insertNote = "INSERT INTO Notes(title,content,author,date,tags) VALUES (?,?,?,DATE_FORMAT(NOW(), '%M %d, %Y'),?)"
const countNote = "SELECT count(*) FROM Notes WHERE %s LIKE '%%%s%%'"
const updateNote = "UPDATE Notes SET title = ?, content = ?, date = DATE_FORMAT(NOW(), '%M %d, %Y') WHERE  author = ? AND id = ?"
const deleteNote = "DELETE FROM Notes WHERE id = ? AND author = ?"

type NotesRepo struct {
	db  *sqlx.DB
	log *logrus.Logger
}

func NewNotesRepo(db *sqlx.DB, log *logrus.Logger) *NotesRepo {
	return &NotesRepo{db: db, log: log}
}

func (r *NotesRepo) GetDetailNotes(id string) (*models.Notes, error) {
	data := models.Notes{}
	stmt, err := r.db.Preparex(detailNote)
	if err != nil {
		r.log.Errorln(err.Error())
	}
	defer stmt.Close()
	err = stmt.QueryRowx(id).StructScan(&data)
	if err != nil {
		r.log.Errorln(err)
	}
	return &data, err
}

func (r *NotesRepo) GetNotes() (*[]models.Notes, error) {
	data := []models.Notes{}
	stmt, err := r.db.Preparex(simpleNote)
	if err != nil {
		r.log.Errorln(err.Error())
	}
	defer stmt.Close()
	err = stmt.Select(&data)
	if err != nil {
		return &data, err
	}
	return &data, nil
}

func (r *NotesRepo) GetNotesByTitle(title string) (*[]models.Notes, error) {
	data := []models.Notes{}
	err := r.db.Select(&data, simpleNoteFilter, title)
	if err != nil {
		r.log.Errorln(err.Error())
	}
	return &data, err
}

func (r *NotesRepo) GetNotesCount(key string, keyword string) (*int, error) {
	var count int
	err := r.db.Get(&count, fmt.Sprintf(countNote, key, keyword))
	if err != nil {
		r.log.Errorln(err.Error())
	}
	return &count, err
}

func (r *NotesRepo) InsertUpdateNote(notes models.Notes, op int) bool {
	var result sql.Result
	if op == 1 {
		result = r.db.MustExec(insertNote, notes.Title, notes.Content, notes.Author, notes.Tags)
	} else {
		result = r.db.MustExec(updateNote, notes.Title, notes.Content, notes.Author, notes.Id)
	}
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

func (r *NotesRepo) DeleteNote(id string, author int) bool {
	result := r.db.MustExec(deleteNote, id, author)
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
