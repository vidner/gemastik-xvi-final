package usercontrollers

import (
	"encoding/json"
	"fmt"
	"net/http"
	models "note-service/models/user"
	. "note-service/utils/helper"
	session "note-service/utils/session"
	"reflect"

	"github.com/julienschmidt/httprouter"
	"github.com/sirupsen/logrus"
)

type BaseHandler struct {
	userRepo models.UserRepository
	log      *logrus.Logger
}

func NewBaseHandler(userRepo models.UserRepository, log *logrus.Logger) *BaseHandler {
	return &BaseHandler{
		userRepo: userRepo,
		log:      log,
	}
}

func (h *BaseHandler) GetProfile(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	var user *models.User
	var err error

	claims, resp_code := session.GetData(r)
	if resp_code != 200 {
		w.WriteHeader(resp_code)
		return
	}

	user, err = h.userRepo.GetProfile(claims.Id)

	if err != nil {
		h.log.Errorln(err.Error())
	}
	SendJSONResp(w, user)
}

func (h *BaseHandler) Logout(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	claims, resp_code := session.GetData(r)
	if resp_code != 200 {
		w.WriteHeader(resp_code)
		return
	}
	session.RemoveToken(claims.Id)
	http.SetCookie(w, &http.Cookie{
		Name:   "token",
		Value:  "",
		MaxAge: -1,
	})
	w.WriteHeader(http.StatusOK)
}

func (h *BaseHandler) LoginCheck(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	var raw map[string]interface{}
	var resp string
	if r.Header.Get("Content-Type") == "application/json" {
		decoder := json.NewDecoder(r.Body)
		userModel := models.User{}
		err := decoder.Decode(&userModel)
		if err != nil {
			h.log.Errorln(err.Error())
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		userData, err := h.userRepo.LoginCheck(userModel.Email, userModel.Password)

		if err != nil || reflect.DeepEqual(userData, (models.User{})) {
			resp = `{"success":false,"message":"User Not Found"}`
		} else {
			token, exp, err := session.GenerateToken(userData.Id, userData.Username)
			if err != nil {
				h.log.Errorln(err.Error())
				resp = `{"success":false,"message":"User Not Found"}`
			} else {
				http.SetCookie(w, &http.Cookie{
					Name:     "token",
					Value:    token,
					Expires:  exp,
					HttpOnly: true,
					Path:     "/",
				})
				resp = fmt.Sprintf(`{"success":true,"message":"Access Granted","token":"%s"}`, token)
			}
		}
		_ = json.Unmarshal([]byte(resp), &raw)
		SendJSONResp(w, raw)
	} else {
		w.WriteHeader(http.StatusBadRequest)
	}
}

func (h *BaseHandler) AddUser(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	if r.Header.Get("Content-Type") == "application/json" {
		decoder := json.NewDecoder(r.Body)
		userModel := models.User{}
		err := decoder.Decode(&userModel)
		if err != nil {
			h.log.Errorln(err.Error())
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		result := h.userRepo.AddUser(userModel)
		if result {
			w.WriteHeader(http.StatusCreated)
			return
		}
		w.WriteHeader(http.StatusInternalServerError)
	} else {
		w.WriteHeader(http.StatusBadRequest)
	}
}
