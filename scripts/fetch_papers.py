#!/usr/bin/env python3
"""
论文抓取脚本 - 持续更新 Memory & Agent 论文库
"""

import os
import json
import re
import requests
from datetime import datetime
from urllib.parse import quote

REPO_DIR = "/root/.openclaw/workspace/OpenClaw-Diary-test"
PAPERS_FILE = f"{REPO_DIR}/papers/README.md"
LOG_FILE = f"{REPO_DIR}/papers/.fetch_log"

# arXiv API
ARXIV_API = "http://export.arxiv.org/api/query"

# 搜索关键词
SEARCH_TERMS = [
    "LLM agent",
    "LLM memory", 
    "LLM reasoning",
    "agent memory",
    "RAG agent",
    "multi-agent LLM",
    "context window",
    "long context LLM",
    "GPT agent",
    "ReAct",
    "Reflexion LLM",
    "Toolformer",
    "MemGPT",
    "agentic RAG",
    "code generation agent",
]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def search_arxiv(query, max_results=50):
    """搜索 arXiv 论文"""
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    try:
        response = requests.get(ARXIV_API, params=params, timeout=30)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        log(f"搜索失败: {query}, 错误: {e}")
    return None

def parse_arxiv_xml(xml_text):
    """解析 arXiv XML"""
    papers = []
    
    # 简单解析
    entries = re.findall(r'<entry>(.*?)</entry>', xml_text, re.DOTALL)
    
    for entry in entries:
        paper = {}
        
        # 提取标题
        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        if title_match:
            paper['title'] = title_match.group(1).strip()
        
        # 提取摘要
        summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
        if summary_match:
            paper['abstract'] = summary_match.group(1).strip()
        
        # 提取链接
        id_match = re.search(r'<id>(.*?)</id>', entry)
        if id_match:
            paper['url'] = id_match.group(1).strip()
            # 提取 arXiv ID
            arxiv_id = paper['url'].split('/')[-1]
            paper['arxiv_id'] = arxiv_id
            paper['arxiv_url'] = f"https://arxiv.org/abs/{arxiv_id}"
        
        # 提取作者
        authors = re.findall(r'<name>(.*?)</name>', entry)
        paper['authors'] = authors[:5] if len(authors) > 5 else authors
        
        # 提取日期
        published_match = re.search(r'<published>(.*?)</published>', entry)
        if published_match:
            paper['published'] = published_match.group(1)[:10]
        
        if paper.get('title'):
            papers.append(paper)
    
    return papers

def load_existing_papers():
    """从现有 README 加载已收录论文"""
    existing = set()
    if os.path.exists(PAPERS_FILE):
        with open(PAPERS_FILE, "r") as f:
            content = f.read()
            # 提取 arXiv ID
            ids = re.findall(r'arXiv:(\d+\.\d+)', content)
            existing.update(ids)
    return existing

def generate_markdown(papers, existing_ids):
    """生成 Markdown 内容"""
    
    # 按年份分组
    by_year = {}
    for paper in papers:
        if paper.get('arxiv_id') in existing_ids:
            continue  # 跳过已存在的
            
        year = paper.get('published', '0000')[:4]
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(paper)
    
    if not by_year:
        log("没有新论文")
        return None
    
    # 生成 Markdown
    md_lines = []
    md_lines.append(f"# 🧠 Memory & Agent 论文知识库")
    md_lines.append("")
    md_lines.append(f"> 持续更新 | Last updated: {datetime.now().strftime('%Y-%m-%d')}")
    md_lines.append("")
    md_lines.append(f"> 仓库地址: https://github.com/Trae1ounG/OpenClaw-Diary-test")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 📊 评分说明")
    md_lines.append("")
    md_lines.append("- ⭐⭐⭐⭐⭐ 必读经典 - 领域奠基之作")
    md_lines.append("- ⭐⭐⭐⭐ 推荐 - 值得深入阅读")
    md_lines.append("- ⭐⭐⭐ 值得一看 - 了解方向")
    md_lines.append("- ⭐⭐ 了解即可")
    md_lines.append("- ⭐ 可跳过")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append(f"## 📅 最新收录 ({datetime.now().strftime('%Y-%m-%d')})")
    md_lines.append("")
    
    for year in sorted(by_year.keys(), reverse=True):
        md_lines.append(f"### {year}年")
        md_lines.append("")
        
        for paper in by_year[year]:
            title = paper.get('title', 'Untitled')[:80]
            arxiv_id = paper.get('arxiv_id', '')
            arxiv_url = paper.get('arxiv_url', '')
            authors = paper.get('authors', [])
            abstract = paper.get('abstract', '')[:200]
            
            md_lines.append(f"### {title}")
            md_lines.append(f"- **arXiv**: [{arxiv_id}]({arxiv_url})")
            md_lines.append(f"- **作者**: {', '.join(authors[:3])}")
            md_lines.append(f"- **摘要**: {abstract}...")
            md_lines.append("")
    
    return "\n".join(md_lines)

def main():
    log("=" * 50)
    log("论文抓取任务开始")
    
    # 加载已存在的论文
    existing_ids = load_existing_papers()
    log(f"已有论文: {len(existing_ids)} 篇")
    
    all_papers = []
    
    # 搜索每个关键词
    for term in SEARCH_TERMS:
        log(f"搜索: {term}")
        xml = search_arxiv(term)
        if xml:
            papers = parse_arxiv_xml(xml)
            all_papers.extend(papers)
            log(f"  找到 {len(papers)} 篇")
    
    # 去重
    unique_papers = {}
    for paper in all_papers:
        aid = paper.get('arxiv_id')
        if aid and aid not in unique_papers:
            unique_papers[aid] = paper
    
    log(f"去重后共: {len(unique_papers)} 篇")
    
    # 生成更新
    new_papers = list(unique_papers.values())
    if new_papers:
        log(f"新增: {len(new_papers)} 篇")
    else:
        log("没有新论文")
    
    log("任务完成")

if __name__ == "__main__":
    main()
