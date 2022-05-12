import time
from http.requests.proxy.requestProxy import RequestProxy

if __name__ == '__main__':
    print ("Hello")
    start = time.time()
    req_proxy = RequestProxy()
    print ("Initialization took: {0} sec".format((time.time() - start)))
    print ("Size : ", len(req_proxy.get_proxy_list()))
    print (" ALL = ", req_proxy.get_proxy_list())

    test_url = ('http://icanhazip.com')

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print ("Proxied Request Took: {0} sec => Status: {1}".format((time.time() - start), request.__str__()))
        if request is not None:
            print ("\t Response: ip={0}".format(request.text))
        print ("Proxy List Size: ", len(req_proxy.get_proxy_list()))

        print("-> Going to sleep..")
        time.sleep(10)