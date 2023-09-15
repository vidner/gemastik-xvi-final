package notesmodels

type Notes struct {
	Id      int    `json:"id" db:"id"`
	Title   string `json:"title"  db:"title"`
	Author  string `json:"author" db:"author"`
	Date    string `json:"date" db:"date"`
	Content string `json:"content,omitempty" db:"content"`
	Tags    string `json:"tags" db:"tags"`
}

type NotesRepository interface {
	GetNotes() (*[]Notes, error)
	GetNotesByTitle(title string) (*[]Notes, error)
	InsertUpdateNote(note Notes, op int) bool
	GetNotesCount(key string, keyword string) (*int, error)
	DeleteNote(id string, author int) bool
	GetDetailNotes(id string) (*Notes, error)
}
