## 关于包的安装：

```
pip install kjb-open-sdk
或
pip3 install kjb-open-sdk
```

## 关于包的引用及示例

```
# 跨境堡提供的SecretId
SECRET_ID = "XXXXX"
# 跨境堡提供的SecretKey
SECRET_KEY = "XXXXXX"
# 服务域名
SERVICE_HOST = "testapi.kjingbao.com"
POLICY_LINK_URL = f"http://{SERVICE_HOST}/cbi/policy/v2/createPolicyLink"

policyRequest = PolicyLinkParamDTO(trackingNo='track6100001989', kjbAccount='XXXXX', thirdPartAccount='XXXX')
config = KJBConfig(SECRET_ID, SECRET_KEY, POLICY_LINK_URL)
try:
    r = PolicyApiUtils.createPolicyLink(policyRequest, config)
    print(r.json())
    assert r.json()['success']
except IOError as e:
    print(e)
```

更多示例请参考SDK下的`test`目录

接口的具体说明请查看：[跨境堡平台API文档](https://testhelp.kjingbao.com/detail/index?documentId=115)



## 关于版本

| 版本号 | sdk更新日期    | 
| -------- |------------| 
| 1.0.0 | 2023-10-11 | 
