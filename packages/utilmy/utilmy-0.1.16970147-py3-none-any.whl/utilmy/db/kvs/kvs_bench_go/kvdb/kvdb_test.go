package kvdb_test

import (
	"testing"

	"github.com/arita37/myutil/utilmy/db/kvs/kvdb"
)

func BenchmarkSetRedis(b *testing.B) {
	clientCount := 100
	setCount := 10000
	kvdb.RunSetXClientsYTimes(clientCount, setCount, "6379")
}

func BenchmarkGetRedis(b *testing.B) {
	clientCount := 100
	getCount := 10000
	kvdb.RunGetXClientsYTimes(clientCount, getCount, "6379")
}

func BenchmarkSetKeydDb(b *testing.B) {
	clientCount := 100
	setCount := 10000
	kvdb.RunSetXClientsYTimes(clientCount, setCount, "6380")
}

func BenchmarkGetKeyDb(b *testing.B) {
	clientCount := 100
	getCount := 10000
	kvdb.RunGetXClientsYTimes(clientCount, getCount, "6380")
}

func BenchmarkSetDragonfly(b *testing.B) {
	clientCount := 100
	setCount := 10000
	kvdb.RunSetXClientsYTimes(clientCount, setCount, "6381")
}

func BenchmarkGetDragonfly(b *testing.B) {
	clientCount := 100
	getCount := 10000
	kvdb.RunGetXClientsYTimes(clientCount, getCount, "6381")
}

// func BenchmarkSetSkyTable(b *testing.B) {
// 	clientCount := 20
// 	setCount := 10000
// 	kvdb.SkyTableRunSetXClientsYTimes(clientCount, setCount)
// }

// func BenchmarkGetSkyTable(b *testing.B) {
// 	clientCount := 20
// 	getCount := 10000
// 	kvdb.SkyTableRunGetXClientsYTimes(clientCount, getCount)
// }
