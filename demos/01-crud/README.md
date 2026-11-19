# 01-crud

练习索引与文档的增删改查，以及 bulk 批量写入。

## 目标

- 创建带显式 mapping 的索引
- 单条 index / get / update / delete
- `_bulk` 批量导入
- `_refresh` 后 `match_all` 查看结果

## 准备

确保 ES + Kibana 已启动（见根目录 README）。

## 方式 A：Python

```bash
# 在仓库根目录
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python demos/01-crud/main.py
```

脚本会重建 `products` 索引、导入 `data/products.ndjson`，并演示临时文档的 CRUD。

## 方式 B：Kibana Dev Tools（推荐对照着练）

1. 打开 http://localhost:5601
2. 进入 **Dev Tools → Console**
3. 打开本目录的 [`console.http`](./console.http)，按注释分段粘贴执行

Console 语法就是官方文档里的 REST 风格；需要 curl 时，在 Console 里选中请求 → 点扳手/复制为 cURL 即可。

## 预期

- `GET /products/_search` + `match_all` 能看到多条商品
- 更新 `price` 后 `GET /products/_doc/1` 字段已变
- 删除某 `_id` 后再搜不到该文档
