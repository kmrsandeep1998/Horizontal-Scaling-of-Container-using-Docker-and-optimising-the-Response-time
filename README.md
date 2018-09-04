
# Here is the list of Resources and some points to to be noted.

docker build -t awesome .

docker swarm init

docker stack deploy --compose-file=docker-compose.yml prod

docker start -it <container-id> /bin/bash

https://opsdaily.blogspot.in/2016/09/haproxy-csv-stats.html

https://www.datadoghq.com/blog/how-to-collect-haproxy-metrics/#unix-socket-interface

http://haproxy.tech-notes.net/9-1-csv-format/

https://stackoverflow.com/questions/12732182/ab-load-testing
ab -k -c 350 -n 20000 http://localhost/

http://robotsforroboticists.com/pid-control/

https://cbonte.github.io/haproxy-dconv/1.7/configuration.html#8.2.3

http://localhost:1936/;csv #stats in csv format

https://stackoverflow.com/questions/26153686/how-do-i-run-a-command-on-an-already-existing-docker-container

