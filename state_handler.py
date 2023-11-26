from main import send_messages, save_downloaded_file, send_invoice
from avatar_curls import fast_avatar_curl, train_avatar_curl
from api_call.api_call import api_new_request
from csv_files.save_csv import save_to_csv

STATES =  ['start', 'options']

STATES_new_request =  ["upload_image","run_docker","process_request","finish"]
STATES_followup_request =  ["upload_image","name_email","run_docker","request_process","finish"]


async def state_handler(user, request_dict, NGROK_URL,msg_user_name=None):
    
    if user.download_flag:
        if user.type == 'photo':
                download_path = await save_downloaded_file(
                    user.id,
                    request_dict.get('message', {}).get('photo', {})[-1].get('file_id', ''))
                user.files_link.append(request_dict.get('message', {}).get('photo', {})[-1].get('file_id', ''))

    elif user.state == STATES[0] or user.text=='reset':
        if user.text.lower() in ['/start','hi','help','reset']:
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Welcome, please select whether you want to make a new request or followup your prev. request . \n\t1.Make a new request \n\t2.followup your prev. request'],
                images=[]
            )
            user.update_flow(STATES[1])
            
    elif user.state == STATES[1]:
        if user.text in ['1','new']:
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Well. please insert ypur image(s) or video'],
                images=[]
            )
            user.service_type= "new_request"
            user.update_flow(STATES_new_request[0])
            
        elif user.text in ['2','prev']:
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Please insert your image/ picture'],
                # images=[f'{NGROK_URL}/teasers/train_avatar.png']
            )
            user.service_type= "follow_up_request"
            user.update_flow(STATES_followup_request[0])
        else:
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Sorry, please select between \n\t1.Make a new request \n\t2.followup your prev.request'],
                images=[]
            )

    elif user.service_type ==  "new_request" :
        if user.state == STATES_new_request[0]:
            if user.type == 'photo':
                download_path = await save_downloaded_file(
                    user.id,
                    request_dict.get('message', {}).get('photo', {})[-1].get('file_id', ''))
                user.files_link.append(request_dict.get('message', {}).get('photo', {})[-1].get('file_id', ''))
                if request_dict.get('message', {}).get('group_media_id', {}) :
                    user.download_flag = True
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Please enter your name and email.'],
                images=[]
            )
            user.update_flow(STATES_new_request[1])
        elif user.state == STATES_new_request[1]:
            if user.type == 'text':
                user.mail_name = user.text # Validation check with llm 
                user.download_flag = False
                # Run Docker 
                output_paths = api_new_request(user.id)
                # save informations. 
                save_to_csv(user,msg_user_name)
                
                await send_messages(
                    recipient_id=user.id,
                    sequence=['text','image'],
                    texts=['Your request has been recieved.'],
                    images=[f'{NGROK_URL}/teasers/fast_avatar.png']
                    # images=[f'{NGROK_URL}{path}' for path in output_paths]
                    # images=[f'{NGROK_URL}/home/yaghoubian/yaghoubian/telegram_bot/photos/163558016/output/AQADesQxG2AiGVN-.jpg']
                    
                )
                user.user_reset()

    elif user.service_type ==  "follow_up_request" :
        if user.state == STATES_followup_request[2]:
            pass




    # elif user.state == STATES[2]:
    #     if user.text == '1':
    #         user.theme = 'business'
    #     elif user.text == '2':
    #         user.theme = 'sport'
    #     elif user.text == '3':
    #         user.theme = 'casual'
    #     else:
    #         user.theme = 'other'
        
    #     await send_messages(
    #             recipient_id=user.id,
    #             sequence=['text', 'image'],
    #             texts=['Send a photo'],
    #             images=[f'{NGROK_URL}/teasers/fast_avatar.png']
    #         )
    #     user.update_flow(STATES[4])

    # elif user.state == STATES[3]:
    #     if user.text == '1':
    #         user.theme = 'business'
    #     elif user.text == '2':
    #         user.theme = 'sport'
    #     elif user.text == '3':
    #         user.theme = 'casual'
    #     else:
    #         user.theme = 'other'
        
    #     await send_messages(
    #             recipient_id=user.id,
    #             sequence=['text', 'image'],
    #             texts=['Send 5 photos'],
    #             images=[f'{NGROK_URL}/teasers/train_avatar.png']
    #         )
    #     user.update_flow(STATES[5])

    # elif user.state == STATES[4]:
    #     if user.type == 'photo':
    #         download_path = await save_downloaded_file(
    #             user.id,
    #             request_dict.get('message', {}).get('photo', {})[-1].get('file_id', '')
    #         )

    #         # if fast_avatar_curl('test.jpg', user.theme):
    #         await send_messages(
    #             recipient_id=user.id,
    #             sequence=['image'],
    #             texts=[],
    #             images=[f'{NGROK_URL}/{download_path}']
    #             # images=[f'{NGROK_URL}/teasers/fast_avatar.png']
    #         )

    #         await send_messages(
    #             recipient_id=user.id,
    #             sequence=['text'],
    #             texts=['You can try again with please Select: \n1.Fast Avatar\n2.Train Avatar'],
    #             images=[]
    #         )
    #         user.update_flow(STATES[1])

    #     else:
    #         await send_messages(
    #             recipient_id=user.id,
    #             sequence=['text'],
    #             texts=['Send a photo'],
    #             images=[]
    #         )

    # elif user.state == STATES[5]:
    #     if user.type == 'photo':
    #         download_path = await save_downloaded_file(
    #             user.id,
    #             request_dict.get('message', {}).get('photo', {})[-1].get('file_id', '')
    #         )    
    #         user.update_num()

    #         if user.num == 5:
    #             await send_messages(
    #                 recipient_id=user.id,
    #                 sequence=['text'],
    #                 texts=['photo received, waiting ...'],
    #                 images=[]
    #             )
                
    #             if train_avatar_curl():
    #                 await send_messages(
    #                     recipient_id=user.id,
    #                     sequence=['image'],
    #                     texts=[],
    #                     images=[f'{NGROK_URL}/{download_path}']
    #                 )
    #             user.update_flow(STATES[1])

    #     else:
    #         await send_messages(
    #             recipient_id=user.id,
    #             sequence=['text'],
    #             texts=['Send the rest of the photos'],
    #             images=[]
    #         )
