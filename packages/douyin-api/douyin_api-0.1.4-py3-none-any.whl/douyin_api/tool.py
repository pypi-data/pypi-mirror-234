import re

import requests


def get_video_id_by_short_url(short_url):
    """
    从抖音短连接获取视频id
    """
    # 使用正则表达式提取视频id
    pattern = r"/video/(\d+)/"
    response = requests.head(short_url, allow_redirects=True)
    if response.status_code == 200:
        actual_url = response.url
        match = re.search(pattern, actual_url)
        if match:
            video_id = match.group(1)
            return video_id


def get_iframe_data_by_video_id(video_id):
    """
    该接口用于通过视频 VideoID 获取 IFrame 代码。视频 VideoID 可以通过 PC 端视频播放地址中获取
    该接口无需申请权限。

    注意：
    该接口以 https://open.douyin.com/ 开头
    请求地址
    GET /api/douyin/v1/video/get_iframe_by_video

    docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/iframe-player/get-iframe-by-video
    """
    url = f"https://open.douyin.com/api/douyin/v1/video/get_iframe_by_video?video_id={video_id}"
    response = requests.get(url, )
    if response.status_code == 200:
        response_data = response.json()
        data = response_data["data"]
        # print(url, response_data)
        return data
    else:
        print("get_iframe_data_by_video_id Error:", response.status_code)
        return None
