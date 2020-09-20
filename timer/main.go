package main

import (
	"fmt"
	"os"
	"time"
)

var interval = time.Second

func main() {
	args := os.Args[1:]

	if len(args) != 1 {
		fmt.Fprintln(os.Stderr, "Requires 1 argument, eg 15m")
		os.Exit(1)
	}

	d, err := time.ParseDuration(args[0])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	end := time.Now().Add(d)

	var delta time.Duration
	var deltaToNextTick time.Duration
	for {
		delta = end.Sub(time.Now())
		if delta <= 0 {
			break
		}
		deltaToNextTick = delta % interval
		time.Sleep(deltaToNextTick)
		fmt.Fprintf(os.Stderr, "    \r%s", (delta - deltaToNextTick).String())
	}

	fmt.Fprintln(os.Stderr, "\rTimer complete.")
}
