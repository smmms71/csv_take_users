import os
import json
import requests

def fast_avatar_curl(input_directory: str, theme: str):
    url = "http://127.0.0.1:9022/human_parser"
    files = [('input_person_file', ('16.jpg', open(input_directory,'rb'), 'image/JPEG'))]
    return requests.request("POST", url, files=files)
    
     
    # token = open('source/token.json').read()[1:-1]
    # api = 'https://studio213.us/gpu'
    # input_url = os.popen(f"curl 'https://studio213.us/gpu/upload.php?file=input.jpg&ses_id='{token} --data-binary '@{input_directory}'").read()
    # curl = os.popen(f"curl {api}/reroute.php\?ses_id\={token}\&container\=ubuntu\&gpu\=container1 -X POST -d '-X POST 127.0.0.1:8002/rembg --form input={input_url} --form output=IO/output'").read()
    
    # try:
    #     url = json.loads(curl)['files'][0]
    #     image_name = 'out.jpg'
    #     os.system(f'wget {url} -O {image_name}')
    #     return True
    # except Exception as e:
    #     print(e)
    #     return False

def train_avatar_curl():
    pass