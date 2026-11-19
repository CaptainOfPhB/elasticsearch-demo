# 04-analyzer-ik

中文 IK 分词：`ik_smart` / `ik_max_word`，以及检索高亮。

## 前提

镜像需带 `analysis-ik`（本仓库 `docker/elasticsearch/Dockerfile`）：

```bash
docker compose build elasticsearch
./scripts/up.sh
# 验证
curl -s 'http://localhost:9200/_cat/plugins?v'
```

## 约定

| 用途 | analyzer |
|------|----------|
| 写入索引 | `ik_max_word`（切得细，召回更好） |
| 搜索查询 | `ik_smart`（切得更合理） |

## 运行

```bash
python demos/04-analyzer-ik/main.py
# Dev Tools：console.http
```

## 预期

- `standard` 对中文几乎按字/奇怪切分；IK 能切出「机械键盘」等词
- `match content=机械键盘` 能命中相关文章，并有 highlight
