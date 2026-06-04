# Biotech Research Agent 🧬

自主买方生物技术基本面研究代理。输入公司代码，自动生成机构级深度研究报告。

## 功能特性

- 🔬 **疾病生物学分析** - 靶点疾病、MoA、流行病学评估
- 💊 **临床数据提取** - ORR、PFS、OS、安全性指标从ClinicalTrials.gov
- 🏥 **竞争格局** - 竞争对手管线、定价、标准护理
- 💰 **风险调整估值** - rNPV、PoS、峰值销售预测
- 📊 **投资论文** - 异见观点、催化剂、机构级报告

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/junweima-1234/biotech-research-agent.git
cd biotech-research-agent

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑.env，添加API密钥：
# - GEMINI_API_KEY
# - TAVILY_API_KEY

# 4. 运行代理
python -m biotech_agent analyze --ticker AMGN --company "Amgen"
```

## 使用示例

### CLI 命令

```bash
# 基础分析
python -m biotech_agent analyze --ticker AMGN --company "Amgen"

# 输出为JSON格式
python -m biotech_agent analyze --ticker NVAX --company "Novavax" --format json

# 详细模式（打印日志）
python -m biotech_agent analyze --ticker BNTX --company "BioNTech" --verbose

# 指定输出文件
python -m biotech_agent analyze --ticker MRNA --company "Moderna" --output report.json
```

## 架构

```
输入（公司代码）
    ↓
[编排器 Orchestrator]
    ↓
并行执行5个工作者：
  ├─→ [工作者1] 疾病生物学
  ├─→ [工作者2] 临床数据
  ├─→ [工作者3] 竞争格局
  ├─→ [工作者4] 估值
  └─→ [工作者5] 综合
    ↓
输出：机构级研究报告（JSON/Markdown）
```

## 项目结构

```
biotech-research-agent/
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── lint.yml
├── src/
│   ├── orchestrator.py
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── disease_biology.py
│   │   ├── drug_profile.py
│   │   ├── commercialization.py
│   │   ├── valuation.py
│   │   └── synthesis.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── web_search.py
│   │   ├── llm_interface.py
│   │   └── config.py
│   └── schemas/
│       ├── __init__.py
│       └── models.py
├── tests/
├── examples/
│   └── analyze_company.py
├── docs/
├── requirements.txt
├── .env.example
├── .gitignore
└── setup.py
```

## 环境要求

- Python 3.9+
- Google Gemini API密钥
- Tavily搜索API密钥

## 更新日志

- v0.1.0：项目初始化，CLI框架搭建

## 贡献

欢迎贡献代码！请提交Pull Request。

## License

MIT
