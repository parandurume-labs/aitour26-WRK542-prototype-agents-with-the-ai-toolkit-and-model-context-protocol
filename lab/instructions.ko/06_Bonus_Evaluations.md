# Bonus: 에이전트 응답을 수동으로 평가하기

> [!NOTE]
> 이 섹션은 보너스(선택) 섹션입니다. 실습 시간에 여유가 있다면 진행하세요. 시간이 부족하다면, 실습 후 개인 속도에 맞춰 진행해도 됩니다.

이 섹션에서는 에이전트 응답 데이터셋을 **수동 평가(manual evaluation)** 하는 방법을 학습합니다. 수동 평가는 사람이 LLM 출력의 품질을 직접 판단하는 방식입니다. 실무에서는 생성된 응답을 읽고, 루브릭(평가 기준)이나 간단한 스케일을 기준으로 정확성/관련성/명확성/유용성 등을 판단합니다. Agent Builder를 사용하면 수동 평가를 통해 에이전트 성능을 점검할 수 있습니다.

## Step 1: 에이전트 Instructions에 변수 추가

Agent Builder의 Evaluation 기능을 사용하려면 에이전트의 **Instructions**에 변수가 포함되어 있어야 합니다. 변수는 에이전트 Instructions 또는 사용자 프롬프트의 컨텍스트를 바꿀 수 있는 값이지만, 에이전트의 목적과는 여전히 관련이 있어야 합니다. 변수는 중괄호 두 겹으로 감쌉니다(예: `{{variable}}`).

Cora 에이전트의 목적은 매장 운영과 본사 리포팅을 지원하는 것이므로, 운영 컨텍스트를 바꾸는 변수가 가장 자연스럽습니다. 이 예에서는 **store**를 변수로 사용합니다. **Instructions**를 아래처럼 수정합니다.

```
You are Cora, an internal assistant for Zava. You help store managers and head office staff analyze sales and manage inventory, tailored to the needs of the {{store}} location.​

Your role is to:​

- Ask clarifying questions and be brief in your responses.​

- Use Zava’s tools (sales + inventory) to answer questions with facts when possible.​

- Summarize sales performance, answer inventory questions, and recommend next actions for the {{store}} location.​
​
Your personality is:​

- Professional, precise, and helpful​

- Curious and practical—never assume, always clarify​
```

> [!NOTE]
> Model이 여전히 **gpt-5.3-chat (via Microsoft Foundry)**로 설정되어 있는지 확인하세요.

모든 변수는 Agent Builder의 **Variables** 섹션에 저장됩니다. 아래 스크린샷에 보이는 오류 메시지는 무시해도 됩니다. Evaluation 탭을 통해 변수 값을 전달할 것입니다.

![Agent variables.](../../img/agent-variables.png)

이 기능은 어떻게 동작할까요? 예를 들어 `{{store}}`에 `Seattle`을 사용한다고 가정해 보겠습니다. `{{store}}` 값으로 `Seattle`을 정의해두면, 사용자 프롬프트를 실행할 때 **Instructions**가 동적으로 수정되어 `{{store}}` 변수가 `Seattle`로 치환됩니다. 즉, 에이전트 지시문은 다음과 같이 읽히게 됩니다.

"You are Cora, an internal assistant for Zava. You help store managers and head office staff analyze sales and manage inventory, tailored to the needs of the Seattle location.​"

그럼 이제 몇 줄의 평가 데이터를 실행해 보겠습니다.

## Step 2: 데이터 추가

Agent Builder에서 **Evaluation** 탭으로 전환합니다. 평가 실행에는 **User Query**와 **{{variable}}** 모두에 값이 필요합니다. **User Query**는 사용자가 에이전트에 제출하는 프롬프트(예: 지난달 내 상위 카테고리는?)이고, **{{variable}}**는 변수의 값(예: `{{store}}`)입니다.

> [!NOTE]
> **+ Add an Empty Row**를 클릭한 뒤에야 테이블 헤더에 {{store}} 변수가 표시될 수 있습니다.
>

![Evaluation table.](../../img/evaluation-table.png)

이제 평가 데이터를 추가하는 방식에 대해 몇 가지 옵션이 있습니다.

> [!TIP]
> **Evaluation** 섹션을 전체 화면으로 확장하려면 휴지통 아이콘 옆의 **Expand to Full Screen** 아이콘을 클릭합니다.

**수동 입력(Manually Add Data)**

**Evaluation** 탭에서 빈 행을 만들고, **User Query** 및 **{{store}}** 셀에 입력해 수동으로 데이터를 추가할 수 있습니다. 아래는 **User Query**와 **{{store}}** 조합 예시입니다.

