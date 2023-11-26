from sanic import Sanic, response
from sanic.response import json, text, file
import asyncio
import aiohttp
from aiogram import types, Bot
from typing import Text, Any, Union, List
import json

import state_handler
from user import User

# API_TOKEN = "5617752022:AAFWXmIGrlFugR-7BOho98nbOcwMw-TLkhU"
API_TOKEN = "5582271816:AAHWWCkX-XwTEQt2O-RQnbKE2XAaqZFh-fY"
bot = Bot(token=API_TOKEN)
PAYMENT_TOKEN = "284685063:TEST:NTBlZDYyODU0ZmM3" # sprite test
NGROK_URL = "https://5d12-138-88-194-9.ngrok-free.app"
WEBHOOK_URL = f"{NGROK_URL}/telegram"
TELEGRAM_BOT_API_URL = f'https://api.telegram.org/bot{API_TOKEN}/'
TELEGRAM_BOT_FILE_URL = f'https://api.telegram.org/file/bot{API_TOKEN}/'
users = {}
sample_price = types.LabeledPrice(label='Sample', amount=10000)

async def sending_request(
        url: Text, 
        params: Any = None, 
        data: Any = None, 
        json: Any = None, 
        headers: Any = None, 
        method: Text = "POST",
        timeout: Any = None, 
        service_name: Text = "Unkown",
        verbose: bool = True
    ) -> Text:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            try: 
                async with aiohttp.request(
                    method, url, json=json,
                    params=params, data=data, headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    return await response.text()
            except aiohttp.ClientError as e:
                if verbose:
                    print(f"[{service_name} Service] Error in API call: {e}")
                return ""
    except Exception as e:
        if verbose:
            print(f"[{service_name} Service] Error Sending request: {e}")
        return ""
    
async def sending_request_file(
        url: Text, 
        params: Any = None, 
        data: Any = None, 
        json: Any = None, 
        headers: Any = None, 
        method: Text = "POST",
        timeout: Any = None, 
        service_name: Text = "Unkown",
        verbose: bool = True
    ):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            try: 
                async with aiohttp.request(
                    method, url, json=json,
                    params=params, data=data, headers=headers, 
                    timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    # file = await response.read()
                    return await response.read()
            except aiohttp.ClientError as e:
                if verbose:
                    print(f"[{service_name} Service] Error in API call: {e}")
                return ""
    except Exception as e:
        if verbose:
            print(f"[{service_name} Service] Error Sending request: {e}")
        return ""

response = asyncio.run(
    sending_request(
        url = f"{TELEGRAM_BOT_API_URL}setWebhook",
        params={
            "url" : WEBHOOK_URL
        }
    )
)
print(f"Response: {response}")

app = Sanic(__name__)

# Define Routes
@app.route('/', methods=['GET'])
async def handle_GET(request):
    return text("This is a GET route")

@app.route('/telegram', methods=['POST'])
async def handle_POST(request):
    if request.method == "POST":
        request_dict = request.json
        if isinstance(request_dict, Text):
            request_dict = json.loads(request_dict)
        await main_program(request_dict)
        
    return text("success")

@app.route('/<folder>/<filename>')
async def get_file(request, folder, filename):
    return await file(f'{folder}/{filename}')

@app.route('/<folder>/<subfolder>/<filename>')
async def get_file2(request, folder, subfolder, filename):
    return await file(f'{folder}/{subfolder}/{filename}')

@app.route('/<folder>/<subfolder1>/<subfolder2>/<filename>')
async def get_file3(request, folder, subfolder1,subfolder2, filename):
    return await file(f'{folder}/{subfolder1}/{subfolder2}/{filename}')

async def send_messages(recipient_id: Union[Text, Any], 
        sequence: List[Text],
        texts: List[Union[Text, Any]], 
        images: List[Union[Text, Any]],  **kwargs: Any) -> None:
    """Sends a message to the recipient."""

    # Send the message based on the sequence item
    for item in sequence:
        if item == 'image':
            url = f"{TELEGRAM_BOT_API_URL}sendPhoto"
            json_data = {"chat_id": recipient_id, "photo": images.pop(0)}
            response = await sending_request(url, json=json_data)
        elif item == 'text':
            url = f"{TELEGRAM_BOT_API_URL}sendMessage"
            json_data = {"chat_id": recipient_id, "text": texts.pop(0), "parse_mode": "HTML"}
            await sending_request(url, json=json_data)
        else:
            print(f"[Telegram] Sequence item is not valid for {item}")
            
async def send_invoice(recipient_id: Union[Text, Any]):
    await bot.send_invoice(recipient_id,
                           title='Working Time Machine',
                           description='Want to visit your great-great-great-grandparents?'
                                       ' Make a fortune at the races?'
                                       ' Shake hands with Hammurabi and take a stroll in the Hanging Gardens?'
                                       ' Order our Working Time Machine today!',
                           provider_token=PAYMENT_TOKEN,
                           currency='USD',
                           photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
                           photo_height=512,
                           photo_width=512,
                           photo_size=512,
                           is_flexible=True,
                           prices=[sample_price],
                           start_parameter='time-machine-example',
                           payload='HAPPY FRIDAYS COUPON')

async def get_telegram_file(file_id: Text):
    """Get a file from Telegram and store it locally."""
    url = f"{TELEGRAM_BOT_API_URL}getFile"
    json_data = {"file_id": file_id}
    response = await sending_request(url, json=json_data)
    response_json = json.loads(response)
    file_path = response_json["result"]["file_path"]
    return f"{TELEGRAM_BOT_FILE_URL}{file_path}"

async def save_downloaded_file(sender_id, file_url: Text):
    file = await bot.get_file(file_url)
    file_name = file.file_unique_id
    extension = file.file_path.split(".")[-1]

    # await bot.download_file(file.file_path, f"test.{extension}")
    await bot.download_file(file.file_path, f"photos/{sender_id}/input/{file_name}.{extension}")

    return f"photos/{sender_id}/input/{file_name}.{extension}"

    # response = await sending_request_file(file_url, method="GET")
    # file_name = file_url.split("/")[-1]
    # extension = file_name.split(".")[-1]
    # save_path = f"photos/{sender_id}/{file_id}.{extension}"
    # with open(save_path, "wb") as f:
    #     f.write(response)

def define_type(request_dict):
    if request_dict.get('message', {}).get('photo', {}):
        return 'photo'
    elif request_dict.get('message', {}).get('text', {}):
        return 'text'
    elif request_dict.get('message', {}).get('video', {}):
        return 'video'
    else:
        return 'unknown'

async def main_program(request_dict):
    msg_user_id = request_dict.get('message', {}).get('from', {}).get('id', "")
    msg_id = request_dict.get('message', {}).get('message_id', "")
    msg_date = request_dict.get('message', {}).get('date', "")
    msg_type = define_type(request_dict)
    msg_text = request_dict.get('message', {}).get('text', "")
    msg_group_media_id = request_dict.get('message', {}).get('group_media_id', "")
    msg_user_name = request_dict.get('message', {}).get('from', {}).get('first_name',{})

    if msg_user_id not in users.keys():
        users[msg_user_id] = User(msg_user_id, msg_id, msg_date, msg_type, msg_text, msg_group_media_id)
    else:
        users[msg_user_id].update_msg(msg_id, msg_date, msg_type, msg_text, msg_group_media_id)

    user = users[msg_user_id]
    
    # Change the state in the flow with this function
    await state_handler.state_handler(user, request_dict, NGROK_URL,msg_user_name)

if __name__ == "__main__":
    app.run(
        host = "0.0.0.0",
        port = 11111,
        debug = True,
        workers=1
    )