package middleware

import (
	"encoding/json"
	"net/http"
	"os"

	"github.com/julienschmidt/httprouter"
	"github.com/sirupsen/logrus"
)

type LogData struct {
	Logfile         string `json:"logfile"`
	TimestampFormat string `json:"timestampformat"`
	Format          string `json:"format"`
}

type LogConfig struct {
	Log LogData `json:"log"`
}

var Logging *logrus.Logger
var StdoutLog *logrus.Logger

func setupStdOutLog(config *LogConfig) {
	StdoutLog = logrus.New()
	StdoutLog.SetFormatter(&logrus.TextFormatter{
		TimestampFormat: config.Log.TimestampFormat,
		FullTimestamp:   true,
	})
}

func setupLogFile(config *LogConfig) {
	Logging = logrus.New()

	if config.Log.Format == "json" {
		Logging.SetFormatter(&logrus.JSONFormatter{
			TimestampFormat: config.Log.TimestampFormat,
		})
	} else {
		Logging.SetFormatter(&logrus.TextFormatter{
			TimestampFormat: config.Log.TimestampFormat,
		})
	}
	f, err := os.OpenFile(config.Log.Logfile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		Logging.Fatal("Cannot Open Logging Files")
	}
	Logging.SetOutput(f)
}

func SetupLogger(data []byte) (*logrus.Logger, *logrus.Logger) {
	config := LogConfig{}
	_ = json.Unmarshal([]byte(data), &config)
	setupStdOutLog(&config)
	setupLogFile(&config)
	return Logging, StdoutLog
}

func Logger(next httprouter.Handle) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
		Logging.Infof("[ %s ] %s %s %s", r.Header.Get("X-Real-IP"), r.Method, r.URL.Path, r.Header.Get("User-Agent"))
		StdoutLog.Infof("[ %s ] %s %s %s", r.Header.Get("X-Real-IP"), r.Method, r.URL.Path, r.Header.Get("User-Agent"))
		next(w, r, ps)
	}
}
