import cv2
from urllib.request import Request, urlopen
import numpy as np

histogram_cache = {}

IMAGE_SIMILARITY_THREADSHOLD = 0.3

def images_are_similar(url1, url2):
    return get_image_correlation(url1, url2) > IMAGE_SIMILARITY_THREADSHOLD

def get_image_correlation(url1, url2):
    hist1 = histogram_cache[url1] if url1 in histogram_cache else get_histogram(url1)
    hist2 = histogram_cache[url2] if url2 in histogram_cache else get_histogram(url2)
    if hist1 is None or hist2 is None:
        return -1
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

def get_histogram(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        req = urlopen(req)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)  # 'Load it as it is'
        try:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            if "Invalid number of channels in input image:" in str(e):
                gray_image = image

        hist = cv2.calcHist([gray_image], [0], None, [128], [0, 256])
        histogram_cache[url] = hist
        return hist
    except:
        return None



