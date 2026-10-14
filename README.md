# FOMO Trader Dataset

2026-10-14版，覆盖原Top100样本中具有完整地址的97个账户：97个EVM地址、96个Solana地址，保留原rank 1–97。账户身份及链地址见`accounts.json`，地址可用性条件见`eligibility.json`。

[下载数据集 v2026.10.14](https://github.com/anglee0323/fomo-top100-traders/releases/tag/v2026.10.14)

## 数据表

|Parquet表（相对dataset）|行数|记录粒度 / 关联键|
|---|---:|---|
|solana/transactions.parquet|135,986|账户×Solana签名；`rank, tx_hash`|
|evm_transactions.parquet|332,970|账户×链×交易；`rank, chain_id, tx_hash`|
|evm_receipts.parquet|243,641|链×执行回执；`chain, tx_hash`|
|relay_orders/transactions.parquet|58,066|账户×Relay请求；`rank, request_id`|
|relay_orders/owner_asset_changes.parquet|109,797|请求执行腿×资产变化；`rank, request_id, phase, leg_index, change_index`|
|indexed_transfers/fungible_transfer_history.parquet|354,333|同质化资产转移观察；`record_id`|
|indexed_transfers/other_asset_history.parquet|2,202|NFT等其他资产观察；`record_id`|
|account_features.parquet|581|账户×链的描述性计数与时间特征|

一般分析从Solana/EVM的transactions表开始。EVM回执按`chain=CAST(chain_id AS VARCHAR), tx_hash`关联，可被多个样本账户共享；执行失败状态保留为`0x0`。Relay通过`rank, request_id`关联资产变化，输入/输出执行腿的交易引用保存在JSON字段。转移表通过链、钱包和交易哈希提供明细，不能与交易头做无条件多对多拼接。

## 覆盖范围

Solana使用钱包直接活动分页，96个已知地址均到达该来源终页，94个有可见记录；这不包含所有ATA/已关闭代币账户的独立完整历史保证。EVM记录来自Relay执行引用及Ethereum、BSC、Base、Robinhood地址转移索引；已纳入的全部交易哈希均有回执，缺失回执为0。

部分Relay执行还涉及链ID 10、137、143、42161、5042、999；这些执行回执与关联交易包含在EVM表内，来源地址索引范围仍按四条主链单列。

地址索引的53个账户×4链共212个来源范围均到达本次查询边界，查询截止为2026-10-14 05:27:07 UTC。查询起始参数1970表示尽可能向前查询，不是账户创建时间。其余44个账户的Relay请求来源到达终页；53个账户仍有未闭合的订单元数据，逐地址列在limitations中。链上执行回执与平台私有订单元数据分别保留。

405条coverage记录列出实际来源、时间与状态。371条limitations包括53项未闭合订单元数据、212项失败/零资产变化等索引类型限制、106项BSC/Robinhood原生内部转移限制；不是371笔已知丢失交易。地址索引中的转移可能包含FOMO平台之外的账户活动，不能将所有行自动标记为FOMO下单。

3个地址掩码账户（原rank 98–100）不纳入数据；rank 97保留EVM，其Solana地址缺失，仅对应Solana范围不可用。具体记录见`eligibility.json`。

## 下载与使用

Git仓库包含说明、账户名单、覆盖清单和示例；Parquet表及压缩来源文件从Release下载。安装uv并完成GitHub CLI登录（`gh auth login`）后，在仓库根目录执行：

```sh
uv run --no-project python download_data.py
uv sync --locked
uv run --no-sync python examples/analyze.py --output analysis-output
```

第三条命令生成`account_features.parquet/.csv`、`daily_activity.csv`、`activity_by_chain.png`和经标准化的`features.npy`。这几份输出由数据表直接计算。已有同名输出目录时脚本拒绝覆盖。

```python
from pathlib import Path
import pandas as pd

root = Path("dataset")
features = pd.read_parquet(root / "account_features.parquet")
```

`account_features.parquet`是随版本提供的账户×链描述性特征表。`examples/analyze.py`提供其可复现计算过程，使用投影读取和SQL聚合，无需一次加载所有来源JSON。生成的数值矩阵可输入scikit-learn等框架；预测目标、时间截断及训练划分由具体研究问题定义。


读取交易头和资产明细：

```python
evm = pd.read_parquet(root / "evm_transactions.parquet")
sol = pd.read_parquet(root / "solana/transactions.parquet",
    columns=["rank", "handle", "wallet", "tx_hash", "timestamp_utc", "has_buy_sell"])
by_chain = evm.groupby("chain_id").agg(
    account_transactions=("tx_hash", "size"),
    physical_transactions=("tx_hash", "nunique"))
```

## 文件导航

|路径|内容|
|---|---|
|dataset/accounts.json|账户身份、链钱包与原排名|
|dataset/metadata.json|版本、表行数、文件大小与SHA256|
|dataset/schema.md / schema.json|每张表的字段、类型及单位|
|dataset/coverage.csv / coverage.json|逐账户、钱包、来源的时间范围及分页状态|
|dataset/limitations.csv / limitations.json|具体地址、链、来源与范围限制|
|dataset/validation.json|文件完整性、引用和回放校验状态|
|dataset/evidence/|按内容摘要存储的压缩来源文件，供追溯与核查|
|examples/analyze.py|汇总、图表和数值特征矩阵示例|

所有`source_path`都相对于dataset目录。通常分析只读取Parquet；需要核查原始字段时，按schema中的来源回放说明定位。原始整数用文本保存，避免大整数经过浮点数后失真；精度未知时保持null。

## 分析口径

交易、事件、资产变化、订单和回执分别具有不同粒度，不能直接相加为交易总数。费用保留原生单位和付款方；网络gas不能替代全部账户成本。数据不附带完整净利润或策略收益标签。

样本按排行榜筛选，代表该样本的可观察活动；不能直接外推全部交易者。全期特征适合描述性分析，预测建模应按当时可知信息重算特征，按账户/时间分组验证，并保留缺失和覆盖标记。

采集方法与复现命令见[Smart Money Dataset Builder](https://github.com/anglee0323/smart-money-dataset-builder)。该仓库作为只读方法存档保留。
