import requests
def getData():
    print("Downloading...")
    url = 'http://117.247.89.137:85/'
    r = requests.get(url)
    print(r)
    with open('solapurMNC.txt', 'wb') as f:
        f.write(r.content)
    print("Downloaded...")

getData()
