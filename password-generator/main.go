package main

import (
	"crypto/rand"
	"flag"
	"fmt"
	"math/big"
)

const (
	letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	numbers = "0123456789"
	symbols = "!@#$%^&*()-=_+[]{},.<>;':\"/?|\\"
)

var (
	includeChars   = flag.String("chars", "", "additional allowed characters")
	includeLetters = flag.Bool("letters", false, fmt.Sprintf("include %s", letters))
	includeNumbers = flag.Bool("numbers", false, fmt.Sprintf("include %s", numbers))
	includeSymbols = flag.Bool("symbols", false, fmt.Sprintf("include %s", symbols))
	length         = flag.Uint("length", 24, "number of characters in password")
)

func main() {
	flag.Parse()
	includeAll := !*includeLetters && !*includeNumbers && !*includeSymbols && *includeChars == ""

	chars := ""
	if *includeLetters || includeAll {
		chars += letters
	}
	if *includeNumbers || includeAll {
		chars += numbers
	}
	if *includeSymbols || includeAll {
		chars += symbols
	}
	if *includeChars != "" {
		chars += *includeChars
	}

	password := make([]byte, *length)
	for i := range password {
		n, err := rand.Int(rand.Reader, big.NewInt(int64(len(chars))))
		if err != nil {
			panic(err)
		}
		password[i] = chars[n.Int64()]
	}

	fmt.Println(string(password[:]))
}
