---
type: concept
title: "연구보조 시스템 - 초심자 튜토리얼"
subtitle: "Obsidian + Claude Code 7일 셋업 가이드"
author: "문제웅"
affiliation: "The University of Alabama"
contact: "jmoon19@ua.edu"
created: 2026-05-02
updated: 2026-05-02
audience: beginner
tags:
  - guide
  - tutorial
  - beginner
status: active
related:
  - "[[Research Assistant System Guide]]"
---

{{DIAGRAM:hero}}

# 연구자를 위한 AI 보조 시스템 — 초심자 가이드

> **이 가이드는 누구를 위한 것인가?** 본인이 박사과정 / 신진교수 / 연구원이고, *수십 개 프로젝트가 폴더 곳곳에 흩어져 있고*, *"지난주에 그 그랜트 마감이 언제였지?"를 자주 검색해야 하고*, *Claude Code/ChatGPT를 쓰지만 매번 같은 배경설명을 반복하고 있다면* — 이 가이드가 본인을 위한 것입니다.
>
> **결과물**: 본인의 모든 프로젝트·방법론·학생·그랜트가 하나의 검색 가능한 지식 그래프에 들어가고, AI가 작업할 때마다 자동으로 노트를 남기고, 새 정보가 들어올 때마다 그래프가 자동 갱신됩니다.

---

## 왜 이걸 해야 할까?

지금 본인의 작업 환경은 아마 이렇게 생겼을 겁니다:

{{DIAGRAM:before-after}}

**왼쪽**: 데스크탑에 PDF, docx, png가 흩어져 있고, 프로젝트 폴더는 16개, *"그 프로젝트 메서드 설명을 어디에 적었더라?"* 검색이 매일 일어남.

**오른쪽**: 모든 프로젝트가 vault 안 entity 페이지로 정리되고, 자동 트래커가 새 노트를 처리하고, AI에게 *"내 프로젝트 X에 대해 알려줘"* 한 줄로 모든 컨텍스트를 받음.

이 가이드를 끝까지 따라가면 오른쪽 상태에 도달합니다. **하루 1-2시간씩 7일.**

---

## 0. 시작 전 — 용어 사전

본격적으로 들어가기 전, 가이드 전체에 반복해서 등장하는 7개 용어를 한 번에 정리합니다. 이미 익숙하면 다음 섹션으로 넘어가도 됩니다.

| 용어 | 한 줄 설명 | 비유 |
|---|---|---|
| **Vault** | Obsidian의 노트 저장소 = 그냥 마크다운(`.md`) 파일이 모여있는 폴더 한 개 | "내 모든 노트가 들어있는 책장" |
| **Entity 페이지** | 사물·개념·사람 한 명에 대한 노트 한 장 (`wiki/entities/Project A.md`) | 위키피디아의 "한 항목" |
| **Frontmatter** | 마크다운 파일 맨 위 `---` 사이 YAML 메타데이터. 컴퓨터가 자동으로 분류·검색에 쓰는 라벨 영역 | 책 표지 안쪽의 도서 정보 페이지 |
| **Wikilink** | `[[프로젝트 A]]` 같은 옵시디언 문법. 다른 페이지로의 연결. 자동 추적·검색됨 | 위키 안에서의 하이퍼링크 |
| **Hook** | 특정 이벤트(세션 종료, 파일 변경 등)가 일어나는 순간 자동 실행되는 명령 | 도어벨 — 누군가 오면 자동으로 울림 |
| **Ontology (온톨로지)** | "타입(Person·Project·Grant 등)과 관계(hasPI·advises·uses 등)"로 본인의 vault를 표현한 구조화된 그래프. 검색·질의 가능 | 가계도 + 조직도를 합친 것 |
| **API key** | OpenRouter 같은 외부 LLM 서비스를 호출할 때 본인을 인증하는 비밀 문자열 | 도서관 회원증 (대출시 제시) |

> 💡 **개념 → 파일 매핑**: 각 entity는 `.md` 파일 한 개. frontmatter가 그 파일이 어떤 *타입* 인지 명시 (`type: project`). wikilink가 다른 entity와 *관계*를 만듭니다. 이 세 가지가 모이면 자동으로 ontology가 만들어집니다.

---

## 0.5. AI Agents — Claude Code와 Codex의 역할 분담

이 시스템은 두 개의 AI 코딩 agent를 **상호 보완적으로** 사용합니다. 둘 다 LLM을 백엔드로 쓰지만, **누가 무엇을 잘 하는지**가 다르고 **어떻게 컨트롤하는지**도 다릅니다.

{{DIAGRAM:agents}}

### 두 agent, 두 역할

**Claude Code** (Anthropic) — *주(主) engineering agent*
- vault에 깊게 통합됨 (Stop hook으로 세션 자동 기록, 슬래시 커맨드 `/slides` `/recall` 사용 가능)
- 긴 컨텍스트 (200K-1M 토큰) — vault 전체를 컨텍스트로 끌어올 수 있음
- 강점: 다단계 reasoning, 신중한 파일 수정, vault navigation, 컨벤션 따르기
- 어디서: vault의 모든 파일 직접 읽고 쓰기 (frontmatter 추가, entity 생성, ontology rebuild 트리거)

**Codex** (OpenAI) — *보조 engineering agent*
- 세션 저장소가 `~/.codex/sessions/` (rollout JSONL 형식). Stop hook은 없음 — 세션 끝나면 `pwsh codex_digest.ps1` 수동 실행
- 강점: 빠른 코드 생성 / 이미지 생성 / Reasoning 모델로 어려운 문제 풀기
- 어디서: 코드 새로 짤 때, Claude가 막힐 때 cross-check, 빠른 prototype

### 어느 쪽을 언제 쓸까

| 상황 | 추천 |
|---|---|
| **vault 페이지 작성/수정** (entity 추가, frontmatter 정리) | **Claude Code CLI** — Stop hook이 자동 기록 |
| **새 스크립트 짜기** (Python/PowerShell) | 둘 다 가능. Codex가 reasoning 모드에서 더 빠를 때 있음 |
| **여러 파일 리팩터링** | **Claude Code** — 다단계 수정 안정적 |
| **막힐 때 두 번째 의견** | 같은 질문을 두 agent에 던지고 비교 |
| **이미지 / mockup 생성** | **Codex** — image_generation 도구 보유 |
| **빠른 챗 / "이게 뭐지?"** | **Claude Desktop app** (GUI, MCP 연결) |
| **세션 디제스트 자동 기록** | **Claude Code** (자동) — Codex는 수동 |

### CLI 컨트롤 — 가장 중요한 5가지

**(1) 어디서 실행하면 컨텍스트가 자동 잡히는가**
```powershell
cd C:\Users\<you>\ObsidianVault   # vault 안에서 실행
claude                              # Claude Code CLI 시작
# 또는
codex                               # Codex CLI 시작
```
두 agent 모두 *현재 디렉토리부터 부모 폴더로 거슬러 올라가며* 다음을 자동 로드:
- Claude Code: `CLAUDE.md` (vault 안 + 사용자 홈 둘 다 인식)
- Codex: `AGENTS.md` (관례) + 사용자 홈 `~/.codex/AGENTS.md`

**즉**: vault 안에서 켜면 가이드가 자동 로드되어 *"내 프로젝트 X 알려줘"* 한 줄로 답이 나옵니다.

**(2) Hook 등록 — Claude Code 전용 (Codex는 미지원)**

