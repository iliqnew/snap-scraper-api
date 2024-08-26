# web-snap-API
A web scraping API service that scrapes user-specified start url by making a screenshot of the page. Does the same thing with the first n urls on that page, where n is a user-passed integer. These parameters are introduced to the API via a POST request

## Run in Docker

```
docer-compose up --build
```

## Run locally
### Windows
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
``` 
### Linux
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage (Postman runs these fine)

### POST
```
curl -X POST -H "Content-Type: application/json" -d '{"start_url": "https://www.google.com", "max_urls": 10}' http://127.0.0.1:8000/screenshots
```

### GET
```
curl http://127.0.0.1:8000/screenshots/{scrape_id}
```

### GET /isalive
```
curl http://127.0.0.1:8000/isalive
```
