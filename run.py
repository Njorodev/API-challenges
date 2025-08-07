from multiprocessing import Process
import uvicorn
from flask_apis.todo-api.app import app as flask_todo-api
from flask_apis.api2.app import app as flask_api2

def run_flask_to():
    flask_todo-api.run(port=5001)

def run_flask_api2():
    flask_api2.run(port=5002)

def run_fastapi_api1():
    uvicorn.run("fastapi_apis.api1.main:app", host="0.0.0.0", port=8001, reload=True)

def run_fastapi_api2():
    uvicorn.run("fastapi_apis.api2.main:app", host="0.0.0.0", port=8002, reload=True)

if __name__ == "__main__":
    processes = [
        Process(target=run_flask_todo-api),
        Process(target=run_flask_api2),
        Process(target=run_fastapi_api1),
        Process(target=run_fastapi_api2),
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
