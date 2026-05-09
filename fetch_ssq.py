import requests
import os
import time
import sys
from datetime import datetime

URL = 'https://dl.laoge.nyc.mn/'
TEST_FILE = "test_data.txt"

OUTPUT_TXT_888 = "888.txt"
OUTPUT_TXT_ALL = "all.txt"
COUNT = 888
MAX_RETRIES = 3
RETRY_DELAY = 5
REQUEST_TIMEOUT = 20

def fetch_data():
    if os.path.exists(TEST_FILE):
        print(f"Using local test file: {TEST_FILE}")
        with open(TEST_FILE, 'r', encoding='utf-8') as f:
            return f.read()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'http://data.17500.cn/',
    }

    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Fetching data from {URL} (attempt {attempt}/{MAX_RETRIES})...", flush=True)
            session = requests.Session()
            session.trust_env = False
            response = session.get(URL, headers=headers, timeout=REQUEST_TIMEOUT, proxies={})
            print(f"  Response status: {response.status_code}, content length: {len(response.text)}", flush=True)
            response.raise_for_status()
            content = response.text
            if not content or not content.strip():
                raise ValueError("Empty response content")
            print("Success!", flush=True)
            return content
        except requests.exceptions.Timeout as e:
            last_error = f"Timeout error (>{REQUEST_TIMEOUT}s): {e}"
        except requests.exceptions.ConnectionError as e:
            last_error = f"Connection error: {e}"
        except requests.exceptions.HTTPError as e:
            last_error = f"HTTP error {response.status_code}: {e}"
        except ValueError as e:
            last_error = f"Content error: {e}"
        except requests.exceptions.RequestException as e:
            last_error = f"Request error: {e}"

        print(f"  Attempt {attempt} failed: {last_error}", flush=True)
        if attempt < MAX_RETRIES:
            print(f"  Retrying in {RETRY_DELAY}s...", flush=True)
            time.sleep(RETRY_DELAY)

    print(f"All {MAX_RETRIES} attempts failed. Last error: {last_error}", flush=True)
    sys.exit(1)

def parse_line(line):
    parts = line.split()
    if len(parts) < 9:
        return None
    period = parts[0]
    date = parts[1]
    red_balls = parts[2:8]
    blue_ball = parts[8]
    return {
        'period': period,
        'date': date,
        'red1': red_balls[0],
        'red2': red_balls[1],
        'red3': red_balls[2],
        'red4': red_balls[3],
        'red5': red_balls[4],
        'red6': red_balls[5],
        'blue': blue_ball
    }

def main():
    content = fetch_data()
    lines = content.strip().split('\n')
    print(f"Total records: {len(lines)}", flush=True)

    records = []
    for line in lines:
        record = parse_line(line)
        if record:
            records.append(record)

    if not records:
        print("Error: No valid records found in the data!", flush=True)
        sys.exit(1)

    print(f"Taking last {COUNT} records (newest data)", flush=True)
    records_888 = records[-COUNT:]

    records.reverse()
    records_888.reverse()

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Writing {len(records)} records to {OUTPUT_TXT_ALL}...", flush=True)
    with open(OUTPUT_TXT_ALL, 'w', encoding='utf-8') as f:
        f.write("期号\t日期\t红球1\t红球2\t红球3\t红球4\t红球5\t红球6\t蓝球\n")
        for r in records:
            f.write(f"{r['period']}\t{r['date']}\t{r['red1']}\t{r['red2']}\t{r['red3']}\t{r['red4']}\t{r['red5']}\t{r['red6']}\t{r['blue']}\n")
        f.write(f"\n# Updated at: {update_time}\n")
    print(f"Text file saved: {OUTPUT_TXT_ALL}", flush=True)

    print(f"Writing {len(records_888)} records to {OUTPUT_TXT_888}...", flush=True)
    with open(OUTPUT_TXT_888, 'w', encoding='utf-8') as f:
        f.write("期号\t日期\t红球1\t红球2\t红球3\t红球4\t红球5\t红球6\t蓝球\n")
        for r in records_888:
            f.write(f"{r['period']}\t{r['date']}\t{r['red1']}\t{r['red2']}\t{r['red3']}\t{r['red4']}\t{r['red5']}\t{r['red6']}\t{r['blue']}\n")
        f.write(f"\n# Updated at: {update_time}\n")
    print(f"Text file saved: {OUTPUT_TXT_888}", flush=True)
    print("Done!", flush=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)
        sys.exit(1)