from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ Homepage route (avoids 404 error on Render)
@app.route('/')
def home():
    return '✅ Cricbuzz Live Score API is running! Visit /api/cricbuzz/live-scores to get scores.'

# ✅ Live scores API route
@app.route('/api/cricbuzz/live-scores', methods=['GET'])
def live_scores():
    try:
        data = get_cricbuzz_scores()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ✅ Web scraping logic
def get_cricbuzz_scores():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    headers = {"User-Agent": "Mozilla/5.0"}
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

        # Details from individual match page
        match_url = "https://www.cricbuzz.com/" + data.find('a')['href']
        sub_response = requests.get(match_url, headers=headers)
        sub_soup = BeautifulSoup(sub_response.content, 'lxml')
        match['description'] = ' '.join(sub_soup.text.split())

        matches.append(match)

    return matches

# ✅ Run locally (ignored by Render)
if __name__ == '__main__':
    app.run(debug=True)
