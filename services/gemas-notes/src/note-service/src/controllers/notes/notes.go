package notescontrollers

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	models "note-service/models/notes"
	. "note-service/utils/helper"
	session "note-service/utils/session"
	"strconv"

	"github.com/buger/jsonparser"
	"github.com/julienschmidt/httprouter"
	"github.com/sirupsen/logrus"
)

type BaseHandler struct {
	noteRepo models.NotesRepository
	log      *logrus.Logger
}

func NewBaseHandler(noteRepo models.NotesRepository, log *logrus.Logger) *BaseHandler {
	return &BaseHandler{
		noteRepo: noteRepo,
		log:      log,
	}
}

func (h *BaseHandler) GetNotes(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	var notes *[]models.Notes
	var err error
	if r.Method == "GET" {
		notes, err = h.noteRepo.GetNotes()
	} else if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		body, err := io.ReadAll(r.Body)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		title, err := jsonparser.GetString([]byte(body), "title")
		if err != nil {
			h.log.Errorln(err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		notes, err = h.noteRepo.GetNotesByTitle(title)
		if err != nil {
			h.log.Errorln(err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
	}

	if err != nil {
		h.log.Errorln(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	SendJSONResp(w, notes)
}

func (h *BaseHandler) GetDetailNotes(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	notes, err := h.noteRepo.GetDetailNotes(ps.ByName("id"))
	if err != nil {
		h.log.Errorln(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	SendJSONResp(w, notes)
}

func (h *BaseHandler) DeleteNote(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	claims, respCode := session.GetData(r)
	if respCode != 200 {
		w.WriteHeader(respCode)
		return
	}
	result := h.noteRepo.DeleteNote(ps.ByName("id"), claims.Id)
	if result {
		w.WriteHeader(http.StatusNoContent)
		return
	}
	w.WriteHeader(http.StatusInternalServerError)
}

func (h *BaseHandler) GetNotesCount(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	if r.Header.Get("Content-Type") == "application/json" {
		var raw map[string]int
		var countResp string

		body, err := io.ReadAll(r.Body)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		key, err := jsonparser.GetString([]byte(body), "count_by")
		if err != nil {
			h.log.Errorln(err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		if key != "title" && key != "tags" {
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		keyword, err := jsonparser.GetString([]byte(body), "keyword")
		if err != nil {
			h.log.Errorln(err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		count, err := h.noteRepo.GetNotesCount(key, keyword)
		if err != nil {
			countResp = `{"count":0}`
		} else {
			countResp = fmt.Sprintf(`{"count":%d}`, *count)
		}
		_ = json.Unmarshal([]byte(countResp), &raw)
		SendJSONResp(w, raw)
	}
}

func (h *BaseHandler) InsertUpdateNote(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	claims, respCode := session.GetData(r)
	if respCode != 200 {
		w.WriteHeader(respCode)
		return
	}

	resp := map[string]int{"PUT": 201, "PATCH": 204}
	method := r.Method
	if r.Header.Get("Content-Type") == "application/json" {
		decoder := json.NewDecoder(r.Body)
		noteDetail := models.Notes{}
		err := decoder.Decode(&noteDetail)
		if err != nil {
			h.log.Errorln(err)
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		noteDetail.Author = strconv.Itoa(claims.Id)
		var result bool
		if method == "PUT" {
			result = h.noteRepo.InsertUpdateNote(noteDetail, 1)
		} else if method == "PATCH" {
			result = h.noteRepo.InsertUpdateNote(noteDetail, 2)
		}
		if result {
			w.WriteHeader(resp[method])
			return
		}
		w.WriteHeader(http.StatusInternalServerError)

	} else {
		w.WriteHeader(http.StatusBadRequest)
	}
}
