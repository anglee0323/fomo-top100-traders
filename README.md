# FOMO 清洗后可用数据

唯一入口：`data/clean/`。原100名单仅剔除无完整地址的3个账户，保留97个EVM账户、96个Sol地址；rank不重排、不补其他人。lowgrandcrane保留EVM，缺失Sol不采集。

## 下载实际数据

[清洗数据 Release（包含全部主表及唯一压缩来源证据）](https://github.com/anglee0323/fomo-top100-traders/releases/tag/clean-20261014)。先安装GitHub CLI并正常登录，克隆仓库后执行：

```sh
uv run --no-project python download_data.py
```

脚本自动下载分卷、校验SHA256并解包；已有`data/clean`时拒绝覆盖。只克隆Git仓库会得到说明与元数据，实际大表在Release中。

## 可直接使用的表

|文件|记录数|含义|
|---|---:|---|
|solana/transactions.parquet|135986|原账户×Sol签名，内嵌来源活动|
|evm_transactions.parquet|332970|原账户×链×交易哈希；已知哈希缺回执0|
|evm_receipts.parquet|243641|去重链×交易回执，包含真实status及日志|
|relay_orders/transactions.parquet|58066|已有Relay订单/执行元数据|
|relay_orders/owner_asset_changes.parquet|109797|来源报告的原账户资产变化|
|indexed_transfers/fungible_transfer_history.parquet|354333|同质化转移事件与原始单位|
|indexed_transfers/other_asset_history.parquet|2202|NFT等其他资产事件，单独保存|

这些表是不同层次，不能相加当独立交易笔数。默认先读取Sol/EVM两个transactions主表；其余用于资产明细、订单上下文和执行证据。

`coverage.csv`保留405个真实来源范围；`gaps.csv`的371项为来源限制/未闭合元数据，**不是371笔已知丢失交易**。Sol是GMGN可见地址活动；EVM索引不保证失败/零资产变化交易，BSC/Robinhood不供应原生内部转移。已知纳入哈希均有回执，不代表所有地址全生命周期完整。

原始rank/handle/完整地址在`cohort.json`，剔除记录在`exclusions.json`。单位见`DATA_DICTIONARY.md`，实际校验见`ACCEPTANCE.json`，文件摘要见`MANIFEST.json`。

来源文件已按内容SHA去重并压缩，仅保留一份`evidence/`；所有引用均相对于`data/clean`，不依赖旧报告或旧数据目录。

下次采集使用[唯一采集流程](https://github.com/anglee0323/smart-money-dataset-builder)：FOMO Sol直接分页，EVM走Alchemy地址索引及批量回执。没有换名单或重新采集的动作。