`~\.claude\settings.json`:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [{
          "type": "command",
          "command": "powershell.exe -File <vault>\\scripts\\save_session.ps1 -Source claude"
        }]
      }
    ]
  }
}
```

지원하는 이벤트: `Stop` (세션 종료), `SessionStart`, `PostToolUse`, `PreToolUse`, `UserPromptSubmit` 등. 우리는 `Stop`만 씀.

**(3) Slash Commands — Claude Code 전용**

`~\.claude\commands\<name>.md` 파일을 만들면 `/<name> <args>` 로 호출 가능. 예: `/slides ProjectA` → `slides.md` 의 prompt 실행.

**(4) Memory — Claude Code 자동 컨텍스트**

`~\.claude\projects\<machine>\memory\MEMORY.md` 가 모든 세션 시작 시 자동 컨텍스트로 주입됨. 이 파일에 *"~~ 이 프로젝트의 메서드 기억해 둬"* 식으로 적어두면 다음 세션부터 자동 인식.

**(5) Codex 세션 후 디제스트 — 3가지 방법**

> 💡 **정정**: Codex CLI에는 Claude Code 같은 *이벤트 hook* (Stop/SessionStart 등)이 **없습니다**. 다만 Codex는 다른 종류의 자동화 — *스케줄 기반 cron* — 을 지원합니다 (`~/.codex/automations/`). 같은 효과를 3가지 방법으로 만들 수 있음:

**방법 A — 수동 (가장 간단)**:
```powershell
# Codex 세션 끝난 직후
pwsh C:\Users\<you>\ObsidianVault\scripts\codex_digest.ps1
```

**방법 B — 셸 wrapper로 "자동 Stop hook 흉내"**:

PowerShell `$PROFILE`에 함수 추가:
```powershell
function cdx {
  codex @args
  pwsh "$env:USERPROFILE\ObsidianVault\scripts\codex_digest.ps1"
}
```

이제 `codex` 대신 `cdx` 쓰면 — 세션 종료시 자동으로 디제스트 실행됨. Bash/zsh도 동일 (`alias` 또는 `function`).

**방법 C — Codex automation으로 주기적 자동 디제스트**:

Codex의 RRULE-기반 cron 시스템 사용. `~/.codex/automations/vault-digest/automation.toml`:
```toml
version = 1
id = "vault-digest"
kind = "cron"
name = "Vault session digest"
prompt = "Run the latest Codex rollout through the vault digest pipeline by executing: pwsh C:\\Users\\<you>\\ObsidianVault\\scripts\\codex_digest.ps1"
status = "ACTIVE"
rrule = "FREQ=HOURLY;INTERVAL=2"
model = "gpt-5.4"
reasoning_effort = "low"
execution_environment = "worktree"
```

→ Codex가 매 2시간마다 자동으로 최신 세션을 디제스트. **단점**: Codex 자체가 실행되어야 (Codex Cloud 또는 desktop 켜져있어야).

→ 최근 `~/.codex/sessions/` 또는 `archived_sessions/` 의 JSONL을 자동 찾아 LLM 요약 후 vault `wiki/sources/Sessions <date>.md` 에 추가.

> 💡 **결론**: *진짜* 이벤트-즉시 자동 기록 = Claude Code Stop hook이 유일. *유사 효과*는 Codex에서 wrapper (방법 B) 또는 automation (방법 C) 로 가능. 둘 다 같은 vault 같은 entity 페이지를 본다는 점이 핵심이라 95% 상호교체 가능.

### Desktop 앱과의 차이

**Claude Desktop** (Claude.ai 데스크탑 앱):
- Hook 시스템 **없음** — Stop 훅이 안 걸림
- MCP (Model Context Protocol) 서버 **있음** — `obsidian-vault` MCP를 연결하면 vault에 직접 read/write 가능
- 슬래시 커맨드 **없음** (CLI만)
- 메모리는 동일 backend라 작동
- 권장 사용: *"vault 콘텐츠로 대화하고 싶을 때"* — 빠른 질의·브레인스토밍

**Codex Desktop** (VS Code 안 또는 standalone):
- Hook 시스템 **없음**
- 자동 세션 archive는 동일하게 `~/.codex/archived_sessions/` 에 저장됨
- VS Code 안에서는 IDE 통합 (파일 트리 / diff / git) 가시적
- 권장 사용: *"코드 짜면서 IDE 안에서 바로"* — 코드 작업

> 💡 **결론**: 본격 vault 작업 (entity 페이지 작성, 자동화 hook, 슬래시 커맨드 사용) = **Claude Code CLI**. 빠른 채팅 / vault 콘텐츠 대화 = **Claude Desktop + MCP**. 코드 생성 backup = **Codex** (CLI 또는 Desktop). 셋 다 같은 vault를 본다는 점이 핵심.

### MCP 연결 (Claude Desktop만 — 선택)

vault를 Claude Desktop에 연결하면 desktop 앱이 vault에 직접 read/write 가능:

1. Claude Desktop 설치
2. `claude_desktop_config.json` 편집:
```json
{
  "mcpServers": {
    "obsidian-vault": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "C:\\Users\\<you>\\ObsidianVault"]
    }
  }
}
```
3. Claude Desktop 재시작 → "🔌" 아이콘에 obsidian-vault 보이면 성공

**이러면**: Claude Desktop에서 *"내 vault에서 Project A 페이지 보여줘"* 하면 직접 파일을 읽어 답합니다. Hook은 여전히 없지만 vault navigation은 가능.

> ⚠️ **Hook이 필요한 자동화는 무조건 CLI**. Desktop 앱은 채팅 / vault 탐색 보조 도구로만.

---

## 1. 핵심 개념 — 3층짜리 두 번째 뇌

복잡해 보일 수 있는데, 이 시스템은 사실 *세 층의 노트 저장소*에 자동화 한 겹을 씌운 것뿐입니다:

{{DIAGRAM:mental-model}}

**1층 — 프로젝트 지식 (`wiki/entities/`, `wiki/concepts/`)**: 본인이 직접 쓰는 노트. 각 프로젝트, 학생, 메서드, 그랜트가 한 페이지씩. 이건 본인이 *영구히* 갖고 갈 자산입니다.

**2층 — 활동 로그 (`wiki/activity/`, `wiki/situation/`, `wiki/sources/Sessions YYYY-MM-DD.md`)**: 자동 생성되는 일별 스냅샷. *"지난주에 뭐 했더라"*에 답하는 용도. 컴퓨터가 알아서 채웁니다.

**3층 — AI 메모리 (`~/.claude/projects/<machine>/memory/`)**: Claude Code가 새 세션 시작할 때 자동으로 읽는 작은 파일들. 본인의 프로젝트·취향·관계를 매번 다시 설명하지 않아도 되게 해줍니다.

> 💡 **외워둘 한 줄**: *내가 쓴다 (1층) → 컴퓨터가 매 2시간 갱신한다 (2층) → AI가 다음 세션에서 자동으로 읽는다 (3층).*

---

## 2. 자동화 흐름 — "매 2시간 어떤 일이 일어나는가"

{{DIAGRAM:tracker-flow}}

**Windows 예약 작업** (또는 macOS launchd, Linux cron)이 매 2시간 (`00:00, 02:00, 04:00, ..., 22:00`)에 한 번씩 작은 PowerShell 스크립트를 돌립니다. 이 스크립트가:

1. 새로 추가된 파일 / 수정된 파일을 스캔
2. Git 커밋, GitHub 활동, Outlook 캘린더 등 곁가지 신호 수집
3. 본인의 vault에서 노트 변경사항을 LLM에 보내 *"뭐가 바뀌었는지"* 판단 (e.g., 새 마감일 발견 → entity 페이지에 자동 추가)
4. **온톨로지 그래프 재구축** — vault 전체를 스캔해서 *"누가 어떤 프로젝트의 PI고, 어떤 메서드를 쓰는지"* JSON 그래프로 export
5. 결과를 `Today.md`에 모아서 본인이 다음에 vault를 열 때 한눈에 보이게

비용: 한 번에 ~$0.001-0.005 (LLM이 새 변화를 판단할 때만). 하루 12회 = 약 **$0.02-0.05/일** = 한 달 1-2달러.

---

## 3. 시작하기 전에 필요한 것

{{DIAGRAM:checklist}}

7일 동안 차근차근 갖춰갈 것이라 처음부터 다 있을 필요 없습니다. **Day 1 시작 시점에 필요한 것만**:

- [ ] **Obsidian 설치** ([obsidian.md](https://obsidian.md), 무료) — 본인의 vault UI
- [ ] **Claude Code 설치 및 로그인** ([claude.com/claude-code](https://claude.com/claude-code)) — AI agent
- [ ] **Python 3.11 이상** (스크립트 돌리는 용도)
- [ ] 기본 터미널 사용 능력 (cd, ls 정도)

**Day 4 이후 필요**:
- [ ] **OpenRouter API key** ([openrouter.ai](https://openrouter.ai), $5 충전이면 몇 달 씀) — LLM 판단 호출용
- [ ] **`gh` CLI** ([cli.github.com](https://cli.github.com)) — GitHub 활동 수집 (선택)

> ⚠️ **이 가이드는 Windows 기준**이지만, macOS / Linux도 path 약간만 바꾸면 동일합니다. PowerShell이 Bash로 바뀌는 정도.

---

## Day 1 — Vault 만들기

**오늘의 목표**: Obsidian으로 빈 vault를 만들고, 본인의 가장 활발한 프로젝트 하나에 대한 entity 페이지를 손으로 작성합니다. 자동화는 아직 없습니다.

### 단계 1.1 — Vault 생성

Obsidian 실행 → "Create new vault" → 이름은 `ResearchVault`, 위치는 `C:\Users\<you>\ObsidianVault\` (이 경로를 가이드에서 계속 사용합니다).

### 단계 1.2 — 폴더 구조

vault 안에 직접 다음 빈 폴더를 만들어주세요 (Obsidian 좌측 패널에서 우클릭 → New folder):

```
ObsidianVault/
└── wiki/
    ├── entities/        ← 프로젝트 / 사람 / 그랜트 한 페이지씩
    ├── concepts/        ← 메서드 / 이론 한 페이지씩
    ├── sources/         ← 원본 문서 / 디제스트 / 세션 로그
    └── (activity/, situation/는 나중에 자동 생성됨)
