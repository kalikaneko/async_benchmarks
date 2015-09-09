benchmark_naive_wsgi:
	python wsgi_ref.py &
	sleep 1
	ab -n 100 http://127.0.0.1:8000/
	curl http://localhost:8000/count
	curl http://localhost:8000/delete
	kill `ps x| grep '[p]ython wsgi_ref.py' | cut -d ' ' -f 1`

benchmark_naive_wsgi_c10:
	python wsgi_ref.py &
	sleep 1
	ab -n 100 -c 10 http://127.0.0.1:8000/
	curl http://localhost:8000/count
	curl http://localhost:8000/delete
	kill `ps x| grep '[p]ython wsgi_ref.py' | cut -d ' ' -f 1`
