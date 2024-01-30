# tinyurl

Run app
```shell
gunicorn "app:get_app()" --chdir src/ --bind localhost:8080 --worker-class uvicorn.workers.UvicornWorker --reload  
```