package helper

import (
	"encoding/json"
	"net/http"
)

func SendJSONResp(w http.ResponseWriter, data interface{}) {
	resp, _ := json.Marshal(data)
	w.Header().Set("Content-Type", "application/json")
	w.Write(resp)
}
