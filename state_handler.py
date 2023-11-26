from main import send_messages, save_downloaded_file, send_invoice
from avatar_curls import fast_avatar_curl, train_avatar_curl

STATES =  ['start', 'options', 'fast_theme', 'train_theme', 'fast', 'train', 'result', 'payment']

async def state_handler(user, request_dict, NGROK_URL):
    if user.state == STATES[0]:
        if user.text == '/start':
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Welcome to Avatar Bot. Please Select: \n1.Fast Avatar \n2.Train Avatar'],
                images=[]
            )
            user.update_flow(STATES[1])
            
            # await send_invoice(user.id)

    elif user.state == STATES[1]:
        if user.text == '1':
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Chosen theme: \n1.Business 2.Sport 3.Casual 4.Other'],
                images=[]
            )

            user.update_flow(STATES[2])
            
        elif user.text == '2':
            await send_messages(
                recipient_id=user.id,
                sequence=['text', 'image'],
                texts=['Send 5 photos'],
                images=[f'{NGROK_URL}/teasers/train_avatar.png']
            )
            user.update_flow(STATES[3])
        
        else:
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Please Select: \n1.Fast Avatar \n2.Train Avatar'],
                images=[]
            )

    elif user.state == STATES[2]:
        if user.text == '1':
            user.theme = 'business'
        elif user.text == '2':
            user.theme = 'sport'
        elif user.text == '3':
            user.theme = 'casual'
        else:
            user.theme = 'other'
        
        await send_messages(
                recipient_id=user.id,
                sequence=['text', 'image'],
                texts=['Send a photo'],
                images=[f'{NGROK_URL}/teasers/fast_avatar.png']
            )
        user.update_flow(STATES[4])

    elif user.state == STATES[3]:
        if user.text == '1':
            user.theme = 'business'
        elif user.text == '2':
            user.theme = 'sport'
        elif user.text == '3':
            user.theme = 'casual'
        else:
            user.theme = 'other'
        
        await send_messages(
                recipient_id=user.id,
                sequence=['text', 'image'],
                texts=['Send 5 photos'],
                images=[f'{NGROK_URL}/teasers/train_avatar.png']
            )
        user.update_flow(STATES[5])

    elif user.state == STATES[4]:
        if user.type == 'photo':
            download_path = await save_downloaded_file(
                user.id,
                request_dict.get('message', {}).get('photo', {})[-1].get('file_id', '')
            )

            # if fast_avatar_curl('test.jpg', user.theme):
            await send_messages(
                recipient_id=user.id,
                sequence=['image'],
                texts=[],
                images=[f'{NGROK_URL}/{download_path}']
                # images=[f'{NGROK_URL}/teasers/fast_avatar.png']
            )

            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['You can try again with please Select: \n1.Fast Avatar\n2.Train Avatar'],
                images=[]
            )
            user.update_flow(STATES[1])

        else:
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Send a photo'],
                images=[]
            )

    elif user.state == STATES[5]:
        if user.type == 'photo':
            download_path = await save_downloaded_file(
                user.id,
                request_dict.get('message', {}).get('photo', {})[-1].get('file_id', '')
            )    
            user.update_num()

            if user.num == 5:
                await send_messages(
                    recipient_id=user.id,
                    sequence=['text'],
                    texts=['photo received, waiting ...'],
                    images=[]
                )
                
                if train_avatar_curl():
                    await send_messages(
                        recipient_id=user.id,
                        sequence=['image'],
                        texts=[],
                        images=[f'{NGROK_URL}/{download_path}']
                    )
                user.update_flow(STATES[1])

        else:
            await send_messages(
                recipient_id=user.id,
                sequence=['text'],
                texts=['Send the rest of the photos'],
                images=[]
            )
