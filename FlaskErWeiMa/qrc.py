import qrcode,random
import re


def reurl(text):
    img = qrcode.make(text)
    text = re.sub('.*?://', 'url_', text)
    text = re.sub(':', '：', text)
    text = re.sub('/', '／', text)
    text = re.sub('>', '》', text)
    text = re.sub('<', '《', text)
    text = re.sub('\?', '？', text)
    text = re.sub('\'', '‘', text)
    text = re.sub('\"', '“', text)
    text = re.sub('\*', 'xinghao', text)
    text = re.sub('\#', 'jinghao', text)
    text = re.sub('\%', 'baifenhao', text)
    text = re.sub(r'\\', '、', text)
    fileName = 'static/qrimg/' + text + '.png'
    img.save(fileName)
    return fileName