```

### 단계 1.3 — 첫 entity 페이지

가장 활발한 프로젝트 하나만 선택하세요. 아래 예시는 가상의 *Project A*를 사용 — 본인 프로젝트 이름으로 바꿔 쓰시면 됩니다. `wiki/entities/Project A.md` 새 파일 생성:

```markdown
---
type: project
title: "Project A"
status: active
tier: 2
deadline: 2026-08-15
related:
  - "[[<나의 이름>]]"
  - "[[Method A]]"
---

# Project A

(한 문장 프로젝트 설명 — 무엇을 만드는 시스템 / 연구인지.)

- **PI**: [[<나의 이름>]]
- **Methods**: [[Method A]], [[Method B]]
- **Status**: 파일럿 N명 진행 중, 외부 그랜트 X 신청 단계.

## 현재 이슈
- 핵심 컴포넌트의 정확도 X% — 검증 강화 필요.
```

> 💡 **Frontmatter 해부**: 위쪽 `---`로 둘러싸인 영역이 바로 frontmatter. 컴퓨터가 읽는 *라벨*들이라 사람이 본문에 쓰는 자유 텍스트와 분리됩니다.
> - `type: project` — Day 5에서 ontology 스크립트가 *"이 페이지는 프로젝트구나"* 알아차리는 핵심 키. **반드시 있어야 함**.
> - `status: active` / `tier: 2` — Today.md가 자동 수집해서 우선순위 표 만들어줌.
> - `deadline: 2026-08-15` — Today.md § 2가 자동으로 D-counter 계산.
> - `related: [...]` — 관련 페이지 wikilink 리스트. ontology가 `relatedTo` 관계로 변환.

> 💡 **Wikilink 동작**: 본문의 `[[Method A]]` 는 *"Method A라는 페이지로 가는 링크"*. 옵시디언이 자동으로:
> - 클릭 가능한 링크로 렌더
> - 그 페이지가 아직 없어도 stub으로 추적 (Day 5 ontology에서 자동 노드 생성)
> - 그래프 뷰(Ctrl+G)에 엣지로 표시

> 💡 **위키링크 `[[...]]`**: Obsidian 안에서 다른 페이지 링크. 아직 그 페이지가 없어도 괜찮음 — 자동 stub으로 추적됨.

### 단계 1.4 — 같은 방식으로 1-2개 더

본인의 advisee 한 명, 자주 쓰는 메서드 하나, 진행 중인 그랜트 하나 정도 추가하세요. *최소 3-4개의 entity*가 있어야 다음 단계 자동화가 의미 있는 그래프를 만듭니다.

> ✅ **Day 1 체크**: Obsidian 좌측 사이드바의 그래프 뷰 (Ctrl+G) 누르면 본인의 노드들이 작은 별자리로 보여야 합니다.

---

## Day 2 — Today.md (단일 진입점)

**오늘의 목표**: 매일 / 매 세션 시작할 때 무조건 여기부터 읽는 *한 페이지*를 만듭니다. 이게 시스템의 심장입니다.

### 단계 2.1 — `wiki/Today.md` 생성

다음 템플릿을 복사하세요. 섹션은 그대로 두고, 본인 프로젝트로 채우면 됩니다:

```markdown
---
type: meta
title: "Today — 단일 진입점"
---

# Today — 단일 진입점

> **첫 진입은 무조건 이 페이지.** 매 세션 시작할 때 여기를 먼저 읽고 필요한 곳으로 이동하세요.

## 1. 어디서 무엇을 물어볼지

| 묻고 싶은 것 | 어디로 |
|---|---|
| **"내 프로젝트 X의 디자인/이론/방법론"** | `wiki/entities/<X>.md` |
| **"누가 누구의 advisee인지, 내가 PI인 그랜트"** | [[<나의 이름>]] |
| **"방법론 (BKT, MAS 등)"** | `wiki/concepts/` |
| **"오늘 뭐 해야 하지"** | 이 페이지 § 2-3 |

## 2. 활성 마감

| 마감 | 항목 | D- |
|---|---|---|
| YYYY-MM-DD | [[그랜트 이름]] 제출 | D-XX |

## 3. 활성 프로젝트 우선순위

### Tier 1 — 마감/제출 직전
- [[프로젝트 A]] — 한 줄 상황

### Tier 2 — 능동 개발
- [[프로젝트 B]] — 한 줄 상황

### Tier 3 — 백로그
- [[프로젝트 C]]

## 4. 최근 활동 (자동 갱신)
<!-- BEGIN AUTO RECENT -->
(Day 4에 자동 채워짐)
<!-- END AUTO RECENT -->

## 5. 빠른 명령
(Day 4-7에 추가됨)
```

### 단계 2.2 — 본인 데이터로 채우기

§ 2 (마감), § 3 (Tier 1-3 프로젝트) 만 본인 데이터로 채워주세요. 나머지는 자동화가 채울 자리입니다.

### 단계 2.3 — Obsidian 즐겨찾기

Obsidian에서 `Today.md` 우클릭 → "Pin" — 늘 상단 탭에 떠있게.

> ✅ **Day 2 체크**: 매일 아침 Obsidian 열고 가장 먼저 보는 페이지가 `Today.md`가 되어야 합니다. 그 위치만 잡혔으면 성공.

---

## Day 3 — Claude Code 연결 + 첫 세션 자동 기록

**오늘의 목표**: Claude Code가 vault를 *알게* 하고, 세션이 끝날 때마다 자동으로 노트를 남기게 합니다.

### 단계 3.1 — User-level CLAUDE.md

`C:\Users\<you>\CLAUDE.md` 파일을 생성하세요. (vault 안이 아니라 사용자 홈 폴더!) Claude Code는 어떤 폴더에서 켜도 *부모 폴더 위로* 올라가며 `CLAUDE.md`를 자동으로 읽습니다.

```markdown
# User-level Claude Code instructions

