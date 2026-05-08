import requests
import os

URL = 'https://dl.laoge.nyc.mn/'
TEST_FILE = "test_data.txt"

OUTPUT_TXT_888 = "888.txt"
OUTPUT_TXT_ALL = "all.txt"
COUNT = 888

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
    
    print(f"Fetching data from {URL}...")
    
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    
    session = requests.Session()
    session.trust_env = False
    response = session.get(URL, headers=headers, timeout=30, proxies={})
    response.raise_for_status()
    print("Success!")
    return response.text

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
    print(f"Total records: {len(lines)}")

    records = []
    for line in lines:
        record = parse_line(line)
        if record:
            records.append(record)

    print(f"Taking last {COUNT} records (newest data)")
    records_888 = records[-COUNT:]

    records.reverse()
    records_888.reverse()

    with open(OUTPUT_TXT_ALL, 'w', encoding='utf-8') as f:
        f.write("期号\t日期\t红球1\t红球2\t红球3\t红球4\t红球5\t红球6\t蓝球\n")
        for r in records:
            f.write(f"{r['period']}\t{r['date']}\t{r['red1']}\t{r['red2']}\t{r['red3']}\t{r['red4']}\t{r['red5']}\t{r['red6']}\t{r['blue']}\n")
    print(f"Text file saved: {OUTPUT_TXT_ALL}")

    with open(OUTPUT_TXT_888, 'w', encoding='utf-8') as f:
        f.write("期号\t日期\t红球1\t红球2\t红球3\t红球4\t红球5\t红球6\t蓝球\n")
        for r in records_888:
            f.write(f"{r['period']}\t{r['date']}\t{r['red1']}\t{r['red2']}\t{r['red3']}\t{r['red4']}\t{r['red5']}\t{r['red6']}\t{r['blue']}\n")
    print(f"Text file saved: {OUTPUT_TXT_888}")
    print("Done!")

if __name__ == "__main__":
    main()