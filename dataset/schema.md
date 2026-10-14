# 数据字典

时间按UTC读取。原始整数与精确小数以文本保存；金额计算使用Decimal。null表示未知或来源未提供。

资产键使用链+合约/mint，账户键使用表所列组合键。相同交易中的多个事件、执行腿和资产变化分别保留。

## solana/transactions.parquet

|字段|类型|含义|
|---|---|---|
|account_id|string|数据集内稳定账户/链钱包角色键；FOMO的original_fomo:rank:handle为本地标识。|
|rank|int32|冻结样本中的原排名；GMGN排名在每链内部定义。|
|handle|string|来源账户用户名，可为空。|
|wallet|string|被查询/关联的钱包；回执表可为空，账户成员关系见memberships_json。|
|tx_hash|string|EVM交易哈希或Solana签名；UserOp来源中为用户操作哈希，需在raw_json读取外层交易。|
|timestamp_utc|string|来源时间，ISO 8601 UTC文本；未知为null，读取时显式转换为UTC时间。|
|has_buy_sell|bool|该Solana交易的来源观察是否包含buy/sell分类。|
|source_event_observation_count|int32|聚合到该账户×签名的活动观察数。|
|event_observations_json|string|该账户×签名的活动及逐条来源引用JSON数组。|

## evm_transactions.parquet

|字段|类型|含义|
|---|---|---|
|rank|int64|冻结样本中的原排名；GMGN排名在每链内部定义。|
|handle|string|来源账户用户名，可为空。|
|wallet|string|被查询/关联的钱包；回执表可为空，账户成员关系见memberships_json。|
|chain_id|int64|十进制EVM链ID：1 Ethereum、56 BSC、8453 Base、4663 Robinhood。|
|tx_hash|string|EVM交易哈希或Solana签名；UserOp来源中为用户操作哈希，需在raw_json读取外层交易。|
|timestamp_utc|string|来源时间，ISO 8601 UTC文本；未知为null，读取时显式转换为UTC时间。|
|block_number|string|EVM区块高度十进制文本。|
|receipt_available|bool|纳入哈希是否有已验证链上回执。|
|execution_status|string|EVM回执执行状态：0x1成功、0x0失败；未知为null。|
|execution_fee_raw|string|gasUsed × effectiveGasPrice的wei整数文本，不代表全部钱包费用。|
|fee_unit|string|费用计量单位，例如wei；不是美元。|
|fee_payer|string|执行费用付款地址，可能为bundler，不一定等于样本钱包。|
|receipt_source_path|string|执行回执来源路径，相对dataset根目录。|
|receipt_source_sha256|string|执行回执来源原始字节SHA256。|
|receipt_source_pointer|string|执行回执在来源JSON中的指针。|
|index_source_path|string|地址索引来源路径，相对dataset根目录。|
|index_source_sha256|string|索引来源原始字节SHA256。|
|index_source_pointer|string|索引来源JSON指针。|
|indexed_event_count|int64|纳入该账户×链×交易的地址索引事件数。|
|relay_references_json|string|关联Relay请求/执行腿的JSON引用数组。|

## evm_receipts.parquet

|字段|类型|含义|
|---|---|---|
|record_id|string|来源记录的稳定标识，不能替代交易哈希。|
|source|string|来源接口/记录类型。|
|chain|string|链标识；GMGN使用sol/bsc/base/eth/robinhood；通用EVM来源表使用十进制chain ID文本。|
|wallet|string|被查询/关联的钱包；回执表可为空，账户成员关系见memberships_json。|
|memberships_json|string|关联账户/链钱包角色列表的JSON文本；回执可同时属于多个账户。|
|tx_hash|string|EVM交易哈希或Solana签名；UserOp来源中为用户操作哈希，需在raw_json读取外层交易。|
|timestamp_utc|string|来源时间，ISO 8601 UTC文本；未知为null，读取时显式转换为UTC时间。|
|asset_address|string|链内资产合约或mint标识；原生资产可为空。|
|token_account|string|来源提供的代币账户，可缺失。|
|amount_raw|string|来源资产原始整数文本；避免浮点转换。|
|decimals_source|int32|来源资产精度，0是有效值，未知为null。|
|amount_basic|string|按来源精度换算的十进制数量文本；精度未知时为null。|
|amount_ui_source|string|来源显示数量文本，仅保留观察值。|
|fee_raw|string|来源原始费用整数文本；类型及单位由fee_type_source/fee_unit指定。|
|fee_unit|string|费用计量单位，例如wei；不是美元。|
|fee_type_source|string|费用的来源含义/计算口径。|
|fee_payer|string|执行费用付款地址，可能为bundler，不一定等于样本钱包。|
|context_slot|string|来源区块高度/上下文槽位文本，具体语义按source解释。|
|source_path|string|相对dataset根目录的压缩来源文件路径。|
|source_sha256|string|来源文件原始字节SHA256；先解压存储层再校验。|
|source_pointer|string|解码来源JSON后定位原记录的RFC 6901 JSON指针。|
|raw_json|string|完整来源记录的JSON文本。|

## relay_orders/transactions.parquet

