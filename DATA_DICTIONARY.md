# 数据字段与读取

`cohort.json` 固定原名单；`events.parquet` 包含有效来源活动；`trades.parquet` 仅包含来源标注的 buy/sell。
`coverage.csv/json` 按账户与链说明范围、续游标和未知；`quarantine.jsonl` 保留无法可靠归属的行。

|字段|含义|
|---|---|
|account_id|本地账户/链钱包角色键；不是平台原始账户ID|
|rank|原名单排名，不重新排序|
|chain / wallet|链与原名单声明的钱包；Solana地址大小写保留|
|event_id|链、钱包、完整来源行的SHA256；同一tx的不同事件不会仅凭tx_hash合并|
|tx_hash|交易哈希或Solana签名；同一交易可有多行|
|timestamp_utc|来源时间转UTC；不代表实际采集时间|
|event_type|来源活动类别；transfer_in不是自动推断的买入|
|asset_address / asset_symbol|合约或mint与来源symbol；不会按symbol拼接或定价|
|token_amount_provider / quote_amount_provider|原来源数量字符串；不猜decimals、不自动除以10^18|
|gas_native_provider / gas_usd_provider|来源报告值，非全部费用证明；0不证明全费用为0|
|cost_usd_provider|来源报告金额，非经验证历史本金/成本基础/净收益|
|source_path / source_sha256 / source_pointer|仓库相对来源路径、来源文件字节SHA256、JSONpointer|
|raw_json|完整公开来源活动字段；可恢复尚未展平的event/log/instruction字段|

未知保留null；不会把未知费用或成本改为0。`source_eof`只说明指定API终页，不证明全链历史完整。
过滤只移除同账户完全相同的来源行；未知/无效身份进入quarantine，不删除原始文件。

```python
import pandas as pd
trades = pd.read_parquet('data/ready/trades.parquet',
    columns=['wallet', 'chain', 'timestamp_utc', 'event_type', 'asset_address', 'token_amount_provider'])
coverage = pd.read_csv('data/ready/coverage.csv')
```

买卖表为精简查询表；完整 `raw_json` 在 events.parquet，源字段还可通过source_path/source_pointer回放。
