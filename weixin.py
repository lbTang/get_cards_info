
import hashlib

def wx_test():
    data = {'timestamp': '1673682183', 'nonce': '1408862576', 'echostr': '7853813367529012519', 'signature': 'dbdc5351acdf7c79a53598443b2992716f522740'}
    if len(data) == 0:
        return "hello, this is handle view"
    signature = data['signature']
    timestamp = data['timestamp']
    nonce = data["nonce"]
    echostr = data["echostr"]
    token = "lianbintang" #请按照公众平台官网\基本配置中信息填写

    l = [token, timestamp, nonce]
    l.sort()
    l = [s.encode(encoding="utf-8") for s in l]
    sha1 = hashlib.sha1()
    l = list(map(sha1.update, l))
    print(l)
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        print(echostr)
    else:
        print("not match")

if __name__ == '__main__':
    wx_test()