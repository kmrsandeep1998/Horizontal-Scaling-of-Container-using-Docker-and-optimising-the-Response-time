from pid_config import *
import time
import docker
import threading



requests, responses = 0, 0

io_combined = open(name = 'pid_combined.dat', mode = 'w+')
io_response = open(name = 'pid_response.dat', mode = 'w+')
io_request = open(name = 'pid_request.dat', mode = 'w+')
io_container = open(name = 'pid_container.dat', mode = 'w+')

####################################################

def log_handler():

	client = docker.APIClient(base_url='unix://var/run/docker.sock');
	logs = client.logs(haproxy_cid,stream=True)
	global requests
	global responses
	while True:
		try:
			log = logs.next()
			for line in log.split('\n'):
				if 'X-Response-Time' in line:
					millis = line.split(' ')[2][0:5]
					responses = responses + float(millis)
					requests += 1
		except RuntimeError:
			pass
####################################################

def scale(required):

	update = max(int(round(required)), 1)
	print update

	client = docker.from_env()
	services =  client.services
	service = services.get(service_id = service_sid)
	replica_mode = docker.types.ServiceMode('replicated', replicas = update)
	service.update(mode = replica_mode)

####################################################

def balance_handler(interval):

	global requests
	global responses

	timer = 0
	pre_requests, pre_responses = 0, 0
	error_prior, integral = 0, 0

	while True:

		actual_request = requests - pre_requests
		actual_response = responses - pre_responses
		actual_avg_response = actual_response / actual_request if actual_request != 0 else 0

		error =  threshold_avg_response - actual_avg_response
		integral = integral + error * interval
		derivative = (error - error_prior) / interval

		required = kp * error + ki * integral + kd * derivative		
		print required

		current_containers = len(docker.from_env().containers.list())
		required = current_containers - required
		
		scale_thread = threading.Thread(target = scale, args = [required])
		scale_thread.start()


		# exporting response time
		export_combined = str(timer * 0.001) + ' ' + str(actual_avg_response) +  ' ' + str(actual_request) + ' ' + str(current_containers) + '\n'
		export_response = str(timer * 0.001) + ' ' + str(actual_avg_response) + '\n'
		export_request = str(timer * 0.001) + ' ' + str(actual_request) + '\n'
		export_container = str(timer * 0.001) + ' ' + str(current_containers) + '\n'


		io_combined.write(export_combined)
		io_combined.flush()

		io_response.write(export_response)
		io_response.flush()

		io_request.write(export_request)
		io_request.flush()

		io_container.write(export_container)
		io_container.flush()

		error_prior = error
		pre_requests = requests
		pre_responses = responses

		timer += interval
		time.sleep(interval * 0.001)


log_thread = threading.Thread(target = log_handler, args = [])
balance_thread = threading.Thread(target = balance_handler, args = [interval])

log_thread.start()
balance_thread.start()