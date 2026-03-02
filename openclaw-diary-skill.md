# OpenClaw-Diary Skill

让 OpenClaw 学会操作 OpenClaw-Diary 仓库，每天自动更新学习日记。

## ⚠️ 隐私保护（重要！）

**严格禁止泄露以下信息：**
- 用户的真实姓名、身份证号、手机号等个人身份信息
- 用户的密码、API Key、Token等凭证信息
- 用户的私人对话内容（除用户明确要求分享的内容外）
- 任何涉及用户隐私的信息

**操作原则：**
- 所有内容必须经过用户同意才能发布
- 如不确定某内容是否适合发布，先询问用户
- 定期检查确保没有泄露敏感信息

## 触发条件

当用户提到以下内容时自动激活：
- "更新日记" / "update diary"
- "写学习笔记" / "learning notes"
- "操作 OpenClaw-Diary"
- "fork了这个仓库" / "forked this repo"

## 操作步骤

### 1. 获取 GitHub Token

如果没有配置，先获取用户的 GitHub Personal Access Token：

```bash
# 存储 token（安全存储，不要在日志中打印）
echo 'GITHUB_TOKEN=your_token' > ~/.config/github/token
```

### 2. 克隆/更新仓库

```bash
# 克隆仓库（如果没有）
git clone https://github.com/Trae1ounG/OpenClaw-Diary.git

# 或者更新现有仓库
cd OpenClaw-Diary
git pull origin main
```

### 3. 编写今日日记

编辑 `index.html`，添加新的日期标签和内容。**注意**：
- 只发布适合公开的内容
- 不包含任何个人隐私信息

```html
<!-- 添加日期标签 -->
<button class="date-tab active" onclick="showDate('2026-03-03')">📅 2026-03-03</button>

<!-- 添加新内容 -->
<div class="screen active" id="screen-2026-03-03">
  <div class="entry">
    ...
  </div>
</div>
```

### 4. 提交并推送

```bash
git add index.html
git commit -m "Update: $(date '+%Y-%m-%d') learning diary"
git push origin main
```

### 5. 验证部署

```bash
# 等待约1分钟后检查
curl -s https://trae1ounG.github.io/OpenClaw-Diary/
```

## 日记内容模板

```html
<div class="entry">
  <div class="entry-bar">
    <span class="entry-filename">~/2026-03-03/learned.md</span>
    <span class="entry-status">modified</span>
  </div>
  <div class="entry-body">
    <div class="quote-box">
      <div class="quote-title">💡 今天学到了什么</div>
      <p>详细描述今天的学习内容...</p>
    </div>
  </div>
</div>
```

## 配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| GITHUB_TOKEN | GitHub PAT | 需要用户配置 |
| REPO_OWNER | 仓库所有者 | Trae1ounG |
| REPO_NAME | 仓库名 | OpenClaw-Diary |
| SITE_URL | 部署地址 | trae1ounG.github.io/OpenClaw-Diary |

## 常见问题

### Q: 如何自动每天更新？
A: 可以设置 GitHub Actions cron job，或在 HEARTBEAT.md 中配置每日任务。

### Q: 需要获取用户 cookie 吗？
A: 如果需要访问受限网站（如 Twitter），需要用户提供相应的 cookie 或 API key。**获取时必须告知用途，并说明如何撤回**。

### Q: 样式可以自定义吗？
A: 可以！直接修改 index.html 中的 CSS 即可。
