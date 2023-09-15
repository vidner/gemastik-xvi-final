package session

import (
	"math/rand"
	"net/http"
	"strings"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
	"github.com/julienschmidt/httprouter"
)

var secretKey = make([]byte, 42)
var validSession = make(map[int]bool)

const tokenExpired = 10

type Claims struct {
	Id       int
	Username string
	jwt.StandardClaims
}

func init() {
	rand.Seed(time.Now().UnixNano())
	rand.Read(secretKey)
}

func getToken(r *http.Request) string {
	token := r.Header.Get("Authorization")
	tokenString := strings.TrimPrefix(token, "Bearer ")
	return tokenString
}

func GenerateToken(id int, username string) (string, time.Time, error) {
	expirationTime := time.Now().Add(tokenExpired * time.Minute)
	claims := &Claims{
		Username: username,
		Id:       id,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expirationTime.Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(secretKey)
	if err == nil {
		validSession[id] = true
	}
	return tokenString, expirationTime, err
}

func GetData(r *http.Request) (*Claims, int) {
	claims := &Claims{}
	tokenStr := getToken(r)
	if tokenStr == "" {
		return claims, 401
	}

	tkn, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
		return secretKey, nil
	})

	if err != nil {
		if err == jwt.ErrSignatureInvalid {
			return claims, 400
		}
		return claims, 401
	}

	if tkn.Valid && validSession[claims.Id] {
		return claims, 200
	}
	return claims, 401
}

func AuthorizationCheck(next httprouter.Handle) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
		_, statusCode := GetData(r)
		if statusCode != 200 {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}
		next(w, r, ps)
	}

}

func RemoveToken(id int) {
	delete(validSession, id)
}
