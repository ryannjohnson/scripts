package main

import (
	"bufio"
	"crypto/rand"
	"fmt"
	"math/big"
	"os"
	"strconv"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		i, err := strconv.ParseInt(line, 10, 64)
		if err != nil || i < 1 {
			fmt.Fprintln(os.Stderr, "Roll sides must be positive integers.")
			os.Exit(1)
		}
		n, err := rand.Int(rand.Reader, big.NewInt(i))
		if err != nil {
			panic(err)
		}
		fmt.Println(n.Int64() + 1)
	}
}
