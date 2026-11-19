# ES 8.17.0 + analysis-ik（版本必须与 ES 一致）
FROM docker.elastic.co/elasticsearch/elasticsearch:8.17.0

RUN bin/elasticsearch-plugin install --batch \
  https://release.infinilabs.com/analysis-ik/stable/elasticsearch-analysis-ik-8.17.0.zip
