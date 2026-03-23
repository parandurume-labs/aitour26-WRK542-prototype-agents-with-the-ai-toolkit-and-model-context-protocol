# エージェント構築: Agent Builder で Zava 店舗運営エージェントを作る

このセクションでは、AI Toolkit の Agent Builder を使って Cora エージェントを作成し、ツールを追加してユーザーの代わりにアクションを実行できるようにします。Agent Builder は、プロンプトエンジニアリングや MCP サーバーなどのツール連携を含む、エージェント構築のエンジニアリング ワークフローを効率化します。

## Step 1: Agent Builder を確認する

Agent Builder にアクセスするには、AI Toolkit のビューで **Developer Tools** 配下の **Build** セクションを見つけます。展開して **Create Agent** をクリックします。次に **Open Agent Builder** を選び、Visual Studio Code 内の新しいタブで Agent Builder UI を開きます。

![Create New Agent](../../img/create-new-agent.png)

Agent Builder の UI は大きく 2 つの領域に分かれています。左側では、エージェント名、モデル選択、指示（instructions）、利用するツールなど、エージェントの基本情報を定義します。右側は、エージェントとのチャットおよび応答の評価を行う領域です。

![Agent Builder](../../img/agent-builder.png)

> [!NOTE]
> 評価（Evaluation）機能は、エージェントの Instructions 内で変数（variable）を定義した後に利用できます。評価は、このラボの Bonus セクションで詳しく扱います。

## Step 2: エージェントを作成する

Zava の Cora エージェントを作成しましょう。**Agent name** フィールドに **Cora** と入力します。**Model** は **gpt-5.3-chat (via Microsoft Foundry)** のモデル インスタンスを選択します。

## Step 3: エージェントの指示（Instructions）を用意する

Model Playground で行ったのと同様に、ここでもシステムプロンプト（system prompt）としてエージェントの振る舞いを定義します。

> [!TIP]
> Agent Builder には、エージェントのタスク説明から LLM に Instructions を生成させる **Generate** 機能があります。
> また、出発点として使えるサンプル Instructions を提示する **Inspire me** 機能もあります。
> どちらも、指示文の作成に迷ったときに役立ちます。

![Generate Agent Instruction](../../img/generate-agent-instruction.png)

このラボでは、[前のセクション](./03_Model_Augmentation.md) で使ったものに近い Instructions を使用します。

