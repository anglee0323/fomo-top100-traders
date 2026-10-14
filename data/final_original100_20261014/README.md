# FOMO 原100人最终可用数据

入口是本目录 MANIFEST.json；原名单在cohort.json，真实范围和缺口在coverage.csv与gaps.csv。

先读取solana/transactions.parquet、relay_orders/transactions.parquet与evm_transactions.parquet。
需要资产明细时读indexed_transfers的同质化转移表或Relay owner_asset_changes表；需要网络执行证据时读evm_receipts.parquet。
这些表是不同来源和不同层次，不应相加作为交易笔数或金额。全部字段含义见DATA_DICTIONARY.md。

3个原名单掩码账户和1个缺Sol地址账户始终保留。不可获得的地址/类型/订单元数据按具体账户、链、时间范围、实际原因列在gaps.csv。
已查询来源的末页状态与全链完整性区分。未声明取得平台私有下单全量导出，也不计算策略收益。

```python
import pandas as pd
sol = pd.read_parquet('solana/transactions.parquet')
evm = pd.read_parquet('evm_transactions.parquet')
orders = pd.read_parquet('relay_orders/transactions.parquet')
gaps = pd.read_csv('gaps.csv')
```
