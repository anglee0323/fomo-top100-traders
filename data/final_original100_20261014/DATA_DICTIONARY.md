# 字段与单位

原100人的 rank/handle/钱包保持原档案。account_id 是本数据集的原名单标识，不冒充平台内部ID。

- solana/transactions.parquet：每原账户×签名一行；event_observations_json 保留来源活动及版本，不把同签名的多条记录当多笔独立交易。
- relay_orders/transactions.parquet：每原账户×Relay request_id一行；这是订单/执行元数据。owner_initiated 与 recipient_only 分开，收到资产不自动认定主动买入。
- relay_orders/owner_asset_changes.parquet：平台报告的原账户 stateChanges；只有明确绑定的原EVM/Sol地址纳入。origin/destination、leg_index/change_index保持，不从quote反推实收。
- evm_transactions.parquet：每原账户×chain_id×tx_hash一行；由地址转移索引或原账户Relay执行引用发现，relay_references_json保留每条订单/执行腿来源。receipt_available表示有可验证回执。execution_status 0x0保留失败，0x1仅指链上执行成功。
- indexed_transfers/fungible_transfer_history.parquet：每原账户×网络×来源uniqueId一行。amount_raw为有符号整数字符串；amount_basic仅由raw与来源decimals精确缩放。0decimals有效；未知保持null。
- indexed_transfers/other_asset_history.parquet：NFT等非同质化记录单独保存，不混入资金买卖统计。
- evm_receipts.parquet：每chain_id×tx_hash一份去重回执；receipt里的from可能是bundler，不自动当原账户payer。
- execution_fee_raw/fee_raw：gasUsed×effectiveGasPrice的wei整数，仅执行gas，非全部钱包费用；不转换美元。未知费用保留null。
- asset_address：链与真实合约地址共同确定资产；原生币使用native:chain_id，不按symbol拼资产。
- source_path/source_sha256/source_pointer：固定输入路径、字节摘要与JSON指针。index与receipt各自保留，不把一个来源当两次独立证明。
- coverage/gaps：来源终页、可见时间、续游标与缺口分开。source_eof不等于链创世以来所有类型历史完整。

Relay费用的reported、paid及币种分别保留；不二次扣除已净实收，不计算净收益或历史本金。主表之外的全回执日志留作证据，不能将别人的路由腿算作本账户交易。
