import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def get_cricbuzz_scores():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevents being blocked
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    matches = []
    listings = soup.find_all('div', class_="cb-mtch-lst cb-col cb-col-100 cb-tms-itm")

    for data in listings:
        match = {}
        match['matchVs'] = data.find('h3', class_="cb-lv-scr-mtch-hdr inline-block").text.strip()
        match['matchType'] = data.find('span', class_="text-gray").text.strip()

        try:
            match['Team1_score'] = data.find_all('div', class_="cb-ovr-flo")[2].text.strip()
        except:
            match['Team1_score'] = ''

        try:
            match['Team2_score'] = data.find_all('div', class_="cb-ovr-flo")[4].text.strip()
        except:
            match['Team2_score'] = ''

        # Go inside match details page
        try:
            match_url = "https://www.cricbuzz.com/" + data.find('a')['href']
            sub_response = requests.get(match_url, headers=headers)
            sub_soup = BeautifulSoup(sub_response.content, 'lxml')
            match['description'] = ' '.join(sub_soup.text.split())
        except:
            match['description'] = 'Details not available.'

        matches.append(match)

    return matches

@app.route('/api/cricbuzz/live-scores', methods=['GET'])
def live_scores():
    try:
        data = get_cricbuzz_scores()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ✅ DO NOT use `app.run()` on Render — Gunicorn will run it
# So use this:
if __name__ == 'API_Cricket_Score':
    app = app
