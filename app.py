from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3MmIxNjE1MC0zZTE0LTAxM2UtOTMzNi02ZThjNzIzMTJmZDIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzUxOTcwNjEwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InBlcmZvcm1hbmNlLWFuIn0.NH0x6_sd19Dx9Ad9Qt5LnUE6ZUwI8vXZGyyub4yA44g"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.api+json"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/matches/<player_name>')
def api_matches(player_name):
    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player_name}"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    if not data.get("data"):
        return jsonify({"error": "Player not found"})
    player = data['data'][0]
    matches = [m['id'] for m in player['relationships']['matches']['data']]
    return jsonify({
        "player_id": player['id'],
        "matches": matches[:10]
    })

@app.route('/api/match/<match_id>')
def api_match_detail(match_id):
    url = f"https://api.pubg.com/shards/steam/matches/{match_id}"
    resp = requests.get(url, headers=HEADERS)
    return jsonify(resp.json())

@app.route('/match/<match_id>')
def match_detail(match_id):
    return render_template('match_detail.html', match_id=match_id)

if __name__ == "__main__":
    app.run(debug=True)
