# encoding: utf-8
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,VideoSendMessage,ImageSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import requests
import os
import main
import datetime
import pandas as pd
import json
import picture_list



app = Flask(__name__)

# Channel_access_token = 'NjzkMRXNNUNqrkRyEoV2JYcNwpm4vQZPZNyCxEDpa8hwAbLXHVNwwWwc6iQAbwyYmmzUC+FBoBjd7ABtM9vWve3pPTbXUKRaT8lebv3FiHwoJ1LKymhW8eBTv76JTOyQ2rWISOoFhhUucEeU2HPWFgdB04t89/1O/w1cDnyilFU='
# Channel_secret ='d83d1fe4fd73b7f1d365c414210bf7e3'

Channel_access_token = 'Ml9DEHV6aYuPgCYlv1K0YL6TOq7SXhXb5A7OvxN0S/1zPqRXW8VdX3a3gKjL0yb0n3xxX/pvzI3qbJmbwYdtMlNMSwKww25ls21P3V2jM9+IoTtf659T+2QE17ZlDW3aygcYKNtQvO0uVXjWwSiOBQdB04t89/1O/w1cDnyilFU='
Channel_secret ='f44a96e298ad1442aa5f6935da4a7f3a'


picture_list.richmenu(Channel_access_token)

# you can replace by load env file
handler = WebhookHandler(Channel_secret) 
line_bot_api = LineBotApi(Channel_access_token) 


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
# 檢查 CSV 檔案是否存在
    new_user_id = event.source.user_id
    welcome_message = "您好~歡迎您!\n!!!!!韭菜沒有輸!!!!!"
    line_bot_api.push_message(new_user_id, TextSendMessage(text=welcome_message))

    sticker_message = StickerSendMessage(
        package_id='446',  # 貼圖包 ID，可以在 Line Developer Console 中取得
        sticker_id='2003'    # 貼圖 ID，可以在 Line Developer Console 中取得
    )
    line_bot_api.push_message(new_user_id, sticker_message)

    return "OK"



