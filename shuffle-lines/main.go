package main

import (
	"bufio"
	"crypto/rand"
	"fmt"
	"math/big"
	"os"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	lines := []string{}
	for scanner.Scan() {
		// Trimming trailing newline helps protect against the
		// last line being the odd one out.
		lines = append(lines, strings.TrimSuffix(scanner.Text(), "\n"))
	}

	shuffle(lines)

	for _, line := range lines {
		fmt.Println(line)
	}
}

// https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#The_modern_algorithm
func shuffle(ss []string) {
	var j int
	for i := len(ss) - 1; i > 0; i-- {
		j = cryptoRandInt(i + 1)
		ss[i], ss[j] = ss[j], ss[i]
	}
}

func cryptoRandInt(maxExclusive int) int {
	r, err := rand.Int(rand.Reader, big.NewInt(int64(maxExclusive)))
	if err != nil {
		panic(err)
	}
	return int(r.Int64())
}