## 매 세션 시작 시
1. 먼저 `C:\Users\<you>\ObsidianVault\wiki\Today.md` 를 읽으세요.
2. 자동 메모리(`~\.claude\projects\<machine>\memory\MEMORY.md`)는 시스템이 자동으로 컨텍스트에 주입함.
3. 새로 추론하기보다 기존 vault 콘텐츠를 먼저 인용하세요.

## 지식 위치
| 질문 종류 | 어디서 답을 찾는가 |
|---|---|
| 프로젝트 디자인 / 메서드 / 상태 | `wiki/entities/<프로젝트>.md` |
| 메서드론 / 이론 | `wiki/concepts/` |
| 최근 활동 | `wiki/activity/<날짜>.md` |

## 사용자 스타일
- 한국어 응답 OK (사용자 한국인).
- 짧고 직접적으로. 자기 요약 반복 X.
```

### 단계 3.2 — 세션 자동 기록 hook 등록

> 💡 **Hook이란?** Claude Code에는 *"특정 이벤트가 일어나는 순간"* 사용자가 지정한 명령을 자동 실행하는 시스템이 있습니다. 우리가 쓸 건 **`Stop`** hook — Claude 세션이 끝나는 순간에 발동. 마치 *"세션이 끝나면 자동으로 노트를 남기게 도어벨을 단다"*고 생각하면 됩니다.
>
> Hook이 받는 정보: stdin으로 JSON 형식의 세션 메타데이터(session_id, transcript_path 등) 한 덩어리. 우리 스크립트는 이걸 받아서 `wiki/log.md`에 한 줄 추가합니다.

`~\.claude\settings.json` 열어서 (없으면 생성) 다음 추가:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"C:\\Users\\<you>\\ObsidianVault\\scripts\\save_session.ps1\" -Source claude"
          }
        ]
      }
    ]
  }
}
```

### 단계 3.3 — 간단한 save_session.ps1

vault 안에 `scripts/` 폴더를 만들고 `save_session.ps1`을 다음과 같이 작성:

```powershell
$VaultRoot = 'C:\Users\<you>\ObsidianVault'
$LogFile   = Join-Path $VaultRoot 'wiki\log.md'

# Stop hook이 stdin으로 JSON을 보내옴
$stdin = [Console]::In.ReadToEnd()
$session = if ($stdin) { $stdin | ConvertFrom-Json } else { @{} }
$sid = if ($session.session_id) { $session.session_id.Substring(0, 8) } else { '--------' }

$stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm')
$line  = "- $stamp [claude $sid] session ended"

if (-not (Test-Path $LogFile)) { New-Item $LogFile -ItemType File -Force | Out-Null }
Add-Content -Path $LogFile -Value $line -Encoding UTF8
```

이 단계는 *최소 버전*입니다. 한 줄짜리 로그만 남기지만, hook이 동작하는 걸 확인하는 게 목표.

### 단계 3.4 — 검증

Claude Code 새 세션을 열고 *"내 프로젝트 X에 대해 알려줘"* 같이 본인 vault에 적은 프로젝트 이름으로 물어보세요. CLAUDE.md가 로드되어 답이 vault 콘텐츠 기반이어야 합니다.

세션을 종료하면 `wiki/log.md`에 한 줄이 추가되어야 합니다.

> ✅ **Day 3 체크**: Claude Code가 본인 프로젝트를 *이미 알고* 답하면 성공. 로그 한 줄도 남았다면 hook 동작 확인.

> ⚠️ **흔한 실수**: hook 명령어의 따옴표 escape — Windows에서는 backslash가 두 번이어야 함 `\\`. JSON 파싱 에러 나면 거의 100% 따옴표/슬래시.

> 💡 **🛠 커스터마이징 — Stop 외 다른 hook 이벤트**: Claude Code는 6가지 이상의 hook 이벤트 지원. 활용 예시:
> - **`SessionStart`** — 세션 시작 시 자동 실행. 예: 본인 calendar / Today.md 인쇄 후 *"오늘 우선순위는 X"* 자동 안내.
> - **`PostToolUse` (matcher: `Write|Edit`)** — 파일 수정될 때마다. 예: vault 안 .md가 저장되면 즉시 `update_today.ps1` 트리거 (2시간 기다리지 않고 즉시 반영).
> - **`UserPromptSubmit`** — 본인이 메시지 보내기 직전 트리거. 예: 자동으로 ontology 최신 상태 prompt에 주입.
>
> 본인이 hook 추가/변경하면 `wiki/sources/My Hook Setup.md` 노트로 어떤 이벤트에 어떤 명령을 매핑했는지, 왜 그랬는지 기록 남기세요. 향후 본인이나 협업자가 *"이 자동화는 어디서 트리거되지"* 추적 가능.

---

## Day 4 — 매 2시간 자동 트래커

**오늘의 목표**: 본인이 일하지 않을 때도 시스템이 자동으로 새 노트를 스캔하고 활동 로그를 갱신하게 합니다.

### 단계 4.1 — `daily_tracker.ps1` 작성

vault `scripts/` 안에 작성. 처음엔 *최소 버전*만:

```powershell
$VaultRoot = 'C:\Users\<you>\ObsidianVault'
$ActivityDir = Join-Path $VaultRoot 'wiki\activity'
$today = (Get-Date).ToString('yyyy-MM-dd')
$note  = Join-Path $ActivityDir "$today.md"

if (-not (Test-Path $ActivityDir)) { New-Item -ItemType Directory $ActivityDir -Force | Out-Null }

# 최근 24h 변경된 vault 파일 수집
$lines = @("# Activity $today", "")
$cutoff = (Get-Date).AddHours(-24)
$recent = Get-ChildItem -Path "$VaultRoot\wiki" -Recurse -File -Include *.md |
    Where-Object { $_.LastWriteTime -gt $cutoff } |
    Sort-Object LastWriteTime -Descending | Select-Object -First 30

$lines += "## File activity (last 24h)"
foreach ($f in $recent) {
    $rel = $f.FullName.Replace($VaultRoot, '').Replace('\','/')
    $lines += "- $($f.LastWriteTime.ToString('HH:mm')) ``$rel``"
}

Set-Content -Path $note -Value ($lines -join "`r`n") -Encoding UTF8
Write-Output "Wrote $note"
```

### 단계 4.2 — Windows 예약 작업 등록

PowerShell을 관리자 권한으로 실행 → 다음 명령:

```powershell
schtasks.exe /Create /TN "ResearchAssistantTracker" `
  /SC DAILY /ST 00:00 /RI 120 /DU 23:59 `
  /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\<you>\ObsidianVault\scripts\daily_tracker.ps1" /F
```

이게 *매일 00:00 시작 + 매 120분 반복 + 23:59 동안 지속* 패턴 → **하루 12회** 자동 실행 (00, 02, 04, 06, ..., 22).

> 💡 **🛠 커스터마이징 — 본인 리듬에 맞게**: 위 명령의 두 숫자만 바꾸면 됩니다.
> - **`/RI 120`** = 반복 간격 (분 단위). `60` = 매시간, `240` = 4시간마다, `360` = 6시간마다, `720` = 12시간마다.
> - **`/ST 00:00`** = 시작 시각. `09:00` = 오전 9시 시작 → 09, 11, 13... 식으로 그날 23:59 까지 반복.
> - 일하는 시간대만 (예: 09:00-19:00) 매시간 돌리려면 `/SC DAILY /ST 09:00 /RI 60 /DU 10:00`.
> - 본인이 트래커 주기를 바꾸면 **이 가이드 옆에 메모로 남겨두세요** — `wiki/sources/My Tracker Setup.md` 같은 노트 만들고 frontmatter에 `tracker_schedule: "/RI 60 /ST 09:00 /DU 10:00"` 라고 적으면 미래의 본인이 *"내가 왜 이렇게 했더라"* 잊지 않음.