# 使用者狀態字典，用來記錄每個使用者的狀態
user_states = {}
# ========== 處理使用者訊息 ==========
@handler.add(MessageEvent, message=TextMessage)  
def handle_text_message(event):
    today = datetime.date.today()
    input_date = today.strftime("%Y%m%d")
    user_id = event.source.user_id
    msg = event.message.text
       # 檢查使用者是否有狀態，如果沒有，設置為初始狀態
    if user_id not in user_states:
        user_states[user_id] = "INITIAL"


    if user_states[user_id] == "INITIAL":
        if(msg == "搜尋個股"):
            line_bot_api.push_message(user_id,TextSendMessage(text=f"請告訴我您想查詢的股票代碼?"))
            user_states[user_id] = "ASK_stock_inf"

        elif(msg == "搜尋產業"):
            user_states[user_id] = "ASK_stock_industry"
            industries = main.select_each_type()
            num_industries = len(industries)

            # 每三個一組分類，限制每個 CarouselTemplate 中的選單數量不超過 10 個
            carousel_columns = []
            for i in range(0, min(num_industries, 30), 3):
                # 確保每個選單最多只有三個產業
                column = CarouselColumn(
                    title="~~~請選擇產業名稱~~~",
                    text='賺錢就是這麼簡單',
                    actions=[]
                )
                for j in range(3):
                    if i + j < num_industries:
                        action = MessageAction(
                            label=industries[i + j],
                            text=industries[i + j]
                        )
                        column.actions.append(action)

                carousel_columns.append(column)

            # 使用 CarouselTemplate 包含所有的選單
            carousel_template = TemplateSendMessage(
                alt_text='CarouselTemplate',
                template=CarouselTemplate(columns=carousel_columns)
            )
            line_bot_api.push_message(user_id, carousel_template)

            if(num_industries > 30):
                how_many = num_industries - 30
                # 每三個一組分類，限制每個 CarouselTemplate 中的選單數量不超過 10 個
                carousel_columns = []
                for i in range(0, min(how_many, 30), 3):
                    # 確保每個選單最多只有三個產業
                    column = CarouselColumn(
                        title="~~~請選擇產業名稱~~~",
                        text='賺錢就是這麼簡單',
                        actions=[]
                    )
                    for j in range(3):
                        if i + j < how_many:
                            action = MessageAction(
                                label=industries[i + j],
                                text=industries[i + j]
                            )
                            column.actions.append(action)

                    carousel_columns.append(column)

                # 使用 CarouselTemplate 包含所有的選單
                carousel_template = TemplateSendMessage(
                    alt_text='CarouselTemplate',
                    template=CarouselTemplate(columns=carousel_columns)
                )
                line_bot_api.push_message(user_id, carousel_template)

        elif(msg == "搜尋飆股"):
            line_bot_api.push_message(user_id,TextSendMessage(text=f"我就知道你急了XD\n買在高點，覺得冷嗎?\n沒事，我給你幾支飆股!"))
            industries = main.select_each_type()
            num_industries = len(industries)
            new_path = main.upload_to_imgur(f"./上市股推薦.jpg")
            image_message = ImageSendMessage(
                original_content_url=new_path,
                preview_image_url=new_path
            )
            line_bot_api.push_message(user_id,TextSendMessage(text=f"!!!!!上市股票推薦!!!!!"))
            line_bot_api.push_message(user_id, image_message)

            new_path = main.upload_to_imgur(f"./上櫃股推薦.jpg")
            image_message = ImageSendMessage(
                original_content_url=new_path,
                preview_image_url=new_path
            )
            line_bot_api.push_message(user_id,TextSendMessage(text=f"!!!!!上櫃股票推薦!!!!!"))
            line_bot_api.push_message(user_id, image_message)

        elif(msg == "策略回測"):
            line_bot_api.push_message(user_id,TextSendMessage(text=f"告訴我您想測試的股票\nEX : 2330"))
            user_states[user_id] = "ASK_strategy"

        elif(msg == "TT選股"):
            new_path = main.upload_to_imgur(f"./choose_stock.jpg")
            image_message = ImageSendMessage(
                original_content_url=new_path,
                preview_image_url=new_path
            )
            line_bot_api.push_message(user_id,TextSendMessage(text=f"推薦股票!!!"))
            line_bot_api.push_message(user_id, image_message) 

        else:
            line_bot_api.push_message(user_id,TextSendMessage(text=f"{msg}?我不懂\n請先選擇下方按鈕"))


    elif user_states[user_id] == "ASK_stock_inf":
        def is_integer(input_str):
            # 檢查字串是否為空
            if not input_str:
                return False
            
            # 檢查字串是否只包含數字字符
            return input_str.isdigit()
        if(is_integer(str(msg))):
            status, msg_return, type = main.select_stock(str(msg))
            if(status == True):
                user_states[user_id] = "INITIAL"
                csv_file = "User_id.csv"
                file_exists = os.path.isfile(csv_file)
                # 如果 CSV 檔案不存在，則建立一個新的空的 DataFrame
                if not file_exists:
                    new_df = pd.DataFrame(columns=['user_id', 'stock_code'])
                    new_df.to_csv(csv_file,index = False)
                else:
                    # 如果 CSV 檔案存在，則讀取 CSV 檔案內容到 DataFrame
                    new_df = pd.read_csv(csv_file)
                # 檢查 DataFrame 中是否已經有相同的 user_id
                if user_id in new_df['user_id'].values:
                    # 如果已經有相同的 user_id，則更新對應的 name
                    new_df.loc[new_df['user_id'] == user_id, 'stock_code'] = msg
                else:
                    # 如果沒有相同的 user_id，則新增一筆資料到 DataFrame
                    new_data = {'user_id': user_id, 'stock_code': msg}
                    new_df = new_df.append(new_data, ignore_index=True)
                
                new_df.to_csv(csv_file, index=False)
                line_bot_api.push_message(user_id,TextSendMessage(text=f"{msg_return}"))
                new_path = main.upload_to_imgur(f"./{str(type)}/{str(msg)}/{str(msg)}.jpg")
                image_message = ImageSendMessage(
                    original_content_url=new_path,
                    preview_image_url=new_path
                )
                line_bot_api.push_message(user_id,TextSendMessage(text="近期一個月資料"))
                line_bot_api.push_message(user_id, image_message)
            else:
                line_bot_api.push_message(user_id,TextSendMessage(text=f"{msg_return}"))

        else:
            line_bot_api.push_message(user_id,TextSendMessage(text=f"請輸入數字!!"))

    elif user_states[user_id] == "ASK_stock_industry":
        user_states[user_id] = "INITIAL"
        new_path = main.upload_to_imgur(f"./相關產業排名/{str(msg)}.jpg")
        image_message = ImageSendMessage(
            original_content_url=new_path,
            preview_image_url=new_path
        )
        line_bot_api.push_message(user_id,TextSendMessage(text="相關產業排名"))
        line_bot_api.push_message(user_id, image_message)

    elif user_states[user_id] == "ASK_strategy":
        def is_integer(input_str):
            # 檢查字串是否為空
            if not input_str:
                return False
            
            # 檢查字串是否只包含數字字符
            return input_str.isdigit()
        if(is_integer(str(msg))):
            status, msg_return, type = main.select_stock(str(msg))
            if(status == True):
                line_bot_api.push_message(user_id,TextSendMessage(text=f"請輸入停利停損%數(0-100)\nEX : 5"))
                user_states[user_id] = "ASK_strategy_2"
                csv_file = "User_id.csv"
                file_exists = os.path.isfile(csv_file)
                # 如果 CSV 檔案不存在，則建立一個新的空的 DataFrame
                if not file_exists:
                    new_df = pd.DataFrame(columns=['user_id', 'stock_code'])
                    new_df.to_csv(csv_file,index = False)
                else:
                    # 如果 CSV 檔案存在，則讀取 CSV 檔案內容到 DataFrame
                    new_df = pd.read_csv(csv_file)
                # 檢查 DataFrame 中是否已經有相同的 user_id
                if user_id in new_df['user_id'].values:
                    # 如果已經有相同的 user_id，則更新對應的 name
                    new_df.loc[new_df['user_id'] == user_id, 'stock_code'] = msg
                else:
                    # 如果沒有相同的 user_id，則新增一筆資料到 DataFrame
                    new_data = {'user_id': user_id, 'stock_code': msg}
                    new_df = new_df.append(new_data, ignore_index=True)
                
                new_df.to_csv(csv_file, index=False)
            else:
                line_bot_api.push_message(user_id,TextSendMessage(text=f"{msg_return}"))
        else:
            line_bot_api.push_message(user_id,TextSendMessage(text=f"請輸入數字!!"))

    elif user_states[user_id] == "ASK_strategy_2":
        def is_integer(input_str):
            # 檢查字串是否為空
            if not input_str:
                return False
            
            # 檢查字串是否只包含數字字符
            return input_str.isdigit()
        if(is_integer(str(msg))):
            user_states[user_id] = "INITIAL"
            csv_file = "User_id.csv"
            file_exists = os.path.isfile(csv_file)
            # 如果 CSV 檔案不存在，則建立一個新的空的 DataFrame
            if not file_exists:
                new_df = pd.DataFrame(columns=['user_id', 'stock_code'])
                new_df.to_csv(csv_file,index = False)
            else:
                # 如果 CSV 檔案存在，則讀取 CSV 檔案內容到 DataFrame
                new_df = pd.read_csv(csv_file)

            new_df.to_csv(csv_file, index=False)
            stock_code = new_df['stock_code'].values[0]
            status, msg_return, type = main.select_stock(str(stock_code))

            main.strategy_k_d_moving(stock_code, msg)
            new_path = main.upload_to_imgur(f"./{str(type)}/{str(stock_code)}/strategy_k_d.jpg")
            image_message = ImageSendMessage(
                original_content_url=new_path,
                preview_image_url=new_path
            )
            line_bot_api.push_message(user_id,TextSendMessage(text="KD策略獲益統計"))
            line_bot_api.push_message(user_id, image_message)
        else:
            line_bot_api.push_message(user_id,TextSendMessage(text=f"請輸入數字!!"))




if __name__ == "__main__":
    app.run(debug=True)