package main

import (
	"fmt"
	"io/ioutil"
	"net/http"

	notescontrollers "note-service/controllers/notes"
	usercontrollers "note-service/controllers/user"
	notesrepo "note-service/repository/notes"
	userrepo "note-service/repository/user"

	. "note-service/utils/db"
	. "note-service/utils/middleware"
	. "note-service/utils/session"

	"github.com/julienschmidt/httprouter"
	"github.com/rs/cors"
)

func main() {
	data, _ := ioutil.ReadFile("config/default.json")
	logfile, log := SetupLogger(data)
	db := Connect_db(data)

	userRepo := userrepo.NewUserRepo(db, logfile)
	userHandler := usercontrollers.NewBaseHandler(userRepo, logfile)

	noteRepo := notesrepo.NewNotesRepo(db, logfile)
	noteHandler := notescontrollers.NewBaseHandler(noteRepo, logfile)

	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"https://*", "http://*"},
		AllowCredentials: true,
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "PATCH"},
	})

	router := httprouter.New()
	router.ServeFiles("/assets/*filepath", http.Dir("./assets"))

	handler := c.Handler(router)

	// users routes
	router.POST("/api/register", Logger(userHandler.AddUser))
	router.POST("/api/login", Logger(userHandler.LoginCheck))
	router.GET("/api/logout", Logger(userHandler.Logout))
	router.GET("/api/profile", Logger(AuthorizationCheck(userHandler.GetProfile)))

	// notes routes
	router.POST("/api/notes", Logger(noteHandler.GetNotes))
	router.GET("/api/notes", Logger(noteHandler.GetNotes))
	router.GET("/api/notes/:id", Logger(noteHandler.GetDetailNotes))
	router.PUT("/api/notes", Logger(AuthorizationCheck(noteHandler.InsertUpdateNote)))
	router.PATCH("/api/notes", Logger(AuthorizationCheck(noteHandler.InsertUpdateNote)))
	router.DELETE("/api/notes/:id", Logger(AuthorizationCheck(noteHandler.DeleteNote)))

	// analytics routes
	router.POST("/api/notes/count", Logger(AuthorizationCheck(noteHandler.GetNotesCount)))

	log.Infoln("Server running on port :3000")
	err := http.ListenAndServe(":3000", handler)
	if err != nil {
		fmt.Println(err)
	}
}
