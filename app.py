from flask import Flask, render_template, request, abort
import requests
import os
import csv
from io import StringIO

app = Flask(__name__)

# Your NewsAPI key (configure in environment for production)
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '8b30c2b8b0ca4516823b09fd09093b0e')

# Base URL for NewsAPI
NEWSAPI_URL = 'https://newsapi.org/v2/top-headlines'
NEWSAPI_EVERYTHING_URL = 'https://newsapi.org/v2/everything'

# Supported categories for filtering
CATEGORIES = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

@app.route('/')
def home():
    category = request.args.get('category')
    search_query = request.args.get('search')
    page = request.args.get('page', default=1, type=int)

    params = {
        'apiKey': NEWSAPI_KEY,
        'country': 'us',
        'pageSize': 20,
        'page': page,
    }
    if category and category.lower() in CATEGORIES:
        params['category'] = category.lower()

    if search_query:
        params['q'] = search_query

    response = requests.get(NEWSAPI_URL, params=params)
    
    if response.status_code != 200:
        abort(500, description="Error fetching news")

    data = response.json()
    articles = data.get('articles', [])

    return render_template(
        'home.html',
        news=articles,
        categories=CATEGORIES,
        selected_category=category or '',
        search_query=search_query or '',
        page=page,
        next_page=page + 1
    )

def fetch_stooq_history(symbol: str, interval: str = 'd'):
    url = f'https://stooq.com/q/d/l/?s={symbol.lower()}&i={interval}'
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200 or not resp.text.strip() or '404 Not Found' in resp.text:
        return []
    csv_text = resp.text
    reader = csv.DictReader(StringIO(csv_text))
    history = []
    for row in reader:
        try:
            history.append({
                'date': row['Date'],
                'open': float(row['Open']) if row['Open'] else None,
                'high': float(row['High']) if row['High'] else None,
                'low': float(row['Low']) if row['Low'] else None,
                'close': float(row['Close']) if row['Close'] else None,
                'volume': int(row['Volume']) if row['Volume'] else None,
            })
        except Exception:
            continue
    return history

def fetch_stooq_quote(symbol: str):
    url = f'https://stooq.com/q/l/?s={symbol.lower()}&f=sd2t2ohlcv&h&e=csv'
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return None
    reader = csv.DictReader(StringIO(resp.text))
    for row in reader:
        try:
            return {
                'symbol': row.get('Symbol'),
                'date': row.get('Date'),
                'time': row.get('Time'),
                'open': float(row.get('Open') or 0),
                'high': float(row.get('High') or 0),
                'low': float(row.get('Low') or 0),
                'close': float(row.get('Close') or 0),
                'volume': int(row.get('Volume') or 0),
            }
        except Exception:
            return None
    return None

@app.route('/markets')
def markets():
    symbol = request.args.get('symbol', 'AAPL')
    # Market news via NewsAPI everything for broader coverage
    news_params = {
        'apiKey': NEWSAPI_KEY,
        'q': f"{symbol} OR stock market OR shares",
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10,
    }
    news_resp = requests.get(NEWSAPI_EVERYTHING_URL, params=news_params)
    news_articles = []
    if news_resp.status_code == 200:
        news_articles = news_resp.json().get('articles', [])

    return render_template('markets.html', symbol=symbol.upper(), news=news_articles)

@app.get('/api/markets/history')
def markets_history():
    symbol = request.args.get('symbol', 'AAPL')
    interval = request.args.get('interval', 'd')  # d, w, m
    data = fetch_stooq_history(symbol, interval)
    return {'symbol': symbol.upper(), 'interval': interval, 'data': data}

@app.get('/api/markets/quote')
def markets_quote():
    symbol = request.args.get('symbol', 'AAPL')
    data = fetch_stooq_quote(symbol)
    if not data:
        abort(404, description='Quote not found')
    return data
@app.route('/news')
def news_detail():
    # For this API-based app, full content is usually not available,
    # typically show details passed via query parameters or direct to source URL
    title = request.args.get('title')
    description = request.args.get('description')
    content = request.args.get('content')
    url = request.args.get('url')
    published_at = request.args.get('publishedAt')
    source = request.args.get('source')

    if not title or not url:
        abort(404, description="News details not found")

    return render_template('news_detail.html', title=title, description=description, content=content,
                           url=url, published_at=published_at, source=source)


if __name__ == '__main__':
    app.run(debug=True)
