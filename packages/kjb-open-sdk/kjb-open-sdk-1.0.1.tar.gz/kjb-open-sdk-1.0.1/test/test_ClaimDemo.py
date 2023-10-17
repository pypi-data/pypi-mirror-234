"""
@version: python3.11
@author: 章鱼
@time: 2023/10/11
@des: 演示理赔相关场景
"""

from src.kjingbaoSDK.ov.claim import *
from src.kjingbaoSDK.ov.KJBConfig import KJBConfig
from src.kjingbaoSDK.api.ClaimApiUtils import ClaimApiUtils


class TestClaimDemo:
    def setup_class(self):
        # 跨境堡提供的SecretId
        self.SECRET_ID = "100054"
        # 跨境堡提供的SecretKey
        self.SECRET_KEY = "99999999"
        # 服务域名
        self.SERVICE_HOST = "testapi.kjingbao.com"
        # 查看理赔信息URL
        self.CLAIM_SHARE_URL = f"http://{self.SERVICE_HOST}/claim-ds/open/share"
        # 新建理赔URL
        self.CLAIM_LINK_URL = f"http://{self.SERVICE_HOST}/claim-ds/open/createClaimLink"

    def test_create_policy_link(self):
        """
        创建理赔信息
        """

        trackingNo = "YD1212e12e12e12e"
        kjbAccount = '13777770001'
        thirdPartAccount = 'admin'

        claimLinkParamDTO = ClaimLinkParamDTO(trackingNo=trackingNo, kjbAccount=kjbAccount, thirdPartAccount=thirdPartAccount)
        config = KJBConfig(self.SECRET_ID, self.SECRET_KEY, self.CLAIM_LINK_URL)
        try:
            r = ClaimApiUtils.createClaimLink(claimLinkParamDTO, config)
            print(r.text)
        except IOError as e:
            print(e)

    def test_claim_share(self):
        """
        查看理赔信息
        """

        POLICY_NO = "xxxxxxxxxxx"
        TRACKING_NO = "YD6123012331223312"

        claimShare = ClaimShareDTO(policyNo=POLICY_NO,
                                   trackingNo=TRACKING_NO,
                                   showReportInfo=True,
                                   showCliamStatusInfo=True,
                                   showSurveyStatusInfo=True,
                                   showAdjustmentInfo=True,
                                   showSurveyResultInfo=True,
                                   showClaimAmountInfo=True,
                                   showClaimDataInfo=True)
        config = KJBConfig(self.SECRET_ID, self.SECRET_KEY, self.CLAIM_SHARE_URL)
        try:
            r = ClaimApiUtils.share(claimShare, config)
            print(r.json())
            assert r.json()['success']
        except IOError as e:
            print(e)
