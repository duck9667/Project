# main.py

...

from slackhandler import Slack

...

# 슬랙 생성
SLACK_TOKEN = '슬랙 토큰'
SLACK_CHANNEL = '채널 이름'
SLACK_SENDER_NAME = '보낸이 이름'
slack = Slack(token=SLACK_TOKEN, channel=SLACK_CHANNEL, username=SLACK_SENDER_NAME)


import datetime

...

# 삭제 파일, 생성된 파일 리스트 관련 메세지 생성
total_file_update_info_text = gen_total_file_update_info_text(deleted_file_list, new_file_list)
# 파일별 달라진점 객체 리스트 문자 데이터 생성
file_diff_info_text = gen_diff_row_info_text(file_diff_info_list)

result_msg = f'{datetime.now()}\n크롤러 결과============================================\n\n\n\n'
if total_file_update_info_text is None and file_diff_info_text is None:
    result_msg += '변경된 내용이 없습니다.'
else:
    if total_file_update_info_text is not None:
        result_msg += f'{total_file_update_info_text}\n\n\n\n\n'

    if file_diff_info_text is not None:
        result_msg += f'{file_diff_info_text}\n\n\n'
result_msg += '====================================================='

slack.send_slack_msg(text=result_msg)