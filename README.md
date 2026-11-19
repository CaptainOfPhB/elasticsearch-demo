# elasticsearch-demo

本地 Elasticsearch 练习仓库：Docker 起 **ES 8.17 + IK 中文分词 + Kibana**，用 **Dev Tools Console** 和 **Python** 双轨练习。内容刻意保持简单。

## 环境

| 组件 | 地址 | 说明 |
|------|------|------|
| Elasticsearch | http://localhost:9200 | 8.17.0，已装 `analysis-ik` |
| Kibana | http://localhost:5601 | Dev Tools → Console |

本地关闭了 xpack security，无需账号密码。

## 快速开始

```bash
# 1. 打开 Docker Desktop 后启动（会 build 带 IK 的镜像，首次较慢）
./scripts/up.sh

# 2. 确认 ES 与 IK
curl -s http://localhost:9200 | python3 -m json.tool
curl -s 'http://localhost:9200/_cat/plugins?v'

# 3. Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. 从 CRUD 开始
python demos/01-crud/main.py
```

Dev Tools：打开 http://localhost:5601 → **Dev Tools → Console**，粘贴各 demo 的 `console.http`。需要系统 curl 时用 **Copy as cURL**。

## Demo 列表

| 目录 | 内容 |
|------|------|
| `01-crud` | 建索引、增删改查、bulk |
| `02-mapping` | text vs keyword |
| `03-search` | match / term / range / bool |
| `04-analyzer-ik` | IK 分词 + 中文检索高亮 |
| `05-bm25` | BM25 的 k1/b 对比与 `_explain` |
| `06-agg` | terms / avg / sum |

建议顺序：`01 → 02 → 03 → 04 → 05 → 06`。

## 目录结构

```
├── docker/elasticsearch/Dockerfile   # 官方 ES + analysis-ik
├── docker-compose.yml
├── data/
│   ├── products.ndjson               # 商品（CRUD / search / agg）
│   └── articles.ndjson               # 中文文章（IK）
├── shared/                           # Python 客户端与小工具
├── scripts/                          # up / down / reset-data
└── demos/0x-*/                       # 每课：README + console.http + main.py
```

## 常用命令

```bash
./scripts/down.sh          # 停容器（保留数据卷）
./scripts/reset-data.sh    # 删卷并空集群重启
docker compose logs -f elasticsearch
docker compose build elasticsearch --no-cache   # 强制重装 IK 镜像
```