```
# **Zava Sales & Inventory Agent – System Instructions**

## **1. 役割とコンテキスト**
あなたは **Cora** です。**Zava**（DIY 小売企業）の社内アシスタントとして、店長と本部スタッフの販売分析と在庫管理を支援します。
* **トーン:** プロフェッショナルで、正確で、親切。
* **会計年度（FY）:** **7 月 1 日**に開始。
  * Q1: 7–9 月 | Q2: 10–12 月 | Q3: 1–3 月 | Q4: 4–6 月。
* **日付の扱い:** DB クエリのために、相対日付（例: "先月"、"Q1"）は常に ISO 形式（YYYY-MM-DD）に変換する。

---

## **2. ツール利用戦略（"ルーター"）**
ユーザー意図を解析し、正しいツール ワークフローを選択しなければならない:

### **A. 商品探索（定性）**
* **トリガー:** ユーザーが特徴、説明、用途、曖昧な商品名（例: "防水ライト"、"コンクリ用ドリル"）を尋ねる。
* **アクション:** 最初に **必ず** `semantic_search_products` を使う。
* **制約:** 商品説明や名称の検索に SQL を **絶対に** 使わない。

### **B. 売上・データ分析（定量）**
* **トリガー:** ユーザーが売上高、販売数量、上位店舗、集計メトリクスを尋ねる。
* **アクション:** `execute_sales_query` を使う。
* **要件:** 時間に依存するクエリ（例: "先月の売上"）では、正しい日付範囲を計算するために **必ず最初に** `get_current_utc_date` を呼ぶ。

### **C. 在庫とアクション（読み取り／書き込み）**
* **トリガー:** ユーザーが在庫数や在庫移動を尋ねる。
* **ワークフロー:**
  1. **特定:** 商品 id が不明なら、`semantic_search_products` で商品 id を取得する。
  2. **確認:** `get_stock_level_by_product_id` を使って在庫可用性を確認し、内部の `store_id` を取得する。
  3. **確認（重要）:** ユーザーが移動を要求した場合は、必ず **停止** して確認を取る: *"確認してください: [数量] 個の [商品名] を [店舗 A] から [店舗 B] へ移動しますか？"*
  4. **実行:** 確認後にのみ `transfer_stock` を呼ぶ。

---

## **3. 範囲と安全性**
* **書き込み保護:** 現在の会話ターンでユーザーの明示的な確認がない限り、`transfer_stock` を実行してはならない。
* **ID の秘匿:** Entity ID（例: `store_id: 4`, `product_id: 99`）はツール実行のために内部で扱うが、最終回答では **絶対に表示しない**。店舗名と商品名を使う。
* **幻覚を禁止:** ツールがデータを返さない場合は "I couldn't find any data matching that request." と言い、数字や商品を捏造しない。
* **範囲外:**
  > "I'm here to assist with Zava sales, inventory, and product data. For other topics, please contact IT support."

---

## **4. 応答ガイドライン**
* **フォーマット:** 商品や売上データの一覧は Markdown テーブルを使う。
* **0 件の場合:**
  * *Semantic Search:* 該当商品がない場合は明確に "I couldn't find any products matching that description." と言う。
  * *Sales Data:* SQL 結果が空の場合は "No sales records found for that specific criteria." と言う。
* **言語:** 応答はユーザーの言語に翻訳する。
* **確認:** 不明確なら決めつけず、確認質問をする。

---

## **5. 推奨質問（最大 10 個まで提示）**
* 先月の売れ筋カテゴリは何でしたか（オンライン vs 店舗）？
* 2024 年 Q2 の総売上高はいくらでしたか？
* 現在、どの店舗でブレーカーの在庫が少ないですか？
* "Pro-Series Hammer Drill" の在庫を全店舗で確認して
* 今月、全米店舗の売上高上位 10 商品は？
* "Pro-Series Hammer Drill" をある店舗から別店舗に 5 個移動して
* 先月のオンライン売上をカテゴリ別に一覧化して
* 先月と比べて返品率が異常に高い店舗は？

---

## **6. 実装メモ**
* **手順順序:** 時刻確認 → 検索／クエリ → 整形。
* **上限:** すべての SQL クエリと検索は、可読性のため既定で `LIMIT 20` にする。
* **曖昧さの扱い:** `semantic_search_products` の類似度が低い結果を返した場合は、一覧の前に *"Here are the most likely product candidates I found for your search."* と前置きする。
```

店舗運営タスク（販売分析、在庫確認、安全な在庫移動）のための明示的なガイダンスを追加している点に注目してください。
ただし、この時点では Cora はまだ販売／在庫データにアクセスできません。次のステップで設定します。

## Step 4: MCP サーバーを起動する

> [!NOTE]
 > [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) は、大規模言語モデル（LLM）と外部ツール／アプリ／データソース間の通信を最適化するための、強力で標準化されたフレームワークです。

前の **Model Augmentation** では、ファイル添付という形でグラウンディング データを追加しました。これは簡単なテストには便利ですが、店舗運営では時間とともに変化するライブ データ（売上・在庫）が必要です。

そこで、Cora をこのワークショップ用に構成された 2 つの MCP サーバーに接続します。

- **Sales Analysis MCP server**（売上メトリクス＋商品セマンティック検索）
- **Inventory MCP server**（在庫レベル＋安全な在庫移動）

サーバーを起動するには、Visual Studio Code で **<kbd>CTRL+F5</kbd>** を押して MCP Servers を起動し、両方のサーバーが初期化されるまで待ちます。サーバーごとに 1 つずつ、合計 2 つの新しいターミナル ウィンドウが開きます。
両方のターミナルで `Uvicorn is running on port XXXX` というメッセージが表示され、サーバーが稼働していることを確認してください。

![MCP Servers running](../../img/mcp_servers_running.png)

> [!TIP]
> UI から起動することもできます。'Run'->'Run without debugging' をクリックしてください。
> ![Run and debug](../../img/run-and-debug.png)

> [!WARNING]
> 初回起動で importlib エラーによりサーバー起動に失敗した場合は、もう一度実行してください。これは Python のバイトコード コンパイルと Windows のファイル システム操作のタイミング問題として知られています。再実行すれば、必要ファイルがキャッシュされているため 2 回目は成功します。

## Step 5: Sales MCP サーバーのツールをエージェントに追加する

このラボでは、両方のサーバーから小さく焦点を絞ったツールセットをエージェントに付与します（商品検索、在庫確認、売上クエリ実行、確認付きの在庫移動ができるだけの最小構成）。

