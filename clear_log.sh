sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' $1)