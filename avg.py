file = open("pid_response.dat","r")
lines = file.readlines()
s,c = 0,0
for line in lines:
	l = line.strip().split(' ')
	s += float(l[1])
	c += 1

print s/c
file.close()