> 💡 **🛠 커스터마이징 — 트래커 안의 어떤 단계를 끌까**: `daily_tracker.ps1` 끝부분에서 호출되는 각 스크립트 (`build_ontology.py`, `situation_watch.py`, `organize_desktop.py` 등)는 **개별로 주석 처리** 가능. *"나는 LLM 비용 아끼려고 situation_watch만 매일 한 번 돌리고 싶다"* 하면, situation_watch 호출 줄을 별도 스크립트로 빼고 `/SC DAILY /ST 02:00`로 따로 등록 — 여러 스케줄을 섞을 수 있음.

### 단계 4.3 — "컴퓨터 꺼져있을 때 catch up" 옵션

```powershell
$task = Get-ScheduledTask -TaskName ResearchAssistantTracker
$task.Settings.StartWhenAvailable = $true
$task.Settings.DisallowStartIfOnBatteries = $false
Set-ScheduledTask -TaskName ResearchAssistantTracker -Settings $task.Settings
```

이게 켜져 있어야 컴퓨터 꺼졌다 켤 때 *놓친 슬롯을 가능한 빨리 보충*해줍니다.

### 단계 4.4 — 즉시 한 번 실행

```powershell
powershell.exe -File C:\Users\<you>\ObsidianVault\scripts\daily_tracker.ps1
```

`wiki/activity/2026-MM-DD.md` 파일이 생성되어야 합니다.

> ✅ **Day 4 체크**: 다음 짝수 시간 (예: 14:00)에 vault 보면 새 activity 파일이 자동 생성되어 있어야 합니다.

---

## Day 5 — 온톨로지 (vault를 검색 가능한 그래프로)

**오늘의 목표**: 본인의 모든 entity 페이지를 자동으로 읽어서, *"누가 무엇의 PI고, 어떤 메서드를 쓰는가"*를 답할 수 있는 그래프로 만듭니다.

### 5.0 — 온톨로지가 뭐고 왜 필요한가

> "온톨로지"라는 말이 어렵게 들릴 수 있는데, 학술적 정의는 잠시 잊고 **두 가지 표만 기억**하면 됩니다:

**(1) 타입 (Entity Types) — 모든 페이지를 분류하는 카테고리:**

| 타입 | 무엇 | 예시 |
|---|---|---|
| `Person` | 사람 한 명 | 본인, 지도학생, 협업자 |
| `Project` | 진행 중인 프로젝트 | "Project A" 같은 연구 시스템 |
| `Grant` | 외부 자금 / 펀딩 | NSF·AERA·KAERA 같은 그랜트 한 건 |
| `Concept` | 방법론·이론·패턴 | "Bayesian Knowledge Tracing", "ECD" |
| `Course` | 강의 / 워크샵 한 개 | 학기당 가르치는 과목 |
| `Manuscript` | 논문 한 편 | 저널 제출 / 리뷰 중인 원고 |
| `Lab` / `Institution` / `Funder` | 조직 | 본인 연구실, 대학, NSF 같은 자금원 |
| `Tool` | 플랫폼·라이브러리 | Supabase, OpenRouter, Three.js |

**(2) 관계 (Relations) — 타입 사이를 잇는 의미 있는 연결선:**

| 관계 | 의미 | 예시 |
|---|---|---|
| `hasPI` | "X의 PI는 Y" | Project A → hasPI → 나 |
| `advises` | "X는 Y의 advisor" | 나 → advises → 학생1 |
| `usesMethod` | "X 프로젝트가 Y 메서드 사용" | Project A → usesMethod → Method A |
| `fundedBy` | "X 프로젝트가 Y 그랜트로 펀딩" | Project A → fundedBy → Grant X |
| `collaboratesWith` | "X와 Y가 협업 중" | 나 → collaboratesWith → 협업자 |
| `taughtIn` | "X 메서드가 Y 강의에서 다뤄짐" | Method A → taughtIn → Course |
| `relatedTo` | (위 관계에 안 맞는 일반 연결) | 기본 fallback |

> 💡 **온톨로지 = 타입 + 관계.** 그것뿐입니다. 본인이 entity 페이지의 frontmatter (`type:`)와 본문 wikilink (`[[...]]`)를 쓰면 → 스크립트가 자동으로 *어떤 타입의 노드가 어떤 관계로 연결되어 있는지* 추출합니다.

> 💡 **🛠 커스터마이징 — 본인 도메인에 맞는 타입 / 관계 추가**: 위 표는 *기본 셋*. 본인 분야가 다르면 (예: HCI 연구자라면 `Study`/`Participant` 타입, 임상 연구자라면 `Trial`/`Cohort` 타입) `build_ontology.py` 안의 두 군데만 추가:
> - **새 타입**: `ENTITY_FALLBACK_BY_TAG` 딕셔너리에 `"study": "Study"` 추가
> - **새 관계**: `RELATION_RULES` 딕셔너리에 `"recruitedFrom": ([r"recruited from", r"sample drawn from"], {"Study"}, {"Population"})` 같은 줄 추가
> - 변경 후 `wiki/sources/My Ontology Customization.md` 노트로 *"왜 이 타입을 추가했는지"* 한 줄 남기면 향후 본인 + 협업자가 추적 가능.

{{DIAGRAM:schema}}

### 5.0.1 — 어떻게 자동 추출되는가 (스크립트 동작)

`build_ontology.py`가 매 2시간마다 다음을 합니다:

1. **`wiki/**/*.md` 모두 읽기** — frontmatter `type:` 으로 각 페이지가 어떤 타입인지 결정.
2. **본문의 `[[wikilink]]` 모두 추출** — 단순히 *"이 페이지는 저 페이지를 언급한다"*는 사실.
3. **링크 주변 ±100자에서 cue word 매칭** — 예를 들어 본문에 *"Project A is funded by Grant X"* 라고 쓰여 있으면 *"funded by"* 가 `fundedBy` 관계로 변환됨.
4. **타입 도메인 강제** — `hasPI`는 `Project|Grant → Person` 방향이어야 의미 있음. 스크립트가 자동으로 방향 맞춤.
5. **JSON-LD 출력** — 표준 형식으로 그래프를 export. 다른 도구(SPARQL, 시각화 라이브러리)에서도 읽을 수 있음.

> 💡 **JSON-LD?** "JSON for Linked Data" — 평범한 JSON에 **`@context`** (어떤 단어가 어떤 의미인지 사전) + **`@graph`** (실제 노드 목록)를 추가한 W3C 표준. RDF·SPARQL 같은 시맨틱 웹 기술과 호환됩니다. 학위논문에서 인용도 가능.

### 단계 5.1 — `build_ontology.py` 다운로드

이 가이드의 풀 버전 (`Research Assistant System Guide.md`)에 ~600줄 짜리 Python 스크립트가 있습니다. 그걸 `scripts/build_ontology.py`로 복사하세요. 핵심 동작:

1. `wiki/**/*.md` 모두 스캔, frontmatter `type:` 읽기
2. 각 페이지 본문의 `[[wikilink]]` 모두 추출
3. 위키링크 주변 ±100자에서 cue word 매칭 ("PI", "advisee", "uses", "funded by") → 관계 결정
4. 결과: `wiki/_ontology.json` (JSON-LD), `wiki/_ontology_graph.html` (D3 인터랙티브 그래프)

### 단계 5.2 — 직접 실행

```powershell
python C:\Users\<you>\ObsidianVault\scripts\build_ontology.py
```

출력:
```
[ontology] scanning C:\Users\<you>\ObsidianVault\wiki ...
[ontology] 12 nodes, 35 edges (vault pages)
[ontology] FINAL: 12 nodes, 35 edges
[ontology] wrote:
  C:\Users\<you>\ObsidianVault\wiki\_ontology.json
  C:\Users\<you>\ObsidianVault\wiki\_ontology_graph.html
```

