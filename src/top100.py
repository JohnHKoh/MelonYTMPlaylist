import melon_retriever
from playlist_updater import PlaylistUpdater
from datetime import datetime
from zoneinfo import ZoneInfo
from chart import Chart

listName = "top100"
korea_time = datetime.now(ZoneInfo("Asia/Seoul"))
date_str = korea_time.strftime("%Y.%m.%d")
time = korea_time.replace(minute=0).strftime("%H:%M")
title = "Melon TOP100 - {} {}".format(date_str, time)
description = """
This is a chart reflecting usage over the past 24 hours and the past 1 hour. Usage is calculated with a weighting of 40% streaming and 60% downloads, and is updated every hour.
To prevent chart distortion, during low-traffic late night and early morning hours (01:00-07:00), a chart is published that reflects 100% of the past 24 hours of usage.
No ranking change information is provided in the 01:00 and 08:00 charts, where the weighting ratios differ.

최근 24시간 동안의 이용량과 최근 1시간의 이용량을 반영한 차트이며, 이용량은 스트리밍 40%+다운로드 60%를 기준으로 집계, 매 시간 업데이트 됩니다.
차트 왜곡을 막기 위해 이용자가 적은 심야와 이른 오전 01시~07시에는 최근 24시간 이용량을 100% 반영한 차트를 발행합니다.
반영 비율이 달라지는 01시·08시 차트에는 순위 변화를 제공하지 않습니다.

{playlist_url}

Updated for: {date}

This playlist is auto-generated.
View the code here: https://github.com/JohnHKoh/MelonYTMPlaylist
"""
PlaylistUpdater().update_playlist(Chart(listName, title, description, date_str))
