# FOMO 原100账户交易数据

最终入口：[data/final_original100_20261014/README.md](data/final_original100_20261014/README.md)。名单固定为原data/traders_profiles.json，未增加、替换或重新排序。

|主表|内容|
|---|---|
|solana/transactions.parquet|135986条账户×Sol签名记录；96个已知地址的GMGN可见来源已到终页|
|evm_transactions.parquet|332970条账户×链×交易哈希记录，全部对应可验证回执|
|evm_receipts.parquet|243641份去重链上回执；保留真实执行状态与gas乘积|
|relay_orders/transactions.parquet|58066条账户×Relay订单记录，原始字段与两端执行引用保留|
|relay_orders/owner_asset_changes.parquet|109797条平台报告的原账户资产变化，quote与实收不混用|
|indexed_transfers/fungible_transfer_history.parquet|354333条可读同质化转移记录；NFT2202条另表|

这些是不同记录层次，不相加当交易笔数或金额。费用是执行gas或平台分别报告的费用，不是已证明全部成本/净收益。

[覆盖表](data/final_original100_20261014/coverage.csv)、[具体缺口](data/final_original100_20261014/gaps.csv)、[字典](data/final_original100_20261014/DATA_DICTIONARY.md)、[文件摘要](data/final_original100_20261014/MANIFEST.json)均在最终目录。

3个原账户钱包掩码（boosted、CryptoZachLA、XbtPika），lowgrandcrane未提供Sol地址，保留原字段和7个钱包位置缺口。
Relay订单源44/97到终点；其余53的旧订单元数据仍有续游标/网络失败，已使用原钱包四主链地址索引补可得链上记录。不能从链上回执编造缺失的订单ID或私有平台元数据。
转移索引不供应失败/零资产变化交易，BSC与Robinhood原生内部转移也不在该索引范围；未知范围逐账户列明。

Sol表是GMGN可见活动，未证明所有已关闭ATA的全链历史。各来源时间范围分别保留，目录日期是整理日期，不代表所有源都更新到同一时刻。

原100个dex_swaps文件、261171条旧活动及已捕获来源保留作回放；无关服务表不作为主交易入口。大表和原始回执只存本机，Git同步代码、说明与可核对元数据，不上传凭据。