### 단계 5.3 — 그래프 보기

`wiki/_ontology_graph.html`을 더블클릭. 브라우저에서 본인의 프로젝트, 사람, 메서드가 *색깔별로* 노드로 보이고 (Person 주황, Project 파랑, Concept 보라 등), 관계 (hasPI, advises, usesMethod...) 가 엣지로 연결됨.

### 단계 5.4 — 트래커에 ontology rebuild 추가

`daily_tracker.ps1` 끝부분에 추가:

```powershell
& python "$VaultRoot\scripts\build_ontology.py"
```

이제 매 2시간마다 본인의 vault 변경사항이 그래프에 반영됩니다.

### 단계 5.5 — 빠른 질의 CLI

`scripts/query_ontology.py` 추가 (가이드 풀 버전 참고). 사용:

```powershell
python scripts\query_ontology.py "Project A"      # 특정 노드 + 모든 관계
python scripts\query_ontology.py --type Grant     # 모든 그랜트
python scripts\query_ontology.py --predicate hasPI  # 모든 PI 관계
```

> ✅ **Day 5 체크**: `python query_ontology.py "<본인 이름>"` 실행하면 본인의 advisees, 본인이 PI인 그랜트, 협업자가 모두 나와야 합니다.

> 💡 **관계 정확도 향상**: entity 페이지 본문에 *"X is the PI of [[프로젝트]]"* 처럼 cue word를 자연스럽게 쓰세요. 다음 ontology rebuild가 더 정확한 관계를 추출합니다.

---

## Day 6 — LLM이 본인 노트를 읽고 변화 감지

**오늘의 목표**: AI가 *"새 노트 / 수정된 노트"*를 읽고 *"마감일이 바뀌었네", "새 협업자가 추가됐네"* 같은 변화를 자동 감지해서 vault에 제안하게 합니다.

### 단계 6.1 — OpenRouter API key

> 💡 **OpenRouter란?** OpenAI / Anthropic / Google 등 여러 LLM 회사의 모델을 *한 개의 API* 로 사용할 수 있게 해주는 프록시 서비스. 모델을 바꾸려면 모델 이름 (예: `google/gemini-2.0-flash-001` → `anthropic/claude-3.5-haiku`) 한 줄만 바꾸면 됩니다. 가격도 각 회사 공식 단가와 동일.
>
> **API key란?** 해당 서비스를 호출할 때 *"내가 누군지"*를 증명하는 비밀 문자열 (예: `sk-or-v1-xxxxx...`). 절대 GitHub 같은 공개 장소에 올리면 안 됨.

