import requests
import os
import time
import sys
from datetime import datetime

URL = 'https://dl.laoge.nyc.mn/'
OUTPUT_TXT_888 = "888.txt"
OUTPUT_TXT_ALL = "all.txt"
COUNT = 888

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'http://data.17500.cn/',
    }

    try:
        print(f"Fetching data from {URL}...", flush=True)
        session = requests.Session()
        session.trust_env = False
        response = session.get(URL, headers=headers, timeout=20, proxies={})
        print(f"Response status: {response.status_code}", flush=True)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to fetch data: {e}", flush=True)
        sys.exit(1)

def parse_line(line):
    parts = line.split()
    if len(parts) < 9:
        return None
    return {
        'period': parts[0],
        'date': parts[1],
        'red1': parts[2],
        'red2': parts[3],
        'red3': parts[4],
        'red4': parts[5],
        'red5': parts[6],
        'red6': parts[7],
        'blue': parts[8]
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
        print("Error: No valid records found!", flush=True)
        sys.exit(1)

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
    print(f"Created: {OUTPUT_TXT_ALL}", flush=True)

    print(f"Writing {len(records_888)} records to {OUTPUT_TXT_888}...", flush=True)
    with open(OUTPUT_TXT_888, 'w', encoding='utf-8') as f:
        f.write("期号\t日期\t红球1\t红球2\t红球3\t红球4\t红球5\t红球6\t蓝球\n")
        for r in records_888:
            f.write(f"{r['period']}\t{r['date']}\t{r['red1']}\t{r['red2']}\t{r['red3']}\t{r['red4']}\t{r['red5']}\t{r['red6']}\t{r['blue']}\n")
        f.write(f"\n# Updated at: {update_time}\n")
    print(f"Created: {OUTPUT_TXT_888}", flush=True)
    print("Done!", flush=True)

if __name__ == "__main__":
    main()