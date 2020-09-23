from urllib import request

def download_file(url, path):
    try:
        request.urlretrieve(url, path)
    except Exception as ex:
        pass
