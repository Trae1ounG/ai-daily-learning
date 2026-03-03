#!/bin/bash
# 论文抓取脚本 - 持续运行

REPO_DIR="/root/.openclaw/workspace/OpenClaw-Diary-test"
PAPERS_FILE="$REPO_DIR/papers/README.md"
LOG_FILE="$REPO_DIR/papers/.fetch_log"

# 搜索关键词
KEYWORDS=("LLM agent" "LLM memory" "LLM reasoning" "agent memory" "RAG agent" "multi-agent LLM" "context window" "long context")

echo "=== 论文抓取开始 $(date) ===" >> $LOG_FILE

# 获取最新论文并更新
for keyword in "${KEYWORDS[@]}"; do
    echo "搜索: $keyword" >> $LOG_FILE
    
    # 这里可以调用 arXiv API 或其他论文源
    # 然后更新 papers/README.md
    
    echo "完成: $keyword" >> $LOG_FILE
done

echo "=== 抓取完成 $(date) ===" >> $LOG_FILE
