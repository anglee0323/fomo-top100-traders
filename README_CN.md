# FOMO Top 100 交易员：多链链上情报与量化建模数据集

[English](README.md) | [简体中文](README_CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Snapshot: 2026--10--09](https://img.shields.io/badge/snapshot-2026--10--09_15%3A45_UTC-blue.svg)](data/)

本仓库开源了 FOMO 平台（`fomo.family`）上 **Top 100+ 交易员** 的链上情报与量化研究数据集。

**本仓库为纯粹的静态离线历史数据存档，快照截取时间为 2026-10-09 15:45:23 UTC**。本仓库仅提供客观整理的原始数据文件，用于学术探索、量化回测与机器学习模型训练，不输出主观交易结论，亦不包含任何外部网络请求或动态执行代码。

收录包含 **未脱敏 EVM 与 Solana 双链真实钱包地址**、横跨 **6 条区块链（总资金规模超 9,000 万美元）** 的多链资产分布明细、代币级持仓关系网、近期多周期收益指标、微观 DEX 买卖交易序列，以及**已预归一化的量化特征宽表**。

---

## 存档范围与时间截点

* **快照截取时间**：`2026-10-09 15:45:23 UTC`
* **数据状态**：完全离线的不可变静态数据
* **收录实体**：134 位交易员画像（97 位资金规模排名前列交易员 + 37 位近期动量榜单交易员）
* **资产覆盖**：$90,042,918 USD（涵盖 Robinhood、Solana、BSC、Base、Ethereum、Arc）
* **地址映射**：双链映射（EVM 16进制 `0x...` 与 Solana base58 原生地址）

---

## 仓库文件结构

```
fomo-top100-traders/
├── README.md                      # 英文说明文档
├── README_CN.md                   # 中文说明文档 (本文档)
├── pyproject.toml                 # 项目元数据配置
├── LICENSE                        # MIT 开源协议
└── data/
    ├── traders_profiles.csv       # 交易员画像表 (Rank, Handles, 双链未脱敏地址, 6链资金, PnL)
    ├── traders_profiles.json      # 嵌套结构化 JSON 格式
    ├── tokens_holdings.csv        # 关系型持仓明细表 (381条持仓：币种, 链, 市值, 占比, 共同持有人数)
    ├── tokens_holdings.json       # 嵌套持仓 JSON 格式
    ├── ml_features.csv            # 专为 AI / ML 训练预归一化的特征工程宽表 (17个量化特征)
    ├── shared_tokens_graph.json   # 交易员交叉持仓二分网络图
    ├── dex_swaps_summary.csv      # 全量 100 位交易员微观执行汇总索引表
    ├── dex_swaps/                 # 全量 100 位交易员真实 DEX 买卖微观交易序列 (3,549 笔 Swap)
    └── sample_dex_swaps/          # 经典样本交易流水
        ├── dumbcrayoneater_swaps.json  # 经典 DEX 狙击手交易流水
        └── unipcs_swaps.json           # 经典机构级高频交易员交易流水
```

---

## 数据字段字典 (Data Schema)

### 1. `data/traders_profiles.csv`

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `rank` | 整数 | 资产规模总排名 (1 至 134) |
| `handle` | 字符串 | 交易员主标识 handle |
| `name` | 字符串 | 显示名称 |
| `x_username` | 字符串 | 关联的 X (Twitter) 用户名 |
| `address_status` | 字符串 | 地址状态 (`unmasked` 已未脱敏 或 `masked`) |
| `evm_address` | 字符串 | 未脱敏 EVM 钱包地址 (对应 Robinhood, Base, BSC, Ethereum) |
| `sol_address` | 字符串 | 未脱敏 Solana 原生钱包地址 (base58) |
| `total_usd` | 浮点数 | 验证的多链资产总估值 (USD) |
| `primary_chain` | 字符串 | 资金沉淀第一大主链 (`hood`, `solana`, `bsc` 等) |
| `evm_usd` | 浮点数 | EVM 体系资产总额 (USD) |
| `sol_usd` | 浮点数 | Solana 体系资产总额 (USD) |
| `hood_usd` | 浮点数 | Robinhood 链资产估值 (USD) |
| `solana_usd` | 浮点数 | Solana 链资产估值 (USD) |
| `bsc_usd` | 浮点数 | Binance Smart Chain 资产估值 (USD) |
| `base_usd` | 浮点数 | Base 链资产估值 (USD) |
| `ethereum_usd` | 浮点数 | Ethereum 链资产估值 (USD) |
| `arc_usd` | 浮点数 | Arc 链资产估值 (USD) |
| `active_chains_count` | 整数 | 余额大于 $10 的活跃链数量 |
| `tokens_count` | 整数 | 主要持仓代币数量 |
| `top_token_symbol` | 字符串 | 最大持仓代币代码 |
| `top_token_usd` | 浮点数 | 最大持仓代币估值 (USD) |
| `top_token_concentration_pct` | 浮点数 | 最大单币持仓占总资产比例 (%) |
| `pnl_24h_usd` | 浮点数 | 24小时盈亏 (USD) |
| `pnl_7d_usd` | 浮点数 | 7天盈亏 (USD) |
| `pnl_30d_usd` | 浮点数 | 30天盈亏 (USD) |
| `volume_usd` | 浮点数 | 记录周期内的交易量 (USD) |
| `trades_count` | 整数 | 记录周期内的交易总笔数 |
| `avg_swap_usd` | 浮点数 | 单笔平均交易规模 (USD) |
| `followers_x` | 整数 | X (Twitter) 粉丝数 |
| `archetype` | 字符串 | 基于持仓规则的分类标签 |
| `hhi_concentration` | 浮点数 | 赫芬达尔持仓集中度指数 |
| `chain_entropy` | 浮点数 | 资金跨链分布香农熵 |
| `network_co_holding_score` | 浮点数 | 与其他 Top 交易员的代币重合共持度均值 |

### 2. `data/tokens_holdings.csv`

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `trader_handle` | 字符串 | 交易员 handle 关联索引 |
| `symbol` | 字符串 | 代币代码 |
| `chain` | 字符串 | 所在区块链 (`hood`, `solana`, `bsc`, `base`, `ethereum`, `arc`) |
| `usd_value` | 浮点数 | 快照时刻持仓美元价值 |
| `portfolio_share_pct` | 浮点数 | 该代币占该交易员总资产比例 (%) |
| `co_holders_count` | 整数 | 同时持有该代币的其他 Top 交易员数量 |

### 3. `data/ml_features.csv`

预处理完成的机器学习特征宽表（134 行，17 列），包含对数资金体量（`log_total_usd`）、各链资产配置比例（`pct_hood`, `pct_sol`, `pct_bsc`, `pct_base`, `pct_eth`, `pct_arc`, `pct_evm_total`）、集中度指数（`hhi_concentration`）及跨链香农熵（`chain_entropy`）。

---

## Python 读取示例

```python
import pandas as pd

# 读取交易员基础画像
traders = pd.read_csv("data/traders_profiles.csv")
print(f"成功加载 {len(traders)} 位交易员，总追踪资产: ${traders['total_usd'].sum():,.2f}")

# 读取代币持仓明细
holdings = pd.read_csv("data/tokens_holdings.csv")
print(f"成功加载 {len(holdings)} 条代币持仓记录。")

# 读取量化建模特征矩阵
features = pd.read_csv("data/ml_features.csv")
print(f"特征矩阵维度: {features.shape}")
```

---

## 开源许可与免责声明

本数据集基于 [MIT 许可证](LICENSE) 开源发布。

本仓库仅供学术研究、数据科学探索与量化建模分析使用，不构成任何形式的投资建议或金融指导。