|字段|类型|含义|
|---|---|---|
|account_id|string|数据集内稳定账户/链钱包角色键；FOMO的original_fomo:rank:handle为本地标识。|
|handle|string|来源账户用户名，可为空。|
|wallet|string|被查询/关联的钱包；回执表可为空，账户成员关系见memberships_json。|
|request_id|string|Relay请求标识；同一请求可有多个账户成员或多条执行腿。|
|created_at_utc|string|来源请求创建时间UTC。|
|updated_at_utc|string|来源请求更新时间UTC。|
|status|string|来源请求状态。|
|participation|string|原账户的参与角色，例如initiator或recipient_only。|
|initiator|string|来源请求发起者。|
|recipient|string|来源请求收款者。|
|input_asset|string|输入资产合约/mint。|
|input_symbol|string|输入资产显示符号。|
|input_amount_reported_raw|string|来源报告的输入原始数量整数文本。|
|input_amount_reported_basic|string|按来源精度缩放的输入数量文本。|
|output_asset|string|输出资产合约/mint。|
|output_symbol|string|输出资产显示符号。|
|output_amount_reported_raw|string|来源报告的输出原始数量整数文本。|
|output_amount_reported_basic|string|按来源精度缩放的输出数量文本，保留reported口径。|
|origin_owner_asset_delta_raw|string|来源报告的输入侧原账户资产变化原始整数文本。|
|origin_owner_asset_delta_basic|string|输入侧原账户资产变化的十进制数量文本。|
|destination_owner_asset_delta_raw|string|来源报告的输出侧原账户资产变化原始整数文本。|
|destination_owner_asset_delta_basic|string|输出侧原账户资产变化的十进制数量文本。|
|in_transactions_json|string|输入侧执行交易数组JSON。|
|out_transactions_json|string|输出侧执行交易数组JSON。|
|app_fee_currency_json|string|来源应用费用资产对象JSON。|
|app_fees_reported_json|string|来源报告应用费用JSON。|
|app_fees_paid_json|string|来源实际支付应用费用JSON，与reported分开。|
|relay_fees_reported_json|string|来源Relay费用JSON。|
|relay_fees_usd_reported_json|string|来源报告的USD Relay费用JSON。|
|source_path|string|相对dataset根目录的压缩来源文件路径。|
|source_sha256|string|来源文件原始字节SHA256；先解压存储层再校验。|
|source_pointer|string|解码来源JSON后定位原记录的RFC 6901 JSON指针。|
|source_request_sha256|string|来源请求对象的规范化内容SHA256。|
|rank|int64|冻结样本中的原排名；GMGN排名在每链内部定义。|
|input_chain_id|int64|来源请求输入链ID。|
|input_decimals_source|int64|输入资产来源精度。|
|output_chain_id|int64|来源请求输出链ID。|
|output_decimals_source|int64|输出资产来源精度。|

## relay_orders/owner_asset_changes.parquet

|字段|类型|含义|
|---|---|---|
|account_id|string|数据集内稳定账户/链钱包角色键；FOMO的original_fomo:rank:handle为本地标识。|
|handle|string|来源账户用户名，可为空。|
|request_id|string|Relay请求标识；同一请求可有多个账户成员或多条执行腿。|
|phase|string|执行腿方向/阶段，例如in/out。|
|tx_hash|string|EVM交易哈希或Solana签名；UserOp来源中为用户操作哈希，需在raw_json读取外层交易。|
|tx_status|string|该执行腿的来源状态。|
|owner_address|string|该条资产变化所属的原账户地址。|
|asset_address|string|链内资产合约或mint标识；原生资产可为空。|
|amount_delta_raw|string|带符号资产变化原始整数文本。|
|amount_delta_basic|string|带符号十进制资产变化文本。|
|source_path|string|相对dataset根目录的压缩来源文件路径。|
|source_sha256|string|来源文件原始字节SHA256；先解压存储层再校验。|
|source_pointer|string|解码来源JSON后定位原记录的RFC 6901 JSON指针。|
|rank|int64|冻结样本中的原排名；GMGN排名在每链内部定义。|
|chain_id|int64|十进制EVM链ID：1 Ethereum、56 BSC、8453 Base、4663 Robinhood。|
|leg_index|int64|来源执行腿数组下标。|
|change_index|int64|来源资产变化数组下标。|
|decimals_source|int64|来源资产精度，0是有效值，未知为null。|

## indexed_transfers/fungible_transfer_history.parquet