Agent Builder に戻り、**Tools** の横の **+** アイコンを選択して、ツール追加ウィザードを開きます。

![Add tool.](../../img/add-tool.png)

**Configured** タブで下にスクロールし、**Local Tools** セクションから **zava-sales-analysis-server** を選択します。

![Select Sales Analysis Server](../../img/select-sales-analysis-server.png)

これで、エージェントの **Tool** セクションにサーバーが表示されます。

> [!NOTE]
> Sales Analysis MCP サーバーのツールを追加する前に、サーバーが起動していることを確認してください。

## Step 6: エージェントで売上クエリをテストする

Cora が店舗運営向けのツール呼び出しを実行できるかテストします。**Agent Builder** タブ右側のチャット ペインで、次のパスにあるブレーカー画像を添付します。

```
C:\Users\LabUser\aitour26-WRK542-prototype-agents-with-the-ai-toolkit-and-model-context-protocol\src\instructions
```

次のテキスト プロンプトを送信します。

```
店長です。写真に写っているものを特定してから、カタログ内で最も近いブレーカー商品を見つけ、全店舗の現在在庫を表示してください。
```

![Agent Builder Playground](../../img/agent-builder-playground.png)

エージェントがツール呼び出しを実行すると、出力内に「どのツールを呼んだか」を示すセクションが表示されます。

![Tool call in the agent's output.](../../img/tool-call.png)

言語モデルは非決定的（non-deterministic）なので、出力は毎回異なる可能性があります。以下は応答例です。

> This appears to be a circuit breaker.
>
> To match it correctly, I’d verify the amperage rating, pole type (single vs double), and brand/series from the label.
>
> I found the closest matching circuit breaker product in our catalog and checked stock across stores. Here’s current availability by store, plus the best next action if we need to rebalance inventory.

想定どおりにツールが使われない場合は、**Instructions** を更新して「どのタスクでどのツールを使うか」をより明示するのが有効です。

次に、以下の質問も試してください。

```text
前四半期の店舗別売上は？
```

```
昨年の売上上位 3 商品は？
```

### Step 7: Inventory MCP サーバーのツールをエージェントに追加する

続いて、在庫ツールを追加し、在庫確認と安全な在庫移動ができるようにします。
手順は、Sales ツールの設定と同様です。

1. Agent Builder で **Tools** の横の **+** アイコンをクリックします。
2. **Configured** タブの **Local Tools** セクションで **zava-inventory-server** を選択します。
3. Sales サーバーと並んで Inventory サーバーが **Tool** セクションに表示されます。

> [!NOTE]
> Inventory MCP サーバーのツールを追加する前に、サーバーが起動していることを確認してください。

## Step 8: 在庫確認と在庫移動をテストする

在庫移動のテストとして、次のような依頼を送ってみます。

```
在庫に余裕のある店舗からオンライン ストアへ、Single Pole Circuit Breaker 20A を 5 個移動してください。
```

エージェントは、移動ツールを実行する前に確認を求めるはずです。移動元／移動先の店舗が正しいことを確認できた場合のみ、承認してください。完了後、在庫レベルを再度確認し、移動が反映されているか検証します。

さらに試す場合は、次のプロンプトも送信してみてください。

```
先月の総売上高を、オンライン vs 実店舗で分けて教えてください。
```

```
現在、どの店舗でブレーカーの在庫が少ないですか？
```

## エージェントをローカルに保存する

テストが終わったら、Agent Builder 右上の **Save to Local** ボタンをクリックし、エージェント構成をローカルに保存してください。保存しておくと、次回以降ゼロから作り直さずに同じ構成を読み込んで利用できます。

Instructions やツールを調整しながら、複数バージョンを保存して比較することもできます。

ローカル エージェントはいつでも、AI Toolkit ビューの **My Resources**->**Local Resources**->**Agents** ->**Local** から参照できます。

## まとめ（Key Takeaways）

- AI Toolkit の Agent Builder は、構成とテスト／評価を分離した 2 ペイン UI を提供する
- 具体的な Instructions により、エージェントの人格、会話スタイル、応答パターンを一貫させられる
- MCP サーバーは、静的なファイル添付よりも効果的に、AI エージェントを外部ツールやデータソースへ接続する標準フレームワークを提供する
- MCP ツール統合により、売上メトリクスや現在在庫を動的に取得し、在庫移動のような運用アクションを **明示的な確認付き**で安全に実行できる

**Next** をクリックして、ラボの次のセクションへ進んでください。
