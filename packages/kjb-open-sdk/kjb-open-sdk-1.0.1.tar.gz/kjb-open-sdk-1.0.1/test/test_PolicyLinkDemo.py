"""
@version: python3.11
@author: 章鱼
@time: 2023/10/11
@des: 演示保单查看接口
"""

from src.kjingbaoSDK.ov.policy import *
from src.kjingbaoSDK.ov.KJBConfig import KJBConfig
from src.kjingbaoSDK.api.PolicyApiUtils import PolicyApiUtils


class TestPolicyLinkDemo:
    def setup_class(self):
        # 跨境堡提供的SecretId
        self.SECRET_ID = "1001275"
        # 跨境堡提供的SecretKey
        self.SECRET_KEY = "76c8ad8e-2d75-493a-bd61-820ee5df59e8"
        # 服务域名
        self.SERVICE_HOST = "testapi.kjingbao.com"
        self.POLICY_LINK_URL = f"http://{self.SERVICE_HOST}/cbi/policy/v2/createPolicyLink"

    def test_create_policy_link(self):
        policyRequest = PolicyLinkParamDTO(trackingNo='track6100001989', kjbAccount='18870000001', thirdPartAccount='admin')
        config = KJBConfig(self.SECRET_ID, self.SECRET_KEY, self.POLICY_LINK_URL)
        try:
            r = PolicyApiUtils.createPolicyLink(policyRequest, config)
            print(r.json())
            assert r.json()['success']
        except IOError as e:
            print(e)
