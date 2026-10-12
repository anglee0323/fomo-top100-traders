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

## 补充源表与单位

最终版本中的各表按来源分开，不能把多来源行数相加当作独立交易数量。

|表|直接可读的内容与边界|
|---|---|
|ethereum_transactions|普通交易；原始 value 与网络费字段保留，不自动推断买卖|
|ethereum_token_transfers|ERC20 等来源转账；保留合约、原始数量和来源 decimals；未验证历史区块 decimals，不填造历史币量|
|ethereum_internal_transactions|内部调用/转账来源记录；不自动认定查询钱包支付了全部费用|
|ethereum_user_operations|账户抽象操作；操作哈希和外层交易哈希分开，完整字段在 raw_json|
|solana_signatures|已发现的签名与来源时间；签名存在不代表已取得完整交易回执|
|solana_transactions|实际取得的交易回执；fee_raw/fee_unit 为真实网络费 lamports，fee_payer 为消息首个账户，不自动认定查询钱包付款|
|holdings_current|Sol 原生币及 SPL/Token2022 当前余额；mint、token_account、原始数量与来源 decimals 分开；零 token 账户仅从此查询表排除，raw 保留|
|native_balances_current|FOMO 已知 EVM 钱包在 Ethereum/BSC/Base/Robinhood 的当前原生币余额；不是 ERC20 全持仓或历史本金|
|relay_requests|每 intent 的代表来源记录；不是自动选定的最新状态或独立交易|
|relay_observations|每钱包每次捕获的完整 intent 观察；不同来源/状态版本保留|
|relay_wallet_links|intent 与原名单账户、查询钱包和实际来源行的关系；第三方 user/recipient 不自动成为 owner|

补充表的 `amount_raw` 为来源整数数量字符串，`decimals_source` 为来源提供的整数小数位，`amount_basic` 仅用于已取得单位依据的当前余额，严格按 raw / 10^decimals 计算（包括 decimals=0）。Token2022 的 `amount_ui_source` 是单独保留的来源 UI 值，可能受扩展影响，不当作市场价值。历史币量未知时保留 null，不猜18位。

`memberships_json` 保留同一钱包对应的原名单角色；Sol 地址逐字区分大小写。`context_slot` 是单次 Sol 当前余额的上下文，不代表全部钱包同一区块。余额观察时间不是交易时间；没有美元价格、成本基础或盈利推断。

来源定位：主活动表 source_path 相对仓库目录；链补充表 source_path 相对该版本目录（CHAIN_SUMMARY.source_path_base）；Relay 表为捕获输入的绝对路径。source_sha256 是捕获文件字节 SHA256，source_pointer 是其中 JSONpointer。raw_json 保留未展平字段。RPC payload_sha256 是解码 payload 的规范 JSON 摘要，不能冒充 HTTP 原始字节摘要。迁移目录时需按这些明确路径基准调整引用，不能只搬 Parquet 而丢掉 inputs。

coverage 按账户/钱包/来源保留 source_eof、续 cursor、预算暂停、实际错误、未查询和无完整地址。API EOF 仅指该来源分页终止；当前余额快照不使用历史 EOF 作为完成定义。签名、完整回执、来源活动、意图及独立经济交易是不同计数。

原 FOMO 三个掩码账户 boosted/CryptoZachLA/XbtPika 保留原排名与公开掩码，完整地址缺失；lowgrandcrane 缺 Sol 地址。它们不变成零余额/零交易，也不阻挡其他账户的数据交付。旧无合约或 mint 的持仓档案只作原始参考，不进入已验证资产持仓表。
