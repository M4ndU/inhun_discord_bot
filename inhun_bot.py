import discord
import asyncio
import datetime
from scrapture import *
from datematch import *

client = discord.Client()

#명령어 목록 안내
Command_list = "```css\n$help : '도움말'\n$V : '버전 정보'\n$안녕 : '안녕'\n$t : '오늘 날짜'\n$g : '급식'```"

#급식안내
meal_notice = "```css\n[안내] 가급적 오늘과 오늘 이후의 날짜만 요청해 주세요.\n[안내] 한 달 이후의 경우 정보가 없을 수도 있습니다.\n[안내] 날짜와 급식이 맞지 않는 경우 개발자에게 문의해주세요.\n[주의] 10월 31일인 경우 1031 로 보낼 것.\n```"
#[안내] 가급적 오늘과 오늘 이후의 날짜만 요청해 주세요.
#[안내] 한 달 이후의 경우 정보가 없을 수도 있습니다.
#[안내] 날짜와 급식이 맞지 않는 경우 개발자에게 문의해주세요.
#[주의] 10월 31일인 경우 1031 로 보낼 것.

#추가 공지사항
plus_meal_notice = "```css\n[안내] 11월 15일부터 석식이 없으며 15일과 16일은 중식도 없습니다.\n```"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('$help'):
        await client.send_message(message.channel, Command_list)

    elif message.content.startswith('$V'):
        await client.send_message(message.channel, "버전 : 1.0.4")

    elif message.content.startswith('$안녕'):
        await client.send_message(message.channel, "안녕")

    elif message.content.startswith('$t'):
        #시간
        dt = datetime.datetime.now()
        local_date = dt.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        await client.send_message(message.channel, local_date)

    elif message.content.startswith('$g'):
        await client.send_message(message.channel, meal_notice)
        await client.send_message(message.channel, plus_meal_notice + '날짜를 보내주세요...')

        def date_check(m):
            return m.content.isdigit()

        meal_date = await client.wait_for_message(timeout=10.0, author=message.author, check=date_check)

        if meal_date is None:
            longtimemsg = '오랫동안 입력하지 않아 취소했음'
            await client.send_message(message.channel, longtimemsg)
            return
        if int(meal_date.content) <= 1029 or int(meal_date.content) > 1231:
            await client.send_message(message.channel, '10월 29일 이전 이거나 잘못된 값입니다.')
            #1년 지나면 1029에서 0101로 변경
        else:
            await client.send_message(message.channel, '기다려봐...')
            meal_date = int(meal_date.content)

            lunch = lunch_match(meal_date)
            dinner = dinner_match(meal_date)

            if (lunch != 0 and dinner != 0):

                l_diet = get_diet(lunch)
                d_diet = get_diet(dinner)
            else:
                l_diet = "급식 정보가 없습니다."
                d_diet = ":("

            await client.send_message(message.channel, l_diet)
            await client.send_message(message.channel, d_diet)

client.run('[your_token_here]')
#
