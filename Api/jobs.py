import requests
import pandas as pd
import requests
def get_listings(page):
    headers = {
        'authority': 'huntr.co',
        'sec-ch-ua': '^\\^Google',
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqUXlPVVpCTVRJNVJEYzJRMFZEUlRjMVJUUkNOMEpGT0VJek0wVTBRa0kwUmprM1FrRkJNQSJ9.eyJpc3MiOiJodHRwczovL3Jlbm5pZWhheWxvY2suYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNjg0ZjhhZjE0YThlMDA3MGM1YTVmZiIsImF1ZCI6Imh0dHBzOi8vYXBwLmh1bnRyLmNvIiwiaWF0IjoxNjE3NDQ4ODQzLCJleHAiOjE2MjAwNDA4NDMsImF6cCI6ImxaUVVjV1dzVHNXYlQ1UXRrcUZuNFNYckY3Q3hQNEJXIiwiZ3R5IjoicGFzc3dvcmQifQ.fS3SZlJrXmLY_xXxs1vWsrFgVVr_KKymcjQHeZOW4iyZ6P-qM8Jtue2hA_WzMuAVqzNE8mpXNjNfKS5lVJho7hXTOXZLHOcLMB-BtUDS4-piiNEKruY8o_JqFMoAGHLOK3_8k-5s166uIHYlmlEEVJASpQrQx5p2r-6XPvyOnonj4KeSufuoipW87gsbU9eSGwSDJc2TLygZfRe9MuqtwUZVsiKqdqKpOZYPGh2eN8fH77PO8hq-UC0qgI44K9e5HSA0MsgTejrogIddYxpls_LLtwmLGAQlXfMu6f1bvzym-Dl6X9S4i9XvsYvmVtaxH9lSMZGVZ511SqYuW-pVXg',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://huntr.co/jobs',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hr-HR;q=0.7,hr;q=0.6',
        #'cookie': '__cfduid=d7ea165eca66fbcaf904edd0aa9937cc11617448737; huntr_referrer=https://www.google.com/; _ga=GA1.2.394037263.1617448751; _gid=GA1.2.20544371.1617448751; _gaexp=GAX1.2._0isSKCySOSXjtbSeRQVsg.18791.1; mp_1d6f823f8d5432354b55fc0af879343c_mixpanel=^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^2217897754f6c1b6-03956cee7a4066-c3f3568-100200-17897754f6de8^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^2217897754f6c1b6-03956cee7a4066-c3f3568-100200-17897754f6de8^%^22^%^2C^%^22^%^24search_engine^%^22^%^3A^%^20^%^22google^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22https^%^3A^%^2F^%^2Fwww.google.com^%^2F^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22www.google.com^%^22^%^2C^%^22__alias^%^22^%^3A^%^20^%^2260684f8af14a8e0070c5a5ff^%^22^%^2C^%^22^%^24user_id^%^22^%^3A^%^20^%^2260684f8af14a8e0070c5a5ff^%^22^%^7D; device-source=https://huntr.co/home; device-referrer=https://huntr.co/signup; helpcrunch.com-huntr-5233-user-id=60684f8bdafb2f002c706a6c; helpcrunch.com-huntr-5233-helpcrunch-device=^{^\\^id^\\^:227551,^\\^secret^\\^:^\\^bWUMK/HUs0zTyYja4huyqtnuU1++SPEnXXG1Xu3+kK433p3zgOLjg8HGllSbqAOKaWouaREozQQKq77EiQhUrQ==^\\^,^\\^sessions^\\^:1^}; helpcrunch.com-huntr-5233-device-id=227551; helpcrunch.com-huntr-5233-token-data=^{^\\^access_token^\\^:^\\^8cqfOpDRpCYCIugPKks8WhnceiWXUzdi9GIsdl9Yd7xR1FgzIM5dlsymoJqGri67l1U017DKksw4UKtvN35fHMn+NA3XCHJA93AnFRnn6cZTxHOpKlY3CqLQxlb08dbsEKmRYjYQhEBuObOUF5+4BjjC+EyKUm4FdabcgACIW2EOw3sN52VTXUGp07dBofUv/xj3F8wRguEKNwgzNpq36//e78AzU58HXjzpu1dE6LQv72Fv6gX1uh8S75t6zBIaQ7+SU/g/Bk6xGo68Puvkz4ww9ijDHEROT0p2Yy0+PYq/FXKENPIK5Ybo+JMUvAk3OYhOZoFSKh4fJnkdcTIpEV2DVWv4YeZCtcA6Pw5iFrQxSOK3D4becf+noADLwUAMnbpuYOr0hGeKfQFAWoZqYaGwJcCBDBDdNubTD8o647ujwxiEewvRn/KsyAU5i/AQQ8+UbRUUXPxyctnKohIPv/EUz6qhWW5TFvW0oMI66IbN3kueF6Koq8kck5isnH5wGq3K7euFFeoaxfgs4JXR0xknCk8Cv2zpaLj9Eg==^\\^,^\\^refresh_token^\\^:^\\^7jQOArTgFPdG30Zx/RW60VsLioZko+9tyQ6XftwFA7AzKSs815fcplySCyad/cahbr3C45A=^\\^,^\\^expires_in^\\^:1617450538461^}',
        'if-none-match': 'W/^\\^DCxd//QpPey/s9ZAg8c19w==^\\^',
    }

    params = (
        ('page', str(page)),
        ('zoom', '1'),
    )

    response = requests.get('https://huntr.co/public/search/job-posts', headers=headers, params=params)

    json_response=response.json()
    #return json_response

    master_list = []

    for listing in json_response['results']:
        data_dict = {}
        # print (listing.keys())
        data_dict["id"] = listing["_id"]
        data_dict["createdAt"] = listing["createdAt"]
        data_dict["employer"] = listing["_employer"]
        #data_dict["textDescription"] = listing["textDescription"]
        try:
            data_dict["address"] = listing["places"][0]["address"]
        except:
            data_dict["address"] = None
        data_dict["name"] = listing["places"][0]["name"]
        data_dict["longitude"] = listing["places"][0]["point"]["coordinates"][0]
        data_dict["latitude"] = listing["places"][0]["point"]["coordinates"][1]

        master_list.append(data_dict)


    data_frame = pd.DataFrame(master_list)

    return (data_frame)

listings=get_listings(20)

print(listings)

listings.to_csv("page_20.csv",index=False)