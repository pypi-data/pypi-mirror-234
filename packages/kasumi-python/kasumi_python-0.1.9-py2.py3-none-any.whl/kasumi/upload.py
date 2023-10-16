from requests import put, post

def upload_bytes_with_upload_url(
    url: str, bytes: bytes, content_type: str = 'application/octet-stream'
) -> str:
    put(url, data=bytes, headers={'Content-Type': content_type})
    # remove query string
    try:
        url = url[:url.index('?')]
    except:
        raise Exception('invalid url')
    return url

def request_upload_url(
    filename: str, app_id: int, app_key: str, kasumi_url: str
) -> str:
    url = kasumi_url + '/v1/file/upload'
    data = {
        'filename': filename,
        'app_id': app_id,
        'key': app_key
    }
    try:
        r = post(url, data=data)
        if r.status_code != 200:
            raise Exception('failed to request upload url: ' + str(r.status_code) + '\n' + r.text)
        return r.json()['data']['url']
    except Exception as e:
        raise Exception('failed to request upload url: ' + str(e))
