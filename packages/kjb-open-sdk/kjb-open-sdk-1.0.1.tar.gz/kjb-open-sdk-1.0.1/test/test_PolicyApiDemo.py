"""
@version: python3.11
@author: 章鱼
@time: 2023/10/08
@des: 演示保单新增和批量新增 (建议使用批量新增接口,支持单条批量新增)
"""
import datetime

from decimal import Decimal

from src.kjingbaoSDK.ov.policy.PolicyApiDTO import PolicyApiDTO
from src.kjingbaoSDK.constant import *
from src.kjingbaoSDK.ov.claim import *
from src.kjingbaoSDK.ov.policy import *
from src.kjingbaoSDK.ov.KJBConfig import KJBConfig
from src.kjingbaoSDK.api.PolicyApiUtils import PolicyApiUtils



class TestPolicyApiDemo:


    # 初始化case
    def setup_class(self):
        # 跨境堡提供的SecretId
        self.SECRET_ID = "1001275"
        # 跨境堡提供的SecretKey
        self.SECRET_KEY = "76c8ad8e-2d75-493a-bd61-820ee5df59e8"
        #服务域名
        SERVICE_HOST = "testapi.kjingbao.com"
        self.DRATT_URL = f"http://{SERVICE_HOST}/cbi/policy/v2/createDraftLink"
        self.BATCH_DRATT_URL = f"http://{SERVICE_HOST}/cbi/policy/v2/createBatchDraftLink"
        self.file_url = "https://kjb-test-1253287739.cos.ap-guangzhou.myqcloud.com/policy/2020/08/10/cd330189-9f3a-4ed3-804c-42f981e89b37/d00fe1af66beee50286f845ba692d815.jpg"


    def test_create_draft(self):

        # 构建一个测试投保单
        policyRequest = PolicyApiDTO(insuredName='测试有限公司', # 被保险人
                                     trackingNo='TEST001', # 设置原单号
                                     transportModeCode=TransportMode.SEA.value, # 运输方式
                                     deliverywayCode=Deliveryway.EXPRESS.value, # 派送方式
                                     transportTool='LH721', # 运输工具及航次
                                     cargoDesc='led灯1', # 货物描述
                                     cargoCategoryCode=CargoCategory.NORMAL.value, # 货物类别
                                     departureCountryCode='CHN', # 起运国
                                     departureAddress='SHENZHEN', # 起运地
                                     destinationCountryCode='USA', # 目的国
                                     destinationAddress='MEM 13292 E Holmes Rd', # 目的地
                                     departureDate=datetime.datetime.now(), # 起运日期
                                     expressCompanyCode=ExpressCompany.UPS.value, # 快递公司名，如果有快递单号，则快递公司必填
                                     expressNo='1Z9474VX6832389526', # 海外派送快递单号
                                     blNo='020-48236661', # 提单号
                                     packingCode='木箱', # 包装类型 002--纸箱 CARTON
                                     packingQuantity=5, # 包装数量
                                     chargeableWeight=400.11,  # 公斤数（毛重)
                                     cargoValue=11.11,  # 货值
                                     baseAmountWay=BaseAmountWay.VALUE.value,  # 计费方式：01 - -货值 * 加成比例
                                     currencyCode=Currency.USD.value,  # 保单币种
                                     ratio=110,  # 投保比例 %
                                     shipmentId='FBA092019293939',  # ShipmentID
                                     remark='Mark',  # 备注
                                     shelfType='NONE',  # 上架类型
                                     shelfName='FBA',  # 上架目的地；目前仅仅支持持FBA上架保障；
                                     destType=DestType.FBA.value,
                                     unrestRisk=True,  # 是否暴动保障
                                     warRisk=True  # 是否战争保障
                                     )

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
        # 构建批量投保单
        policyList = []
        policyRequest = PolicyApiDTO(insuredName='测试有限公司',  # 被保险人
                                     trackingNo='track6100001989',  # 设置原单号
                                     transportModeCode=TransportMode.SEA.value,  # 运输方式
                                     deliverywayCode=Deliveryway.EXPRESS.value,  # 派送方式
                                     transportTool='LH721',  # 运输工具及航次
                                     cargoDesc='led灯1',  # 货物描述
                                     cargoCategoryCode=CargoCategory.NORMAL.value,  # 货物类别
                                     departureCountryCode='CHN',  # 起运国
                                     departureAddress='SHENZHEN',  # 起运地
                                     destinationCountryCode='USA',  # 目的国
                                     destinationAddress='MEM 13292 E Holmes Rd',  # 目的地
                                     departureDate=datetime.datetime.now(),  # 起运日期
                                     expressCompanyCode=ExpressCompany.UPS.value,  # 快递公司名，如果有快递单号，则快递公司必填
                                     expressNo='1Z9474VX6832389526',  # 海外派送快递单号
                                     blNo='020-48236661',  # 提单号
                                     packingCode='木箱',  # 包装类型 002--纸箱 CARTON
                                     packingQuantity=5,  # 包装数量
                                     chargeableWeight=400.11,  # 公斤数（毛重)
                                     cargoValue=11.11,  # 货值
                                     currencyValue=Currency.USD.value,  # 货值币别
                                     baseAmountWay=BaseAmountWay.VALUE.value,  # 计费方式：01 - -货值 * 加成比例
                                     currencyCode=Currency.USD.value,  # 保单币种
                                     ratio=110,  # 投保比例 %
                                     shipmentId='FBA092019293939',  # ShipmentID
                                     remark='Mark',  # 备注
                                     shelfType='NONE',  # 上架类型
                                     shelfName='FBA',  # 上架目的地；目前仅仅支持持FBA上架保障；
                                     destType=DestType.FBA.value,
                                     unrestRisk=True,  # 是否暴动保障
                                     warRisk=True  # 是否战争保障
                                     )

        # 上传附件 FILE
        policyAttachmentApiDTO = PolicyAttachmentApiDTO(remake='nothing', type='guarantee_letter', url=self.file_url)
        attachments = [policyAttachmentApiDTO]
        policyRequest.attachmentList = attachments

        # 被保险人
        policyInsuredApiDTO = PolicyInsuredApiDTO(insuredName='被保险人名称',
                                                  certificateType=CertificateType.PID.value,
                                                  certificateNo='330227100000000001',
                                                  mobile='13966666666',
                                                  contactAddress='被保险人联系地址'
                                                  )
        policyRequest.insuredInfo = policyInsuredApiDTO

        # 货主
        policyOwnerApiDTO = PolicyOwnerApiDTO(owner='货主名称',
                                              certificateType=CertificateType.PID.value,
                                              certificateNo='330227100000000002',
                                              mobile='18888888888',
                                              contactAddress='联系地址')
        policyRequest.ownerInfo = policyOwnerApiDTO

        # 用户名(登录跨境堡的用户名), 两者二选一, 如果同时传, 以kjbAccount为准
        # policyRequest.kjbAccount = "kjbAccount"
        # policyRequest.thirdPartAccount = "YT082101"
        policyList.append(policyRequest)
        policyBatchApiDTO = PolicyBatchApiDTO(policyList=policyList, thirdPartAccount="admin")
        config = KJBConfig(self.SECRET_ID, self.SECRET_KEY, self.BATCH_DRATT_URL)
        try:
            r = PolicyApiUtils.createBatchDraftLink(policyBatchApiDTO, config)
            print(r.json())
            assert r.json()['success']
        except IOError as e:
            print(e)

    def teardown_class(self):
        pass
