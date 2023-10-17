"""
@version: python3.11
@author: 章鱼
@time: 2023/10/12
@des: 传统货运获取投保链接API案例
"""
import datetime
from src.kjingbaoSDK.constant import *
from src.kjingbaoSDK.ov.policy import *
from src.kjingbaoSDK.ov.KJBConfig import KJBConfig
from src.kjingbaoSDK.api.PolicyApiUtils import PolicyApiUtils


class TestTraditionalPolicyApiDemo:
    def setup_class(self):
        # 跨境堡提供的SecretId
        self.SECRET_ID = "1001275"
        # 跨境堡提供的SecretKey
        self.SECRET_KEY = "76c8ad8e-2d75-493a-bd61-820ee5df59e8"
        # 服务域名
        self.SERVICE_HOST = "testapi.kjingbao.com"
        self.DRATT_URL = f"http://{self.SERVICE_HOST}/cbi/policy/v2/createTraditionalDraftLink"
        self.BATCH_DRATT_URL = f"http://{self.SERVICE_HOST}/cbi/policy/v2/createTraditionalBatchDraftLink"
        self.file_url = "https://kjb-test-1253287739.cos.ap-guangzhou.myqcloud.com/policy/2020/08/10/cd330189-9f3a-4ed3-804c-42f981e89b37/d00fe1af66beee50286f845ba692d815.jpg"

    def test_create_draft(self):
        policyRequest = PolicyApiDTO(insuredName='测试有限公司',  # 被保险人
                                     trackingNo='TEST001',  # 设置原单号
                                     transportModeCode=TransportMode.SEA.value,  # 运输方式
                                     transportTool='LH721',  # 运输工具及航次
                                     unrestRisk=True,  # 是否暴动保障
                                     warRisk=True,  # 仓至仓条款
                                     departureCountryCode='CHN',  # 起运国
                                     departureAddress='SHENZHEN',  # 起运地
                                     destinationCountryCode='USA',  # 目的国
                                     destinationAddress='MEM 13292 E Holmes Rd',  # 目的地
                                     transferCountryCode='CHN',  # 中转国
                                     transferAddress='NINGBO',  # 中转地
                                     claimSite='赔付地',  # 赔付地
                                     creditNo='信用证号',  # 信用证号
                                     CreditLetter='信用证条款',  # 信用证条款
                                     departureDate=datetime.datetime.now(),  # 起运日期
                                     departureDateFlag=False,  # 起运日期显示方式
                                     blNo='020-48236661',  # 提单号
                                     invoiceNo='发票号',  # 发票号
                                     bargainNo='销售合同号',  # 销售合同号
                                     cargoValue=1111.11,  # 发票金额
                                     chargeableWeight=400.11,  # 公斤数（毛重)
                                     currencyCode=Currency.USD.value,  # 保单币种
                                     ratio=100,  # 投保比例 %
                                     cargoDesc='led灯1',  # 货物描述
                                     cargoCategoryCode=CargoCategoryTraditional.CARGO_CATEGORY_0301.value,  # 0301-玻璃制品
                                     packingCode='木箱',  # 包装类型 002--纸箱 CARTON
                                     packingQuantity=5,  # 包装数量
                                     cargoMarks='唛头',  # 唛头
                                     remark='Mark',  # 备注
                                     )
        # 险别信息对象 详情见基础数据<传统险险种信息>
        ir1 = InsuranceRiskApiDTO(kindName='海洋货物运输一切险条款', kindCode='012', mainFlag=True)
        list_risk = [ir1]
        policyRequest.insuranceRiskList = list_risk

        # 上传附件 FILE
        policyAttachmentApiDTO = PolicyAttachmentApiDTO(remake='nothing', type='guarantee_letter', url=self.file_url)
        attachments = [policyAttachmentApiDTO]
        policyRequest.attachmentList = attachments

        # 被保险人
        policyInsuredApiDTO = PolicyInsuredApiDTO(certificateType=CertificateType.PID.value,
                                                  certificateNo='330227100000000002')
        policyRequest.insuredInfo = policyInsuredApiDTO

        # 货主
        policyOwnerApiDTO = PolicyOwnerApiDTO(owner='货主名称',
                                              certificateType=CertificateType.PID.value,
                                              certificateNo='330227100000000002',
                                              mobile='18888888888')
        policyRequest.ownerInfo = policyOwnerApiDTO

        # 用户名(登录跨境堡的用户名), 两者二选一, 如果同时传, 以kjbAccount为准
        policyRequest.kjbAccount = "18870000001"
        policyRequest.thirdPartAccount = "admin"

        config = KJBConfig(self.SECRET_ID, self.SECRET_KEY, self.DRATT_URL)
        try:
            r = PolicyApiUtils.createDraftLink(policyRequest, config)
            print(r.json())
            assert r.json()['success']
        except IOError as e:
            print(e)

    def test_create_batch_draft(self):
        policyRequest = PolicyApiDTO(insuredName='测试有限公司',  # 被保险人
                                     trackingNo='TEST001',  # 设置原单号
                                     transportModeCode=TransportMode.SEA.value,  # 运输方式
                                     transportTool='LH721',  # 运输工具及航次
                                     unrestRisk=True,  # 是否暴动保障
                                     warRisk=True,  # 仓至仓条款
                                     departureCountryCode='CHN',  # 起运国
                                     departureAddress='SHENZHEN',  # 起运地
                                     destinationCountryCode='USA',  # 目的国
                                     destinationAddress='MEM 13292 E Holmes Rd',  # 目的地
                                     transferCountryCode='CHN',  # 中转国
                                     transferAddress='NINGBO',  # 中转地
                                     claimSite='赔付地',  # 赔付地
                                     creditNo='信用证号',  # 信用证号
                                     CreditLetter='信用证条款',  # 信用证条款
                                     departureDate=datetime.datetime.now(),  # 起运日期
                                     departureDateFlag=False,  # 起运日期显示方式
                                     blNo='020-48236661',  # 提单号
                                     invoiceNo='发票号',  # 发票号
                                     bargainNo='销售合同号',  # 销售合同号
                                     cargoValue=1111.11,  # 发票金额
                                     chargeableWeight=400.11,  # 公斤数（毛重)
                                     currencyCode=Currency.USD.value,  # 保单币种
                                     ratio=100,  # 投保比例 %
                                     cargoDesc='led灯1',  # 货物描述
                                     cargoCategoryCode=CargoCategoryTraditional.CARGO_CATEGORY_0301.value,  # 0301-玻璃制品
                                     packingCode='木箱',  # 包装类型 002--纸箱 CARTON
                                     packingQuantity=5,  # 包装数量
                                     cargoMarks='唛头',  # 唛头
                                     remark='Mark',  # 备注
                                     )
        # 险别信息对象 详情见基础数据<传统险险种信息>
        ir1 = InsuranceRiskApiDTO(kindName='海洋货物运输一切险条款', kindCode='012', mainFlag=True)
        list_risk = [ir1]
        policyRequest.insuranceRiskList = list_risk

        # 上传附件 FILE
        policyAttachmentApiDTO = PolicyAttachmentApiDTO(remake='nothing', type='guarantee_letter', url=self.file_url)
        attachments = [policyAttachmentApiDTO]
        policyRequest.attachmentList = attachments

        # 被保险人
        policyInsuredApiDTO = PolicyInsuredApiDTO(certificateType=CertificateType.PID.value,
                                                  certificateNo='330227100000000002')
        policyRequest.insuredInfo = policyInsuredApiDTO

        # 货主
        policyOwnerApiDTO = PolicyOwnerApiDTO(owner='货主名称',
                                              certificateType=CertificateType.PID.value,
                                              certificateNo='330227100000000002',
                                              mobile='18888888888')
        policyRequest.ownerInfo = policyOwnerApiDTO

        policyBatchApiDTO = PolicyBatchApiDTO(policyList=[policyRequest, policyRequest],
                                              kjbAccount="18870000001",
                                              thirdPartAccount="admin"
                                              )
        config = KJBConfig(self.SECRET_ID, self.SECRET_KEY, self.BATCH_DRATT_URL)
        try:
            r = PolicyApiUtils.createBatchDraftLink(policyBatchApiDTO, config)
            print(r.json())
            assert r.json()['success']
        except IOError as e:
            print(e)