[openrouter.ai](https://openrouter.ai) 가입 → $5 충전 → API key 발급 → 저장:

```
C:\Users\<you>\Desktop\_secrets\openrouter.txt   ← 이 파일에 키 한 줄
```

> ⚠️ **`_secrets/` 폴더는 절대 vault 안에 두지 마세요.** vault는 옵시디언이 인덱싱하고 (잠재적으로) 동기화될 수 있는 공간. 키는 **별도 폴더**.

### 단계 6.2 — `situation_watch.py`

가이드 풀 버전의 스크립트를 복사 (~250줄). 핵심 동작:

1. 최근 24h `wiki/sources/`에 추가/수정된 파일 스캔
2. 각 파일의 entity 매칭 + 키워드 ("deadline", "decision", "submitted") 점수화
3. 상위 10개를 OpenRouter (Gemini Flash) 에 보내 구조화 JSON으로 *"무엇이 바뀌었는지"* 받기
4. 결과를 `wiki/situation/<날짜>.md`에 [AUTO] / [REVIEW] 태그로 분류해서 기록

### 단계 6.3 — 트래커에 추가

```powershell
# daily_tracker.ps1 끝부분
& python "$VaultRoot\scripts\situation_watch.py" --hours 24
```

### 단계 6.4 — 첫 실행

```powershell
python C:\Users\<you>\ObsidianVault\scripts\situation_watch.py --hours 168
```

(처음에는 168시간 = 7일 윈도우로 돌려서 충분한 데이터 확보.) `wiki/situation/<오늘날짜>.md` 파일에 다음 같은 결과가:

```markdown
### [AUTO] Project A — deadline_update
- new_value: 2026-09-01
- confidence: 0.92
- reason: Project A README에 새 deadline 명시됨
- evidence: "Final pilot deadline pushed to September 1, 2026"
```

### 단계 6.5 — `apply_situation.py`로 적용

```powershell
python C:\Users\<you>\ObsidianVault\scripts\apply_situation.py
```

이 명령은 [AUTO] 항목 (confidence ≥ 0.85) 만 자동 적용. [REVIEW] 항목은 본인이 직접 검토 후 `--review` 플래그로 적용.

> ✅ **Day 6 체크**: situation note에 *"본인이 알고 있던 변화"*가 자동 감지되어 있어야 합니다. 그러면 시스템이 본인의 vault를 *읽고 이해하고* 있다는 뜻.

> ⚠️ **자동 적용 정책은 보수적**: AI는 deadline / status / progress 같은 *팩트* 변경만 자동 적용. 새 협업자 추가, 메서드 변경 같은 *해석*이 필요한 변경은 [REVIEW]로 남겨서 본인이 결정.

> 💡 **🛠 커스터마이징 — 3가지 다이얼**: `situation_watch.py` 상단의 세 상수가 시스템 *기질*을 결정합니다:
> - **`MODEL = "google/gemini-2.0-flash-001"`** — 비용 ↓ / 품질 적당. 더 정확하게 하려면 `"anthropic/claude-3.5-haiku"` 또는 `"anthropic/claude-3.5-sonnet"` (10×~50× 비용이지만 여전히 한 달 수 달러).
> - **`AUTO_THRESHOLD = 0.85`** — 자동 적용 confidence 하한. `0.95`로 올리면 더 보수적 (의심스러운 건 모두 [REVIEW]), `0.75`로 내리면 공격적.
> - **`IMPORTANCE_KEYWORDS`** 리스트 — 본인 도메인 키워드 추가. 예: 임상 연구자라면 `r"\bIRB approval\b"`, `r"\bDSMB\b"`, `r"\benrollment milestone\b"`. HCI 연구자라면 `r"\bpilot N\b"`, `r"\bThink-aloud\b"`.
>
> 본인이 임계값/모델/키워드를 바꿨으면 `wiki/sources/My LLM Tuning.md`에 *"2026-05-XX 임계값을 0.90→0.80으로 내림. 이유: 마감 변경 missing이 많아서"* 식으로 결정 근거 남기세요. 6개월 후 본인이 *"왜 이래뒀더라"* 잊지 않게.

---

## Day 7 — /slides — 발표자료 자동 생성

**오늘의 목표**: 본인이 *"AI 윤리 강의용 슬라이드 만들어줘"* 한 줄 입력하면, vault 콘텐츠를 끌어와서 단일 HTML 슬라이드덱이 자동 생성되게 합니다.

### 단계 7.1 — open-design 스킬 캐시

```powershell
mkdir C:\Users\<you>\Desktop\_tools\open-design-cache\skills
```

다섯 개 슬라이드 스킬을 GitHub에서 fetch (코드 실행 없음, 마크다운만):

```powershell
# 매거진 스타일 (기본)
gh api "repos/nexu-io/open-design/contents/skills/guizang-ppt/SKILL.md" --jq '.content' | base64 -d > C:\Users\<you>\Desktop\_tools\open-design-cache\skills\magazine-web-ppt\SKILL.md

# 강의용 (warm paper + learning objectives)
gh api "repos/nexu-io/open-design/contents/skills/html-ppt-course-module/SKILL.md" --jq '.content' | base64 -d > C:\Users\<you>\Desktop\_tools\open-design-cache\skills\html-ppt-course-module\SKILL.md

# 시스템 아키텍처 / 메서드론
gh api "repos/nexu-io/open-design/contents/skills/html-ppt-knowledge-arch-blueprint/SKILL.md" --jq '.content' | base64 -d > C:\Users\<you>\Desktop\_tools\open-design-cache\skills\html-ppt-knowledge-arch-blueprint\SKILL.md
```

(나머지 두 스킬도 동일 패턴으로 가져오세요. 각 스킬 디렉토리 안에 `references/`, `assets/template.html`, `example.html`도 fetch — 풀 가이드 참고.)

### 단계 7.2 — `~/.claude/commands/slides.md`

이게 슬래시 커맨드. Claude Code에서 `/slides <주제>`를 입력했을 때 어떻게 동작할지 hardcode 한 markdown 파일:

```markdown
---
description: vault content + open-design skill template으로 HTML slide deck 생성
argument-hint: "<topic> [--skill <skill-name>]"
---

사용자가 `/slides $ARGUMENTS`를 실행함. 다음 순서대로:

1. **스킬 자동 선택**:
   - "강의 / teaching / 워크샵" → html-ppt-course-module
   - "메서드론 / 아키텍처 / framework" → html-ppt-knowledge-arch-blueprint
   - 기타 → magazine-web-ppt (기본)

2. **스킬 파일 읽기**:
   - C:\Users\<you>\Desktop\_tools\open-design-cache\skills\<skill-id>\SKILL.md
   - 같은 폴더의 references/, assets/template.html (또는 example.html)

3. **vault 콘텐츠 끌어오기**:
   - wiki/entities/<topic>.md 직접 읽기
   - wiki/concepts/ 관련 페이지 grep
   - python query_ontology.py "<topic>" 으로 관련 노드 끌기

4. **outline 먼저 제안** — 8-15 슬라이드 구조를 사용자에게 보여주고 OK 받기

5. **단일 self-contained HTML 생성** — CSS/JS inline, fonts CDN, 외부 자산 없음
   출력: Desktop\_PTs\<YYYY-MM-DD>_<topic-slug>\index.html

6. **브라우저로 자동 열기**.
```

### 단계 7.3 — 사용

Claude Code 세션에서 입력:

```
/slides Project A 메서드론
```

Agent가 outline 먼저 제안 → 본인 승인 → 3-5분 안에 HTML 생성 → 브라우저 자동 오픈.

> ✅ **Day 7 체크**: `Desktop\_PTs\<날짜>_<주제-슬러그>\index.html` 파일이 생성되고, 브라우저에서 본인의 vault 콘텐츠가 매거진 스타일로 보여야 합니다.

> 💡 **🛠 커스터마이징 — 새 스킬 / 새 슬래시 커맨드 추가**:
> - **새 슬라이드 스킬**: open-design 레포에 30+ 스킬 있음. 가져오려면 `gh api "repos/nexu-io/open-design/contents/skills/<id>/SKILL.md" --jq '.content' | base64 -d > Desktop\_tools\open-design-cache\skills\<id>\SKILL.md` 후 `~\.claude\commands\slides.md`의 §2 라우팅 표에 한 줄 추가.
> - **새 슬래시 커맨드** (예: `/literature-review`, `/grant-budget`, `/student-feedback`): `~\.claude\commands\<name>.md` 파일 만들고 frontmatter + prompt body 작성 → 즉시 사용 가능. 본인이 자주 하는 작업을 자동화하기 좋음.
> - **본인 스킬 작성** (open-design 외): SKILL.md 형식만 맞추면 자체 템플릿도 가능. `wiki/sources/My Custom Skills.md` 노트에 *어떤 상황에 어떤 스킬을 만들었는지* 기록.

---

## 7일 후 — 일상의 흐름

{{DIAGRAM:weekly-flow}}

**아침** — Obsidian 열고 `Today.md` 봅니다. § 2 마감, § 3 우선순위, § 4 *"지난 밤 무엇이 변했는가"* 한눈에.

**작업 중** — Claude Code 어디서든 켜고 *"X에 대해 어떻게 생각해?"* 식으로 자연스럽게 물어봅니다. CLAUDE.md + 메모리 자동 로드되어 본인 컨텍스트 즉시 잡힘.

**매 2시간 (백그라운드)** — 트래커 자동 실행. 새 노트 스캔, ontology rebuild, situation 변화 감지, Today.md 갱신. 본인은 아무것도 안 해도 됨.

**세션 종료** — Stop hook이 자동으로 세션 디제스트를 `wiki/sources/Sessions <날짜>.md`에 추가. 다음 세션이 그걸 읽고 컨텍스트 이어감.

**주말** — `wiki/situation/<지난 날짜>.md` 파일들 훑어봐서 [REVIEW] 항목 검토. 적용할 거 적용. ontology graph 한 번 열어봐서 본인 portfolio 시각적으로 확인.

---

## 실제 시나리오 — 어떤 상황에서 가장 도움이 되는가

추상적인 "vault + ontology"가 아닌 **연구자/박사과정 일상의 구체 순간**에서 어떻게 작동하는지 5가지:

{{DIAGRAM:scenarios}}

### 시나리오 1 — 디서테이션 챕터 막힘 (박사 4년차)

**상황**: Chapter 3 메서드 작성 중. 6개월 전 advisor와 *"어떤 추정 방법 쓸지"* 결론 내렸던 게 가물가물. 그날 회의 어디 적었더라.

| 없을 때 | 있을 때 |
|---|---|
| Slack DM 검색 + 옛 메모 폴더 + 이메일 검색 → 30-45분 | `python query_ontology.py "Method A"` → 그 메서드 쓰는 모든 프로젝트 + advisor session 디제스트 자동 출력. `Read wiki/sources/Sessions 2025-11-XX.md` 한 번이면 그날 결정 5줄 요약 + 거절했던 대안 method까지. **3분**. |

> 💡 **핵심**: Day 3의 Stop hook이 매 세션마다 디제스트 자동 기록하기 때문. 6개월 전 결정의 근거가 사라지지 않음.

### 시나리오 2 — 그랜트 마감 D-7 패닉

**상황**: 외부 그랜트 마감 일주일 남음. narrative / 예산 / 인용 / current support 9개 docx 일관성 깨졌을지 걱정. 어디부터 보지.

| 없을 때 | 있을 때 |
|---|---|
| 9개 파일 manual diff. *"narrative v5에서 예산 $35K → docx 안 어디는 $30K로 남아있던데"* 같은 미스 발생 | `wiki/entities/<그랜트>.md` frontmatter `deadline:`이 자동 D-7 카운트. situation_watch가 매 2시간 새 파일 변화 LLM-검토 → *"narrative v5에 예산 $35K, current_support v3에 $30K — 불일치 의심 conf 0.91"* 자동 감지해서 Today.md에 표시. **마감 전 검출**. |

> 💡 **핵심**: Day 6 situation_watch가 *"본인이 놓칠 수 있는 변화"*를 미리 잡아냄. 마감 직전 체크리스트가 자동으로 만들어짐.

### 시나리오 3 — 새 advisee 온보딩

**상황**: 박사생 한 명 새로 받음. *"내 연구 portfolio가 뭐고 어떤 메서드 쓰는지"* 한 시간 안에 설명해야 함.

| 없을 때 | 있을 때 |
|---|---|
| PPT 새로 만들기 → 2-3시간. 또는 옛 발표자료 paste. | `/slides 내 연구 portfolio` 한 줄 → 본인 entity 페이지 + ontology graph + 최근 session 디제스트 자동 통합 → 매거진 스타일 단일 HTML. 옆에 `wiki/_ontology_graph.html` 도 같이 띄우면 *"이게 내 모든 프로젝트와 메서드의 관계도"*. **5분**. |

> 💡 **핵심**: Day 7의 `/slides` + Day 5의 ontology graph가 *"내 portfolio 한눈 시각화"*를 자동으로 만들어둠. 새 사람 만날 때마다 다시 만들 필요 X.

### 시나리오 4 — Reviewer 2 ("왜 X 메서드 안 썼는지 설명하라")

**상황**: 저널 R&R 받음. Reviewer 2의 *"why didn't you use X-method"* 질문 — 6개월 전에 검토했다가 거절한 method인데 거절 이유가 가물.

| 없을 때 | 있을 때 |
|---|---|
| 옛 미팅 노트 다시 읽기 / 메일 검색 / 본인 기억으로 답변 짜내기 → 답변 모호 | `grep "X-method" wiki/sources/Sessions*.md` → 6개월 전 그 method 검토했던 세션 발견 → key_decisions에 *"computational cost prohibitive at N=2000, switched to method A"* 라고 본인이 그때 기록. 답변이 명확하고 짧음. **2분**. |

> 💡 **핵심**: Day 3 session digest의 `key_decisions` 필드가 *결정의 근거*를 매 세션 자동 추출. 거절된 옵션이 사라지지 않음 → 미래의 본인이 변호 가능.

### 시나리오 5 — Comp exam / Quals 준비

**상황**: 종합시험 한 달 전. 6개월 동안 읽은 논문 80편 + 그 사이 등장한 메서드/이론 정리 필요. 인용 네트워크 그려야 할 것 같은데 어디서 시작.

| 없을 때 | 있을 때 |
|---|---|
| EndNote/Zotero에 메타만 있고, 메서드 사이 관계는 머릿속 → 빠진 게 많음 | Day 1부터 각 논문을 `wiki/sources/<paper>.md`로 짧게 정리 (frontmatter `type: source` + `cites: [[Method A]]` + `extends: [[Theory B]]`) → Day 5 ontology가 자동으로 *"어떤 메서드가 어떤 이론을 cites 하는가"* 그래프. `python query_ontology.py --predicate cites` 로 인용 네트워크. `--predicate extends` 로 이론 발전 계보. 시각화는 `_ontology_graph.html`. |

> 💡 **핵심**: 가이드를 6개월 일찍 시작했다는 가정. 매일 논문 한두 편을 읽으며 vault에 1-2분만 넣으면 → 시험 준비 시점에 인용 그래프가 *이미* 만들어져있음. 마감 직전 작업 0.

---

> 💡 **공통 패턴**: 위 5가지 시나리오 모두 *"평소 작업할 때 vault에 흔적을 남겨두면 → 필요할 때 컴퓨터가 자동으로 답을 찾아온다"*는 구조. 시스템은 본인의 작업을 *추가로 부담시키지 않고* — 오히려 평소 노트 작성 + Stop hook 자동 기록만으로 — 미래의 본인에게 자료를 쌓아주는 인프라입니다.

---

## 자주 막히는 곳 (트러블슈팅)

| 증상 | 원인 | 해결 |
|---|---|---|
| Stop hook이 안 걸림 | settings.json 경로 escape 문제 | `\\` 두 번 들어갔는지 확인. PowerShell 명령은 큰따옴표 escape `\"` |
| 트래커가 매 2시간 안 도는 거 같음 | 컴퓨터가 절전모드, 또는 StartWhenAvailable 미설정 | `schtasks /Query /TN ResearchAssistantTracker /V /FO LIST | Select-String "Last\|Next"` 로 마지막 실행 시각 확인 |
| ontology에 노드 0개 | frontmatter `type:` 누락 | 각 entity 페이지 첫 줄 `---` 안에 `type: project` 같이 명시 |
| `query_ontology.py "X"` 결과 없음 | label 대소문자 불일치 | `--type Project` 으로 전체 리스트 보고 정확한 레이블 확인 |
| situation_watch가 (LLM error) | OpenRouter key 없음/만료 | `_secrets/openrouter.txt` 확인, `curl -H "Authorization: Bearer <key>" https://openrouter.ai/api/v1/models` 로 테스트 |
| /slides가 빈 슬라이드만 생성 | vault에 해당 entity 없음 | 먼저 `wiki/entities/<주제>.md` 손으로 작성하고 retry |

> 💡 **거의 모든 막힘은 frontmatter / 경로 escape 문제입니다.** 5분 안에 해결 안 되면 frontmatter 확인 + 경로 backslash 확인부터 하세요.

---

## 다음 단계

7일 가이드를 끝냈으면, 본인은 이미 작동하는 연구보조 시스템을 갖고 있습니다. 더 깊이 가고 싶다면:

- **풀 가이드** ([[Research Assistant System Guide]]) — 14개 컴포넌트 모두 자세한 설명, 디자인 결정 트레이드오프, customization 가이드, 200줄 도식.
- **온톨로지 v0.2 (이벤트-허브)** — Session/Deck도 노드로 격상하면 *"지난 학기 프로젝트 X에 대해 만든 모든 작업물 보여줘"* 식 시간-기반 질의 가능.
- **Codex 통합** — Codex CLI 쓰면 `pwsh codex_digest.ps1` 추가해서 동일한 세션 디제스트 파이프라인 적용.
- **Desktop 자동 정리** — `organize_desktop.py` 추가해서 데스크탑 loose 파일도 LLM이 알아서 분류.

---

## 모든 커스터마이징은 노트로 기록 (권장 패턴)

이 가이드의 모든 숫자·임계값·키워드는 **본인 입맛대로 바꿀 수 있게 설계**되어 있습니다 (트래커 주기, LLM 모델, 자동 적용 confidence, ontology 타입, 슬래시 커맨드, hook 이벤트 등). 다만 시스템이 점점 복잡해지면 *"3개월 전에 내가 왜 이걸 0.85에서 0.80으로 내렸지"* 잊습니다. 그래서:

> 💡 **권장 패턴**: 본인이 어떤 부분을 바꿀 때마다 **vault 안 별도 노트**로 결정 근거 남기기.
>
> ```
> wiki/sources/
> ├── My Tracker Setup.md        ← 트래커 주기 / 시작 시각 / 활성 단계
> ├── My LLM Tuning.md            ← 모델 선택 / threshold / keywords
> ├── My Ontology Customization.md ← 추가 type/relation
> ├── My Hook Setup.md            ← Stop 외 hook 매핑
> └── My Custom Skills.md         ← 새 슬래시 커맨드 / 슬라이드 스킬
> ```
>
> 각 노트의 frontmatter에 `type: source` + `tags: [tuning, customization]` + 결정 timestamp를 남기면 — ontology가 자동으로 *"내 시스템이 어떻게 진화해왔는가"* 그래프로 만들어줍니다 (Day 5의 ontology가 이런 메타-노트도 노드로 잡음).

이 패턴은 *시스템 자체가 본인의 결정 이력을 기록하는* 자기-참조 구조를 만들어줍니다. 6개월·1년 후 본인이 *"왜 이렇게 셋업했더라"* 가 `python query_ontology.py "tuning"` 한 줄로 답이 나옵니다.

---

## 핵심 원칙 (외워두면 좋음)

1. **단일 진입점이 검색을 없앤다** — 매일 30분씩 잃는 *"어디 적었더라"* 대신 `Today.md` 한 페이지.
2. **메모리는 prompt engineering보다 강하다** — 매번 재설명할 필요 없게 `~/.claude/projects/<machine>/memory/`에 영구 저장.
3. **온톨로지는 평면 태그를 이긴다** — *"내가 PI인 모든 그랜트"* 식 질문은 그래프 한 줄로.
4. **LLM은 가장자리에서만** — orchestrator는 평범한 Python/PowerShell. AI는 결정 포인트에서만 (situation 판단, 파일 분류, 슬라이드 생성).
5. **자동 적용은 보수적으로** — 모든 LLM 제안에 confidence + [REVIEW] 옵션. *해석*이 필요한 변경은 절대 자동 적용 안 함.
6. **모든 행동은 되돌릴 수 있어야 한다** — 데스크탑 이동은 undo, frontmatter 변경은 audit log, ontology는 매번 재생성.
