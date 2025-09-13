package main

func getNumSum(num int) int {
	sum := 0
	for num > 0 {
		tmp := num % 10
		num = num / 10
		sum += tmp
	}
	return sum
}

func countBalls(lowLimit int, highLimit int) int {
	rest := make(map[int]int)

	for i := lowLimit; i <= highLimit; i++ {
		ss := getNumSum(i)
		rest[ss]++
	}

	maxCount := 0
	for _, count := range rest {
		if count > maxCount {
			maxCount = count
		}
	}

	return maxCount
}
