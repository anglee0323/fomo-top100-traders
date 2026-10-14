# 字段与单位

- `rank/handle`是原名单身份；原rank1–97保留。不是新榜或新平台ID。
- Sol主表每账户×签名一行；`event_observations_json`是原始来源活动观察，多条观察不等于多笔交易。
- EVM主表每账户×chain_id×tx_hash一行；`indexed_event_count`是该交易的索引事件数。`relay_references_json`保留来源订单与执行腿引用。
- `receipt_available`仅表示已取得并验证回执；`execution_status=0x0`为失败，保留而非剔除。`fee_payer`可能是bundler，不自动等于原钱包。
- `execution_fee_raw/fee_raw`为gasUsed×effectiveGasPrice的wei整数，非全部钱包费用、不转USD、不算净利润。
- `amount_raw/amount_delta_raw`为整数文本；`amount_basic`按来源decimals精确缩放，decimals=0有效，未知保持null。资产按chain+真实CA识别，不按symbol套价。
- Relay `participation`区分主动来源、收款等；reported/paid app fee、quote/实收保持分开，不二次扣除净实收。
- `source_path`（包括receipt/index和嵌套来源）相对于本数据根目录。解压其gzip存储层得到原始文件字节，校验`source_sha256`；若原文件本身为gzip，再解压后按`source_pointer` JSON指针读取。`evidence/index.json`列出压缩前/后摘要。
- coverage的pages/rows/cursor/EOF仅指该来源；gaps是明确的来源限制、续页与原因，缺失不填0。

raw_json保留来源原行；回执日志与订单腿不能直接当作钱包所有的独立决策。当前数据不保证完整资金或净利润对账。
