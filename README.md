## 🚀 Назначение

Telegram‑бот создаёт чек‑лист задач, используя GPT‑4o и **Model Context Protocol (MCP)** — стандартный мост между LLM и внешними сервисами ([Model Context Protocol][1], [Anthropic][2]).
Интеграции («серверы» MCP) дают доступ к Google Drive, Notion и GitHub Projects без прямых API‑обёрток ([GitHub][3], [GitHub][4], [GitHub][5]).

---

## ⚙️ Архитектура (MCP‑термины)

| Слой                      | Роль                                                                                                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MCP Servers**           | готовые Docker‑контейнеры: <br>• Drive Server (поиск/чтение) ([GitHub][3]) <br>• Notion Server (поиск/CRUD) ([GitHub][4]) <br>• GitHub Server (issues/PR/Projects) ([GitHub][5]) |
| **MCP Host** (`src/host`) | держит Telegram‑бота, OpenAI‑клиент и MCP‑клиентов (python‑sdk) ([GitHub][6]); маршрутизирует `function_call → server.tool`                                                      |
| **LLM**                   | GPT‑4o через OpenAI API (function calling)                                                                                                                                       |
| **UI Client**             | `python-telegram-bot` слушает чат, передаёт сообщения Host’у ([python-telegram-bot.org][7], [GitHub][8])                                                                         |

Sequence: **User → Bot → Host → GPT‑4o ↔ MCP Servers → Host → Bot → User**.


## 📁 Структура репозитория

```
checklist_bot/
├─ docker-compose.yml   # three MCP servers
├─ .env.example         # OPENAI_API_KEY, GITHUB_PAT, NOTION_TOKEN, GOOGLE_CRED
├─ prompts/             # system_prompt.md
└─ src/
   ├─ host/
   │  ├─ config.py      # env & server URIs
   │  ├─ mcp_clients.py # Client("ws://...") per server
   │  ├─ llm.py         # OpenAI call + tool loop
   │  └─ router.py      # executes tool → returns result
   └─ clients/
      └─ telegram_bot.py
```

## 🛠️ Быстрый запуск

```bash
git clone …
cp .env.example .env   # заполнить ключи
docker-compose up -d   # запускаем Drive/Notion/GitHub MCP
pip install -r requirements.txt
python -m src.clients.telegram_bot
```

Напишите «@ChecklistBot Новая фича …» — бот создаст задачу в GitHub Projects с DoD и ссылками.

### 🔗 Ссылки на используемые MCP‑серверы

* Google Drive MCP Server — GitHub repo isaacphi/mcp-gdrive ([GitHub][3])
* Notion MCP Server — makenotion/notion-mcp-server ([GitHub][4])
* GitHub MCP Server — github/github-mcp-server ([GitHub][5])

Доп. ресурсы: MCP Intro ([Model Context Protocol][1]), Python SDK ([GitHub][6]), MCP client quick‑start ([Model Context Protocol][9]).

### 👩‍💻 Как доработать

1. **Новый сервер** → добавить сервис в `docker-compose`, указать URI в `.env`.
2. **Новая логика** → расширить `prompts/system_prompt.md`.
3. **Безопасность** → выдать MCP‑серверу токен с минимальными правами (Drive read‑only, Notion – только нужные страницы, GitHub – `projects, issues` scopes).

[1]: https://modelcontextprotocol.io/introduction?utm_source=chatgpt.com "Model Context Protocol: Introduction"
[2]: https://www.anthropic.com/news/model-context-protocol?utm_source=chatgpt.com "Introducing the Model Context Protocol - Anthropic"
[3]: https://github.com/isaacphi/mcp-gdrive?utm_source=chatgpt.com "isaacphi/mcp-gdrive: Model Context Protocol (MCP) Server ... - GitHub"
[4]: https://github.com/makenotion/notion-mcp-server?utm_source=chatgpt.com "GitHub - makenotion/notion-mcp-server"
[5]: https://github.com/github/github-mcp-server?utm_source=chatgpt.com "GitHub's official MCP Server"
[6]: https://github.com/modelcontextprotocol/python-sdk?utm_source=chatgpt.com "modelcontextprotocol/python-sdk - GitHub"
[7]: https://python-telegram-bot.org/?utm_source=chatgpt.com "python-telegram-bot"
[8]: https://github.com/python-telegram-bot/python-telegram-bot?utm_source=chatgpt.com "python-telegram-bot/python-telegram-bot: We have made ... - GitHub"
[9]: https://modelcontextprotocol.io/quickstart/client?utm_source=chatgpt.com "For Client Developers - Model Context Protocol"
