import sys
import time
import requests

requests.packages.urllib3.disable_warnings()


def download(url, path):
    for i in range(1, 5):
        try:
            resp = requests.get(url, verify=False)
            resp.raise_for_status()
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(resp.text)
            return
        except requests.exceptions.RequestException as e:
            if i == 4:
                raise e
            time.sleep(i * 2)
            print(f"request retry time: {i}, url: {url}, error: {e}", flush=True)


if __name__ == '__main__':
    file_url = sys.argv[1]
    save_path = sys.argv[2]
    download(file_url, save_path)
