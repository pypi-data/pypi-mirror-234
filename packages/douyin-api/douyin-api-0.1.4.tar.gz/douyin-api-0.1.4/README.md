# douyin-api

## 说明

抖音官网接口

开发者文档：https://developer.open-douyin.com/docs-page

移动/网站应用文档指引：https://developer.open-douyin.com/docs/resource/zh-CN/dop/overview/usage-guide


## 接口演示

```python
from douyin_api import DouYin
from douyin_api.utils import Timer
from douyin_api.tool import get_video_id_by_short_url, get_iframe_data_by_video_id

from _.不要对外公开 import client_key, client_secret, redirect_uri, access_token, open_id, item_id, refresh_token, short_url

正式环境 = 'https://open.douyin.com'

沙盒环境 = 'https://open-sandbox.douyin.com'

if __name__ == '__main__':
    with Timer() as timer:
        ...
        d = DouYin(client_key, client_secret, 正式环境)

        # print(d.client_token())

        scope = 'user_info,video.list.bind,video.data.bind'
        scope += ',trial.whitelist'  # 测试的时候需要这个权限

        # renew_refresh_token 用户授权续期
        print(d.get_permission_code_url(scope=scope, redirect_uri=redirect_uri))

        # print(d.access_token(code='9c1592704acfd7dbuQbpWj9u7EsBV8KuDbPT'))

        # 刷新 refresh_token 的有效期
        # print(d.renew_refresh_token(refresh_token))

        # 刷新 refresh_token 的有效期
        # print(d.refresh_token(refresh_token))

        # 设置用户access_token，有些接口需要这个才能访问
        d.set_access_token(access_token, open_id)

        # print(d.userinfo())

        # 分页获取用户所有视频的数据，返回的数据是实时的
        # print(d.video_list(cursor=0, count=10))

        # 查看设置用户access_token是否影响client_token接口访问
        # print(d.client_token())

        # video_id = get_video_id_by_short_url(short_url)
        # print('从抖音短连接获取视频id', video_id)
        # # 通过VideoID获取IFrame代码
        # if video_id:
        #     print(get_iframe_data_by_video_id(video_id))

        # 查询用户特定视频的数据，如点赞数、播放数等，返回的数据是实时的
        # print(d.video_data(ids=[item_id]))
        # print(d.video_data(ids=[str(video_id)], use_item_ids=False))

```

