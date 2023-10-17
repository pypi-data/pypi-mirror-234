## Reference


https://aws.amazon.com/blogs/database/optimize-redis-client-performance-for-amazon-elasticache/

https://doordash.engineering/2020/11/19/building-a-gigascale-ml-feature-store-with-redis/

https://doordash.engineering/2019/01/02/speeding-up-redis-with-compression/





# Install Go
```bash
curl -OL https://go.dev/dl/go1.19.3.linux-amd64.tar.gz
sha256sum go1.19.3.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.3.linux-amd64.tar.gz
echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.bash_profile
```

## Running the tests
```bash

https://ragainis.lt/yet-another-comparison-redis-5-6-vs-keydb-6-for-small-instances-eed4f36bd2ba


https://openbenchmarking.org/test/pts/rocksdb

https://openbenchmarking.org/suite/pts/database


    docker compose up -d
    go mod download
    go install  golang.org/x/perf/cmd/benchstat
    go test ./... -bench=. -cpu 4 >/tmp/out
    benchstat /tmp/out
```

## example output
### example1
- cpu: 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
- 100 clients
- 10.000 operations / client
- 10 length of key and 500 length of value

|name                 |time    |
|---                  |---     |
|SetRedis             |7.78s   |
|GetRedis             |7.29s   |
|SetKeydDb            |8.31s   |
|GetKeyDb             |5.47s   |
|SetDragonfly         |6.21s   |
|GetDragonfly         |6.33s   |

### example2
- cpu: 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
- 20 clients
- 10.000 operations / client
- 10 length of key and 500 length of value

|name                   |time    |
|---                    |---     |
|SetRedis               |1.67s   |
|GetRedis               |1.49s   |
|SetKeydDb              |1.93s   |
|GetKeyDb               |1.74s   |
|SetDragonfly           |3.71s   |
|GetDragonfly           |1.57s   |


### example3
- cpu: 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
- 4 clients
- 50.000 operations / client
- 10 length of key and 500 length of value

|name                   |time    |
|---                    |---     |
|SetRedis               |2.62s   |
|GetRedis               |2.17s   |
|SetKeydDb              |2.82s   |
|GetKeyDb               |2.32s   |
|SetDragonfly           |3.70s   |
|GetDragonfly           |2.93s   |