|   User Query        | {{store}}
--------------|-------------
What were the top 3 categories by revenue last month? | Seattle
Which products are at risk of stockout this week? | Redmond
Summarize online vs physical sales performance last month. | Head Office
Do we have enough circuit breakers for this weekend’s promotion? | Bellevue

> [!TIP]
> **Add an Empty Row** 버튼으로 각 행을 만든 뒤 셀을 더블 클릭해 내용을 편집할 수 있습니다.

**데이터 생성(Generate Data)**

데이터 생성에 도움이 필요하면 **Generate Data** 기능으로 최대 10행의 합성 데이터(synthetic data)를 생성할 수 있습니다. 합성 데이터는 실제 사용자나 이벤트에서 수집된 것이 아니라, 현실 데이터를 모방해 인공적으로 생성한 데이터입니다. 이 기능은 **Generation Logic**을 입력으로 받아 **User Query**와 **{{store}}** 쌍을 생성합니다. **Generate Data** 기능은 에이전트 **Instructions**를 기반으로 Generation Logic을 자동 생성하지만, 원하는 대로 수정할 수도 있습니다.

![Generate data.](../../img/generate-data.png)

**Rows of Data to Generate**에 생성할 행 수를 입력한 뒤, Generation Logic을 수정하고 **Generate**를 선택해 데이터셋을 생성합니다. 생성된 데이터셋이 평가 테이블에 표시됩니다.

**데이터셋 가져오기(Import a Dataset)**

**User Query**와 **{{store}}** 쌍으로 구성된 대량 데이터셋을 이미 갖고 있다면, Agent Builder로 가져와 평가할 수 있습니다. Agent Builder는 아래 형식으로 구성된 `.csv` 파일을 지원합니다.

|   User Query        | {{store}}
--------------|-------------
What were the top 3 categories by revenue last month? | Seattle
Which products are at risk of stockout this week? | Redmond
Summarize online vs physical sales performance last month. | Head Office
Do we have enough circuit breakers for this weekend’s promotion? | Bellevue

여기서 **User Query**와 **{{store}}**는 헤더입니다. **Import** 아이콘(선 위의 위쪽 화살표)을 사용하면 Agent Builder로 가져올 데이터셋 파일을 선택할 수 있습니다.

![Import dataset.](../../img/import-dataset.png)

각 옵션을 한 번씩 실험해 보세요. 이후 안내는 첫 번째 옵션인 **Manually Add Data**를 기준으로 계속 진행합니다.

## Step 3: 에이전트 출력 평가

데이터셋이 준비되면, 행을 하나씩 실행하거나 여러 행을 선택해 함께 실행할 수 있습니다. 모든 행을 선택하려면 헤더 행의 체크박스를 선택합니다. 선택한 행을 실행하려면 **Run Response** 아이콘(재생 버튼)을 선택합니다.

![Run button.](../../img/run-eval.png)

모델은 각 **User Query**와 **{{store}}** 쌍에 대해 응답을 생성합니다. 응답이 생성되면 출력을 검토하고 **Manual** 열에서 **thumbs up** 또는 **thumbs down** 아이콘을 선택합니다.

![Manual evaluation.](../../img/manual-evaluation.png)

thumbs up/down은 어떻게 판단할까요? 출력이 기대를 충족했는지를 기준으로 판단합니다. **thumbs up**은 응답이 정확하고 관련성이 있으며 명확하고 실질적으로 도움이 되었다는 뜻입니다(원하는 정보나 결과를 제공함). **thumbs down**은 응답이 틀렸거나 불완전하거나 혼란스럽거나 주제에서 벗어나거나 작업에 도움이 되지 않는 등 어떤 면에서든 부족했다는 뜻입니다.

요약하면 다음을 자문해 보세요. **“이 출력이 내가 필요로 했던 일을 해줬는가?”** 그렇다면 thumbs up, 그렇지 않다면 thumbs down을 선택합니다.

## Key Takeaways

- {{store}} 같은 변수를 Instructions에 추가하면, 에이전트의 핵심 목적을 유지한 채 서로 다른 운영 컨텍스트에 대해 체계적으로 테스트할 수 있습니다.
- Agent Builder는 수동 입력, 합성 데이터 생성, CSV 가져오기를 지원하므로, 테스트 목적에 맞는 평가 데이터셋을 유연하게 만들 수 있습니다.
- thumbs up/down 기반의 사람 판단은 자동화된 지표로는 포착하기 어려운 정확성/관련성/유용성 등을 평가하는 데 도움이 됩니다.
