# 原100人FOMO：完整性调查

名单固定使用 `data/traders_profiles.json`，100条，不换榜。旧261171条活动保留。

## 需要补采的原因

旧采集代码 `core/sync.py` 使用GMGN activity接口，EVM过滤buy/sell/transferIn；另一个补采脚本只查三个EVM链transferIn。
旧同步按tx_hash去重，会丢同一交易中的不同事件，并在遇到一个已知哈希时停止增量；原档案未保存逐页终点证明。
因此Solana和EVM都不能直接标成完整。是否Pancake/router执行不是唯一标准，需核对钱包实际交易、资产变化与跨链两端。

FOMO官方条款明确其交易在第三方基础设施执行，并列有跨链/永续等服务。这是平台能力，不能推断每个账户使用了所有服务。
来源：https://fomo.family/terms
Relay官方接口说明：https://docs.relay.link/references/api/api_guides/migrating-to-requests-v3

本轮用原第一名theunipcs的声明EVM与Solana地址，各取得100条真实Relay请求（共200条来源行，非200笔独立交易）。
原第二名pointfarmcap的EVM查询随后HTTP429，已共享暂停；其他未尝试账户不能标无数据或完成。
请求包含user/recipient、两端chainId/hash、费用和原始状态，分别保留；外部付款人或solver不自动视作账户钱包。

## 真实缺口

原98/99/100（boosted、CryptoZachLA、XbtPika）钱包掩码且活动为空；97 lowgrandcrane无Solana地址。
原97个完整EVM、96个完整Solana地址均可形成明确补采清单；未知地址不得猜测。
原档案没有分页EOF证明；Relay、实际链上普通交易/内部交易/token事件/UserOp、Solana回执按来源单独记录。
Hyperliquid/TradeXYZ账户、持仓、资金费仅在有实际关联与记录时加入；不把GMGN spot档案称作完整永续历史。
余额/持仓快照只覆盖快照时点，不保证所有小额资产或历史变化。

## 已可使用

`data/ready/events.parquet`：261171条原活动。
`data/ready/trades.parquet`：104759条来源buy/sell。
`data/ready/coverage.csv`：100账户×5原活动链=500范围行，保留无地址与无活动情况。
`data/raw/relay/summary.json`：实际补采结果与未尝试来源数，不将429当EOF。
