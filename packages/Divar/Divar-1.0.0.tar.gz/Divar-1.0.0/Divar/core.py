import requests
import json
import sqlite3
import jwt
import datetime


class Client:
    def __init__(self , header:dict = None , db_usage:bool = False , db_name:str = None):
        '''
            setting up things needed to run the instance , but all the arguments are clearly optional!
        '''
        self._header = header
        self._Cookie = self._header.get('Cookie')
        self._db_name = db_name if db_name and db_usage == True else 'db.sqlite3'

        if self._header is None:
            self._header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        
    def GetCategory(self , city:str , category_name:str , pagination:int=1) -> None:
        '''
            Getting Catogry Posts , pagination is optional
        '''
        url = f'https://api.divar.ir/v8/web-search/{city.lower()}/{category_name.lower()}?page={pagination}'
        req = requests.get(url, headers=self._header).json()

        resp_list = list()
        if req.status_code == 200 or 201:
            for item in data['web_widgets']['post_list']:
                if item['data']:
                    try:
                        respon_dict = dict()
                        respon_dict['Price'] = item['data']['middle_description_text']

                        respon_dic['Title'] = item['data']['title'] 
                        respon_dic['Status'] = item['data']['top_description_text']
                        respon_dic['Loc_time']= item['data']['bottom_description_text'] 
                        respon_dic['Exact_loc'] = item['data']['action']['payload']['web_info']['district_persian']  
                        respon_dic['Slug'] = item['data']['action']['payload']['web_info']['category_slug_persian'] 
                        respon_dic['Token'] = item['data']['token']
                        respon_dic['IsVerified'] = item['data']['is_checked'] 
                        respon_dic['CanChat'] = item['data']['has_chat'] 
                        respon_dic['ImgCount'] = int(item['data']['image_count'])
                        respon_dic['MainImg'] = item['data']['image_url'][1]['src']

                        resp_list.append(respon_dict)

            return resp_list

                    except Exception as err:
                        raise err


    def GetPost(self , Token:str) -> None :
        '''
            Getting Post information -> Token is necessary
        '''

        url = f'https://api.divar.ir/v8/posts-v2/web/{Token}'
        req = requests.get(url, headers=self._header).json()

        if req.status_code == 200 or 201:
            result_dict = dict()

            try:
                title = data["sections"][1]["widgets"][0]["data"]["title"]
                result_dict["عنوان"] = title
                # Get the description
                description = data["sections"][2]["widgets"][1]["data"]["text"]
                result_dict["توضیحات"] = description

                # Get all images
                images = [item["image"]["url"] for item in data["sections"][3]["widgets"][0]["data"]["items"]]
                result_dict["images"] = images

                Brand = data["sections"][4]["widgets"][0]["data"]["action"]["payload"]["uri_schema"][1]
                result_dict["برند"] = Brand
                Ram = data["sections"][4]["widgets"][6]["data"]["value"]
                result_dict["رم"] = Ram
                
                for field in data["sections"][4]["widgets"]:

                    try:
                        result_dict[field["data"]["title"]] = field["data"]["value"]

                    except Exception as err:
                        raise err

                return result_dict

            except Exception as err:
                raise err


    def GetPostNumer(self , Token:str):
        try:
            jwt_token = self._Cookie.split('; token=')[1].split(';')[0]
            payload = jwt.decode(jwt_token , algorithms = ['HS512'])
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            
            self._lark = False if datetime.datetime.now() > exp_time else True

        except Exception as e:
            raise Exception(f'{e} the was an error during checking the jwt token')

        if self._lark:
            req = requests.get(
                f"https://api.divar.ir/v8/postcontact/web/contact_info/{Token}", headers=self._session
            )

            if req.status_code == 200 or 201:
                jsn = json.loads()

                if jsn['widget_list'][0]['data']['title'] == '\u0634\u0645\u0627\u0631\u0647 \u0645\u062e\u0641\u06cc \u0634\u062f\u0647 \u0627\u0633\u062a':
                    return 'Hidden Number!'
                
                else:
                    return jsn['widget_list'][0]['data']['action']['payload']['phone_number']
                
            else:
                raise Exception('Couldnt find the Token you specified , please replace it with a good one')
                
        else:
            raise Exception('The JWT Token is expired , plz replace it and try again')
        
    def GetPostImage(self , id:int , Token:str , path:str):
        try:
            jwt_token = self._Cookie.split('; token=')[1].split(';')[0]
            payload = jwt.decode(jwt_token , algorithms = ['HS512'])
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            
            self._lark = False if datetime.datetime.now() > exp_time else True

            if self._lark:
                req = requests.get(
                f"https://s100.divarcdn.com/static/thumbnails/{id}/{Token}.jpg", headers=self._header
                )
                
                if req.status_code == 200 or 201:
                    with open(path, 'wb') as file:
                        for chunk in req:
                            file.write(chunk)

                else:
                    raise Exception(f'{req.status_code} -> Bad Request!')
                
            else:
                raise Exception('the cookie you specified is not correct! or jwt is expired')

        except Exception as e:
            raise Exception(f'{e} the was an error during checking the jwt token')
        

    def __str__(self):
        return 'instance of Divar pkg'
        
    
                

