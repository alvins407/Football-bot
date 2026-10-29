import os
import requests

# 1. Load your secure keys from GitHub Secrets
LIVESCORE_API_TOKEN = os.environ.get("LIVESCORE_TOKEN")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")

# 2. RapidAPI Endpoints for API-Football (Live Matches)
URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
HEADERS = {
    "x-rapidapi-key": LIVESCORE_API_TOKEN,
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
}


def fetch_live_matches():
  querystring = {"live": "all"}
  response = requests.get(URL, headers=HEADERS, params=querystring)

  if response.status_code == 200:
    return response.json().get("response", [])
  else:
    print(f"Error fetching scores: {response.status_code} - {response.text}")
    return []


def post_to_facebook(message):
  url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/feed"
  payload = {"message": message, "access_token": FB_PAGE_ACCESS_TOKEN}
  response = requests.post(url, data=payload)

  if response.status_code == 200:
    print("Successfully posted to Facebook!")
  else:
    print(f"Failed to post: {response.text}")


def main():
  print("Checking live matches via RapidAPI...")
  matches = fetch_live_matches()

  if not matches:
    print("No live matches right now.")
    return

  for match in matches:
    try:
      home_team = match["teams"]["home"]["name"]
      away_team = match["teams"]["away"]["name"]

      home_score = match["goals"]["home"]
      away_score = match["goals"]["away"]

      elapsed_time = match["fixture"]["status"]["elapsed"]
      status_short = match["fixture"]["status"]["short"]

      message = (
          f"⚽ LIVE MATCH UPDATE ⚽\n\n"
          f"{home_team}  {home_score} - {away_score}  {away_team}\n"
          f"⏱️ Time: {elapsed_time}' ({status_short})\n\n"
          f"#LiveScore #Football"
      )

      post_to_facebook(message)

    except Exception as e:
      print(f"Error parsing match data: {e}")


if __name__ == "__main__":
  main()
