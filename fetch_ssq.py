import requests
from openpyxl import Workbook
import csv
import os

URL = 'https://dl.laoge.nyc.mn/'
TEST_FILE = "test_data.txt"

OUTPUT_TXT = "888.txt"
OUTPUT_XLSX = "888.xlsx"
OUTPUT_CSV = "888.csv"
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

    records = records[-COUNT:]
    print(f"Taking last {len(records)} records (newest data)")

    records.reverse()

    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write("期号\t日期\t红球1\t红球2\t红球3\t红球4\t红球5\t红球6\t蓝球\n")
        for r in records:
            f.write(f"{r['period']}\t{r['date']}\t{r['red1']}\t{r['red2']}\t{r['red3']}\t{r['red4']}\t{r['red5']}\t{r['red6']}\t{r['blue']}\n")
    print(f"Text file saved: {OUTPUT_TXT}")

    wb = Workbook()
    ws = wb.active
    ws.title = "双色球近888期"

    headers = ["期号", "日期", "红球1", "红球2", "红球3", "红球4", "红球5", "红球6", "蓝球"]
    ws.append(headers)

    for r in records:
        ws.append([r['period'], r['date'], r['red1'], r['red2'], r['red3'], r['red4'], r['red5'], r['red6'], r['blue']])

    wb.save(OUTPUT_XLSX)
    print(f"Excel file saved: {OUTPUT_XLSX}")

    with open(OUTPUT_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in records:
            writer.writerow([r['period'], r['date'], r['red1'], r['red2'], r['red3'], r['red4'], r['red5'], r['red6'], r['blue']])
    print(f"CSV file saved: {OUTPUT_CSV}")
    print("Done!")

if __name__ == "__main__":
    main()