|字段|类型|含义|
|---|---|---|
|record_id|string|来源记录的稳定标识，不能替代交易哈希。|
|source|string|来源接口/记录类型。|
|chain|string|链标识；GMGN使用sol/bsc/base/eth/robinhood；通用EVM来源表使用十进制chain ID文本。|
|wallet|string|被查询/关联的钱包；回执表可为空，账户成员关系见memberships_json。|
|memberships_json|string|关联账户/链钱包角色列表的JSON文本；回执可同时属于多个账户。|
|tx_hash|string|EVM交易哈希或Solana签名；UserOp来源中为用户操作哈希，需在raw_json读取外层交易。|
|timestamp_utc|string|来源时间，ISO 8601 UTC文本；未知为null，读取时显式转换为UTC时间。|
|asset_address|string|链内资产合约或mint标识；原生资产可为空。|
|token_account|string|来源提供的代币账户，可缺失。|
|amount_raw|string|来源资产原始整数文本；避免浮点转换。|
|decimals_source|int32|来源资产精度，0是有效值，未知为null。|
|amount_basic|string|按来源精度换算的十进制数量文本；精度未知时为null。|
|amount_ui_source|string|来源显示数量文本，仅保留观察值。|
|fee_raw|string|来源原始费用整数文本；类型及单位由fee_type_source/fee_unit指定。|
|fee_unit|string|费用计量单位，例如wei；不是美元。|
|fee_type_source|string|费用的来源含义/计算口径。|
|fee_payer|string|执行费用付款地址，可能为bundler，不一定等于样本钱包。|
|context_slot|string|来源区块高度/上下文槽位文本，具体语义按source解释。|
|source_path|string|相对dataset根目录的压缩来源文件路径。|
|source_sha256|string|来源文件原始字节SHA256；先解压存储层再校验。|
|source_pointer|string|解码来源JSON后定位原记录的RFC 6901 JSON指针。|
|raw_json|string|完整来源记录的JSON文本。|

## indexed_transfers/other_asset_history.parquet

|字段|类型|含义|
|---|---|---|
|record_id|string|来源记录的稳定标识，不能替代交易哈希。|
|source|string|来源接口/记录类型。|
|chain|string|链标识；GMGN使用sol/bsc/base/eth/robinhood；通用EVM来源表使用十进制chain ID文本。|
|wallet|string|被查询/关联的钱包；回执表可为空，账户成员关系见memberships_json。|
|memberships_json|string|关联账户/链钱包角色列表的JSON文本；回执可同时属于多个账户。|
|tx_hash|string|EVM交易哈希或Solana签名；UserOp来源中为用户操作哈希，需在raw_json读取外层交易。|
|timestamp_utc|string|来源时间，ISO 8601 UTC文本；未知为null，读取时显式转换为UTC时间。|
|asset_address|string|链内资产合约或mint标识；原生资产可为空。|
|token_account|string|来源提供的代币账户，可缺失。|
|amount_raw|string|来源资产原始整数文本；避免浮点转换。|
|decimals_source|int32|来源资产精度，0是有效值，未知为null。|
|amount_basic|string|按来源精度换算的十进制数量文本；精度未知时为null。|
|amount_ui_source|string|来源显示数量文本，仅保留观察值。|
|fee_raw|string|来源原始费用整数文本；类型及单位由fee_type_source/fee_unit指定。|
|fee_unit|string|费用计量单位，例如wei；不是美元。|
|fee_type_source|string|费用的来源含义/计算口径。|
|fee_payer|string|执行费用付款地址，可能为bundler，不一定等于样本钱包。|
|context_slot|string|来源区块高度/上下文槽位文本，具体语义按source解释。|
|source_path|string|相对dataset根目录的压缩来源文件路径。|
|source_sha256|string|来源文件原始字节SHA256；先解压存储层再校验。|
|source_pointer|string|解码来源JSON后定位原记录的RFC 6901 JSON指针。|
|raw_json|string|完整来源记录的JSON文本。|

## account_features.parquet

|字段|类型|含义|
|---|---|---|
|account_id|large_string|数据集内稳定账户/链钱包角色键；FOMO的original_fomo:rank:handle为本地标识。|
|rank|int64|冻结样本中的原排名；GMGN排名在每链内部定义。|
|wallet|large_string|被查询/关联的钱包；回执表可为空，账户成员关系见memberships_json。|
|chain|large_string|链标识；GMGN使用sol/bsc/base/eth/robinhood；通用EVM来源表使用十进制chain ID文本。|
|event_count|int64|本账户×链的来源观察数；GMGN为活动行，FOMO为账户交易头行。|
|transaction_count|int64|本账户×链的不同交易哈希/签名数量。|
|active_days|int64|有可解析UTC时间的观察日期数。|
|first_seen_utc|timestamp[us, tz=Asia/Shanghai]|本来源观察的最早UTC时间，不代表账户创建时间。|
|last_seen_utc|timestamp[us, tz=Asia/Shanghai]|本来源观察的最晚UTC时间。|
|has_observed_activity|bool|本数据表是否包含该账户×链的观察；false不证明链上无活动。|

## 来源回放

`source_path`相对于dataset根目录。对该文件gzip解压一次得到来源原始字节，校验`source_sha256`。如果原始字节仍为gzip，再解压后解析JSON，使用`source_pointer`定位原记录。`evidence/index.json`列出存储层及来源层的字节数和SHA256。

## 汇总特征

`account_features.parquet`每账户×链一行，基于各主表的全部已观察范围计算。计数为0仅表示表内无观察；时间边界/覆盖限制仍以coverage为准。该表适合描述性分析和特征探索。预测任务应按决策截止时间重新截断、建立目标并划分训练/验证集，不能直接把全期汇总作为历史决策时特征。
