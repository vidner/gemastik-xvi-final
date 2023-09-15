package usermodels

type User struct {
	Id       int    `json:"id" db:"id"`
	Username string `json:"username" db:"username"`
	Password string `json:"password,omitempty" db:"password"`
	Email    string `json:"email" db:"email"`
}

type UserRepository interface {
	LoginCheck(Username string, Password string) (*User, error)
	GetProfile(id int) (*User, error)
	AddUser(user User) bool
}
