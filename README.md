# FOMO 原100人数据

固定使用原 `data/traders_profiles.json` 的100人；不会从其他排行榜增加、替换或重新排序。

|文件|用途|
|---|---|
|data/traders_profiles.json / csv|原100人资料、声明钱包及原指标|
|data/dex_swaps/|原100个JSON；97非空，共261171条来源活动|
|data/ready/events.parquet|全部261171条可读来源活动，包含转账与其他类别|
|data/ready/trades.parquet|104759条来源买卖；不混入transfer_in|
|data/ready/cohort.json|原名单与SHA256，不是另一份榜单|
|data/ready/coverage.csv / json|每账户×链的范围、空数据、未知与分页状态|
|data/ready/inputs.json|输入路径、字节SHA256与行数|
|data/raw/relay/|本轮按原钱包补查的意图、两端执行与续游标|
|data/tokens_holdings.json / csv|原持仓快照，非所有历史持仓|

原活动总体时间：2025-10-09T19:24:52Z至2026-10-11T15:56:38Z；这是整体极值，不代表每人覆盖整个区间。
97完整EVM地址、96完整Solana地址；3个原名单账户地址掩码，1个原账户未提供Solana地址，均保留在100人分母。

已验收的固定补充组件位于`data/ready_final_original_cohorts_v1/`；联合最终交付仍在组装，下面的来源分别读取，不相加当独立交易：

|组件|已验收记录与范围|
|---|---|
|hyperliquid/|234823条成交、7079条资金费、1513条其他账本；97已知EVM地址的三类可见分页均到来源终点，3掩码账户保留缺口；当前仓位、余额与状态另表|
|sol_holdings/|37377条当前native/SPL/Token2022余额，96已知Sol地址的288个源快照；4个无Sol地址位置保留|
|evm_native_balances/|388条当前原生币余额，97地址×4链；3掩码账户的12位置保留，非ERC20全持仓|
|address_gaps/|原100人原字段与7个缺失钱包位置的逐行证据；3掩码账户及lowgrandcrane缺Sol，不填0或猜地址|
|ethereum_internal_compatibility/|45条实际兼容索引内部调用；服务报告索引不完整或429、未查询均保留，非完整历史|

这些表的`source_path`相对各组件目录；旧`data/ready`只取events.parquet和trades.parquet作原档案基线，其中早期部分Relay表不作为当前最终Relay来源。

完整性：**原始数据可使用，全历史未证明完整**。已存活动不是261171笔独立经济交易，也不构成完整费用/净利润对账。
详见 [完整性调查](COMPLETENESS.md)、[字段字典](DATA_DICTIONARY.md)。

```python
import pandas as pd
trades = pd.read_parquet('data/ready/trades.parquet',
    columns=['wallet', 'chain', 'timestamp_utc', 'event_type', 'asset_address', 'token_amount_provider'])
coverage = pd.read_csv('data/ready/coverage.csv')
```

采集和整理代码位于 `smart-money-dataset-builder`，本仓库只放数据与说明。原始文件不被清洗覆盖。
较大的本地Parquet/raw不提交GitHub；仓库保存结构、范围与可核对manifest，实际文件位于本机上述路径。
