package main

import (
	"crypto/rand"
	"flag"
	"fmt"
	"math/big"
)

const (
	lower   = "abcdefghijklmnopqrstuvwxyz"
	upper   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	letters = lower + upper
	numbers = "0123456789"
	symbols = "!@#$%^&*()-=_+[]{},.<>;':\"/?|\\"
)

var (
	includeChars   = flag.String("chars", "", "additional allowed characters")
	includeLetters = flag.Bool("letters", false, fmt.Sprintf("include %s", letters))
	includeLower   = flag.Bool("lower", false, fmt.Sprintf("include %s", lower))
	includeNumbers = flag.Bool("numbers", false, fmt.Sprintf("include %s", numbers))
	includeSymbols = flag.Bool("symbols", false, fmt.Sprintf("include %s", symbols))
	includeUpper   = flag.Bool("upper", false, fmt.Sprintf("include %s", upper))
	length         = flag.Uint("length", 24, "number of characters in password")
)

func main() {
	flag.Parse()
	includeAll := !*includeLetters && !*includeLower && !*includeNumbers && !*includeSymbols && !*includeUpper && *includeChars == ""

	chars := ""
	if *includeLetters || includeAll {
		chars += letters
	} else {
		if *includeLower {
			chars += lower
		}
		if *includeUpper {
			chars += upper
		}
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
