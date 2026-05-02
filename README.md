# Research Assistant AI Workflow

> Obsidian × Claude Code 기반 박사·연구자용 AI 보조 시스템 7-day 셋업 가이드.

🌐 **Live**: <https://educatian.github.io/research-assistant-ai-workflow-ko/>

---

## 무엇

Obsidian 노트 vault + Claude Code (또는 Codex) 를 결합해, 박사과정·신진교수·연구원이 자기 프로젝트 portfolio (논문·메서드·학생·그랜트)를 자동으로 indexing·querying·visualize할 수 있는 시스템의 셋업 가이드.

- **하루 1-2시간씩 7일** 따라가면 본인 vault에 작동하는 시스템이 셋업됨
- **월 비용 ~$1-2** (LLM API 사용량)
- **로컬 우선**: 모든 데이터가 본인 컴퓨터에. 외부 LLM은 결정 포인트에서만 호출
- **BYOK**: OpenRouter API 키로 어떤 모델이든 swap 가능 (Gemini Flash 기본, Claude Sonnet 등)

## 가이드 구성

| | 내용 |
|---|---|
| **§ 0** | 용어 사전 — Vault / Entity / Frontmatter / Wikilink / Hook / Ontology / API key |
| **§ 0.5** | AI agents — Claude Code vs Codex 역할 분담, CLI vs Desktop 차이 |
| **§ 1-3** | 핵심 개념 (3층 구조) · 자동화 흐름 · 시작 전 체크리스트 |
| **Day 1** | Vault 만들기 + 첫 entity 페이지 |
| **Day 2** | `Today.md` 단일 진입점 |
| **Day 3** | Claude Code 연결 + Stop hook 자동 기록 |
| **Day 4** | 매 2시간 자동 트래커 (Windows Task Scheduler) |
| **Day 5** | 온톨로지 — vault를 검색 가능한 그래프로 |
| **Day 6** | LLM이 노트 변화 자동 감지 (situation watch) |
| **Day 7** | `/slides` 발표자료 자동 생성 |
| **이후** | 일상 흐름 · 5가지 시나리오 · 트러블슈팅 · 커스터마이징 노트 패턴 |

## 산출물 미리보기

가이드 HTML은 단일 파일 (132KB)에 다음을 포함:

- 🎨 **8 인라인 SVG 다이어그램** — 3층 mental model · 트래커 흐름 · 7-day timeline · 온톨로지 schema · agents 비교 · 5 시나리오 등
- 📚 **40+ 콜아웃** — 💡 TIP / ⚠ WATCH OUT / ✓ CHECK / 🛠 커스터마이징
- 🎯 **Sticky TOC** — 스크롤시 활성 섹션 자동 하이라이트 (○ → ●)
- ⌨ **키보드 단축키** — `F` 좁은 컬럼 · `D` 다크모드
- 🌏 **bilingual ko/en** — 한글 본문 + 영문 기술 용어
- 🖋 **Pretendard + Hahmlet** — 한글 모던 폰트 + 영문 serif

## 직접 빌드하려면

```bash
pip install markdown
python render.py
# → index.html 생성
```

`guide.md`를 수정하고 위 명령 다시 돌리면 HTML이 갱신됨.

커스텀 경로:
```bash
python render.py path/to/source.md path/to/output.html
```

## 사용 기술

- [Obsidian](https://obsidian.md) — vault UI (무료)
- [Claude Code](https://claude.com/claude-code) — Anthropic AI agent
- [Codex CLI](https://github.com/openai/codex) — OpenAI 보조 agent (선택)
- [OpenRouter](https://openrouter.ai) — LLM 프록시 (BYOK)
- [open-design](https://github.com/nexu-io/open-design) — 슬라이드덱 스킬 템플릿
- Python 3.11+ / PowerShell / Markdown

## 작성자

**문제웅** · The University of Alabama · [jmoon19@ua.edu](mailto:jmoon19@ua.edu)

질문·피드백 환영. PR 환영.

## 라이선스

- **콘텐츠** (`guide.md`, `index.html`): [CC BY-SA 4.0](LICENSE-content) — 출처 표시 + 동일 조건 변경 허락 시 자유 사용
- **코드** (`render.py`): [MIT](LICENSE-code) — 자유 사용

## 기여

이슈·PR 환영. 본인 도메인의 시나리오 / 새 ontology 타입 / 슬라이드 스킬 등 추가 환영.
