import json
import sys
from flask import Flask

sys.path.append("../../feishu")
from kl_feishu import FeiShuHelp, CardMsgRoot, CardListenerHandler, CardReq
from zyx_tools import OtherTool

import logging

feishu_appid = "cli_a37e9b540bb8100d"
feishu_appsecret = "4YNiJZQBaFkazFUL8L9r5elryb11icqp"
feishu = FeiShuHelp(feishu_appid, feishu_appsecret)


# 向一个群发文本消息
def test_sendmsg_togroup():
    group_id = "oc_7353a1bef0ac8ad0785d3f8e195217e6"
    send_text = "你好"
    feishu.send_msg_to_group(group_id, send_text)


# 向某一个用户发文本消息
def test_sendmsg_tomember():
    member_id = "ou_538df4c47a4008b2c51258b00d9f9742"
    sendtext = "ddd"
    feishu.send_msg_to_user(member_id, sendtext)


# 向一个用户发送卡片信息
def test_sendcardmsg_tomember():
    member_id = "ou_538df4c47a4008b2c51258b00d9f9742"
    with open("ok_msg.json", "r", encoding="UTF-8") as fb:
        send_json = json.load(fb)
        send_data = CardMsgRoot.parse_obj(send_json)
    send_data.header.title.content = f"正常"
    send_data.json(exclude_none=True)
    feishu.send_card_to_user(member_id, send_data.dict())


# 向一个群发送卡片信息
def test_sendcardmsg_toGroup():
    group_id = "oc_7353a1bef0ac8ad0785d3f8e195217e6"
    with open("ok_msg.json", "r", encoding="UTF-8") as fb:
        send_json = json.load(fb)
        send_data = CardMsgRoot.parse_obj(send_json)
    send_data.header.title.content = f"正常"
    send_data.json(exclude_none=True)
    feishu.send_card_to_group(group_id, send_data.dict())


# 获取群信息
def test_getGroupinfo():
    group_name = "Bugly报警"
    groupinfo = feishu.get_group_info_by_name(group_name)
    print(f"获取到的基本信息:{groupinfo}")
    feishu.init_group_user_list(groupinfo)
    print(f"获取到的用户信息:{groupinfo}")
    return groupinfo


# 获取群中一个用户的信息
def test_getGroupUserInfo():
    group_name = "Bugly报警"
    user_name = "张雨鑫"
    groupinfo = feishu.get_group_info_by_name(group_name)
    userinfo = feishu.get_group_user_info(groupinfo, user_name)
    print(f"用户信息:{userinfo}")


def test_server():
    feishu_server = Flask(__name__)

    def process_info(cardinfo: CardReq):
        print(
            f"cardinfo:{cardinfo.json(exclude_none=True,ensure_ascii=False,indent=4)}"
        )

    handler_server = CardListenerHandler(
        "eqaN7fyB1ki00TNoT82a8feBvvtz8jyD", "", process_info
    )

    @feishu_server.route("/", methods=["POST"])
    def card():
        logging.getLogger().setLevel(logging.DEBUG)
        return handler_server.process()

    feishu_server.run(port=8080, debug=False)


if __name__ == "__main__":
    print("start test")
    OtherTool.init_log(level=logging.DEBUG)
    # test_sendmsg_togroup()
    # test_sendmsg_tomember()
    # test_sendcardmsg_tomember()
    # test_sendcardmsg_toGroup()
    # test_getGroupinfo()
    # test_getGroupUserInfo()
    test_server()
