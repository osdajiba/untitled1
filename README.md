
# BTC自动交易程序

## 概述

这是一个用于自动交易比特币（BTC）的程序。该程序使用某种特定的交易策略执行自动化的买卖操作。

## 功能特性

- 支持自定义交易策略
- 实时市场数据监测
- 下单和交易执行功能
- 风险管理和资金管理

## 系统要求

- Python 3.3 及以上
- 依赖库（列出所有需要的第三方库，可以包括requirements.txt）

## 安装

1. 克隆仓库到本地

   ```bash
   git clone https://github.com/{yourusername}/BN-auto-trader.git
   ```

2. 进入项目目录

   ```bash
   cd btc-auto-trader
   ```

3. 安装依赖

   ```bash
   pip install -r requirements.txt
   ```

## 配置

1. 复制配置文件模板

   ```bash
   cp config.example.json config.json
   ```

2. 打开 `config.yaml` 文件，配置以下参数：
   - API密钥和密钥密码（如果使用交易所API）
   - 交易策略参数
   - 风险管理参数
   - 其他配置选项

## 运行

运行主程序

   ```bash
   python main.py
   ```

## 交易策略

在 `./lib/strategies` 文件夹中找到并编辑交易策略文件。提供足够的注释和说明以便用户理解和自定义策略。

## 注意事项

- 交易存在风险，使用前请谨慎测试。
- 使用前请先连接全局VPN。
- 请确保你的交易所账户设置正确且具备交易权限。
- 请妥善保护好自己的 API key 和 secret key 避免安全隐患，本项目不提供加密。
- 出现账户亏损或丢失本项目概不负责

## 贡献

欢迎贡献、问题报告和建议。请在 GitHub 上提出问题或提交 Pull Request。

注意，由于基础文件中包含中文字库，无法直接运行'pipreqs .', 所以当你新增导入库后，需要在根目录运行代码：

   ```bash
   pipreqs . --encoding=utf8
   ```

用以重新生成requirements.txt文件

## 许可

MIT License
