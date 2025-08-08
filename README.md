# AI News App

A Flask application that fetches top headlines from NewsAPI and includes a Markets section with charts from Stooq.

## Local Development

1. Create a virtual environment and install dependencies:

```
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```

2. Set your NewsAPI key (get one at https://newsapi.org):

```
$env:NEWSAPI_KEY="YOUR_KEY"
# or
export NEWSAPI_KEY=YOUR_KEY
```

3. Run the server:

```
python app.py
```

## Deploy to Render

This repo includes `render.yaml` and a `Procfile`.

- Create a new Web Service in Render and connect your GitHub repo
- Render will detect Python, run `pip install -r requirements.txt`, and start with the Procfile command
- Set the environment variable `NEWSAPI_KEY` in the Render dashboard

## Environment Variables

- NEWSAPI_KEY: required to fetch news

## Notes

- Markets chart uses Stooq public CSV endpoints; some symbols may not provide real-time quotes. Use `.NS` for NSE symbols when available (e.g., `RELIANCE.NS`).

