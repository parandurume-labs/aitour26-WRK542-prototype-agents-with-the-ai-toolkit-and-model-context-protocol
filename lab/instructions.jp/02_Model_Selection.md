# モデル選定: AI Toolkit Model Catalog の探索

このセクションでは、AI Toolkit の Model Catalog を使って、マルチモーダル エージェント プロジェクトに適したモデルを発見・フィルター・比較します。Model Catalog では、GitHub、Microsoft Foundry、OpenAI など複数プロバイダーのモデルにアクセスできます。

## Step 1: フィルターを適用して候補を絞り込む

1. 左サイドバーの **AI Toolkit** 拡張機能アイコンを見つけます
2. AI Toolkit アイコンをクリックして拡張機能パネルを開きます
3. **Developer Tools** 配下の **Discover** を展開し、**Model Catalog** をクリックしてカタログ UI を開きます

![Model Catalog](../../img/model_catalog.png)

ページ上部に人気モデルが表示されます。下にスクロールすると利用可能なモデルの一覧が表示されます。

一覧は多いため、要件に合わせてフィルターを使い候補を絞り込みます。

![Filter Options](../../img/filter_options.png)

### ホスティング プロバイダーでフィルター

1. **Hosted by** フィルターのドロップダウンをクリックします。GitHub（無料で使えるがトークン レート制限ありのモデル）、Microsoft Foundry、OpenAI などに加え、Ollama や ONNX を通じたローカルホストのモデルも選べます。

2. **Microsoft Foundry** を選択し、Microsoft Foundry でホストされているモデルを表示します。Foundry ホストモデルは、エンタープライズ用途に適したセキュリティ／コンプライアンス機能が提供されます。

### パブリッシャー（提供元）でフィルター

1. **Publisher** フィルターのドロップダウンをクリックし、Microsoft、Meta、Cohere など提供元で絞り込みます。オープンソースとプロプライエタリの両方が含まれます。
2. **Meta** を選択し、この主要プロバイダーのモデルを表示します。

### 機能（Feature）でフィルター

1. **Feature** フィルターのドロップダウンをクリックし、画像／音声／動画処理、ツール呼び出し（tool calling）などの能力で絞り込みます。
2. **Image Attachment** を選択し、画像入力を扱えるマルチモーダル モデル（テキスト＋画像の対話）を探します。

## Step 2: モデルをサブスクリプションにデプロイする

フィルター適用後、候補が絞り込まれた一覧が表示されます。
フィルター結果から **Llama-4-Maverick-17B-128E-Instruct-FP8** を見つけます。これは推論性能が良好なマルチモーダル モデルです。

2. モデル タイルの **Deploy** をクリックして、デプロイ構成ウィンドウを開きます。

![Add Model](../../img/add_model.png)

3. **Token Per Minute** のスライダーを右にドラッグして 120K に設定します。その他は既定のままにして、**Deploy to Microsoft Foundry** をクリックし、サブスクリプションにモデル インスタンスをプロビジョニングします。

![Deployment Configuration](../../img/deployment_configuration.png)

## Step 3: Playground を開いてテストする

1. 左サイドバーの **My Resources** を見つけ、Microsoft Foundry プロジェクト配下のリソースを展開します。
1. **Models** 配下に、今デプロイしたモデル インスタンスが表示されます。また、後で比較用に **gpt-5.3-chat** の事前デプロイ インスタンスと、次のセクションでベクター検索／RAG に使用する **text-embedding-3-small** のインスタンスも表示されるはずです。
1. 先ほどデプロイしたモデル インスタンスを右クリックし、ドロップダウンから **Open in Playground** を選択して Playground を開きます。
![Try in playground](../../img/try_in_playground.png)

2. **Model** フィールドに、選択したモデル名が表示されます。

![Model Playground](../../img/model_playground.png)

> [!WARNING]
> 初回アクセス時など、Playground の読み込みに時間がかかる場合があります。モデル初期化が完了するまでしばらくお待ちください。

3. **Compare** ボタンをクリックして左右比較（side-by-side）を有効化します
4. ドロップダウンから、このワークショップ用に Microsoft Foundry へ事前デプロイされている **gpt-5.3-chat** を選択します
5. 比較テスト用に 2 つのモデルが並びます

![Model Comparison](../../img/model_comparison.png)

## Step 4: テキスト生成とマルチモーダル能力をテストする

> [!TIP]
> 左右比較を使うと、同じ入力に対してモデルがどう振る舞うかを正確に見比べられます。ユースケースに最適なモデルを選ぶのに役立ちます。

まずはシンプルなプロンプトで対話してみます。

1. テキスト入力欄（"Type a prompt" と表示されている欄）に、次のプロンプトを入力します。

```
DIY 小売店の店長です。週次の売上サマリーで確認すべき最重要メトリクスは何で、なぜ重要ですか？
```

2. 紙飛行機アイコンをクリックし、両方のモデルに同時に実行します

![Test the model](../../img/test_the_model.png)

次に、推論能力を次のプロンプトで試します。

```
店舗が 3 つ（A, B, C）あります。ブレーカーの総在庫は全店舗合計で 40 個しかなく、補充は 10 日後です。

売れ行きと手元在庫の簡単なスナップショットは次のとおりです。

| Store | Sales trend (WoW) | Avg weekly units sold | Current stock (units) |
|------:|-------------------:|----------------------:|----------------------:|
| A     | +30%              | 18                    | 8                     |
| B     | 0%                | 10                    | 22                    |
| C     | -15%              | 7                     | 10                    |

欠品と機会損失を最小化するには、今日どのように在庫を配分すべきですか？理由をステップバイステップで説明し、追加で確認したい重要データを 3 つ挙げてください。
```

次に、画像処理能力をテストします。

1. テキスト入力欄に次のプロンプトを入力します。

```
この画像に写っているものを説明し、どの種類の電気部品に見えるかを教えてください。
```

2. 画像添付アイコンをクリックし、入力として画像を追加します

![Image Attachment](../../img/image_attachment.png)

3. ファイル選択ウィンドウが表示されます。次の場所に移動します。

```
C:\Users\LabUser\aitour26-WRK542-prototype-agents-with-the-ai-toolkit-and-model-context-protocol\src\instructions
```

次に **circuit_breaker.png** を選択し、**Open** をクリックします。
![Image File Path](../../img/image_file_path.png)

4. 両方のモデルに同時にマルチモーダル プロンプトを送信します。

## Step 5: 結果を分析・比較する

両方のモデルの出力を確認し、以下の観点で評価します。

- **応答品質**: 説明の深さと正確性、プロンプトに対する整合性
- **詳細度**: より包括的な分析をしているのはどちらか
- **処理時間**: 応答速度の違い
- **出力フォーマット**: 明瞭さ、構成、冗長さ（verbosity）。冗長さはトークン使用量とコストに影響します。

### GitHub Copilot を使って比較分析を補助する

比較分析の要約を作るために、GitHub Copilot を活用できます。

GitHub Copilot Chat を開くには、Visual Studio Code 上部の **Toggle Chat** アイコンを選択します。

![Toggle chat button.](../../img/toggle-chat.png)

モデル選択ドロップダウン（**Auto** をクリック）を展開し、*Claude Opus 4.5* を選択します。
![Select claude Opus 4.5](../../img/select_claude_opus.png)

> [!TIP]
> ドロップダウンの 'Other models' セクションを展開すると、Claude Opus 4.5 が見つかる場合があります。

> [!WARNING]
> ログインしていない場合、モデルを選択できません。前のセクションの手順で GitHub Copilot にサインイン済みであることを確認してください。もしくは、プロンプト送信によってサインイン フローが起動することもあります。

Copilot チャットで次のプロンプトを試します。

```
#mcp_azure_mcp_foundry Zava（米国に 20 店舗＋オンラインを持つ DIY 小売企業）の店舗運営と本部の販売分析を支援する AI エージェント向けにモデルを評価しています。Llama-4-Maverick-17B-128E-Instruct-FP8 と OpenAI GPT-5.3-chat を比較中です。このシナリオではどちらを推奨しますか？推論能力、コスト、レイテンシ、コンテキスト長などの観点でトレードオフを説明し、意思決定できるようにしてください。
```

この質問に対して Copilot は *Foundry MCP server* のツールを呼び出し、ユースケースに基づくモデル推奨を行います。Foundry MCP server ツールへのアクセス許可を求められた場合は、**Allow in this session** をクリックして続行してください。分析に必要な情報を収集するために、複数回許可を求められる場合があります。

![Get AI model guidance](../../img/get_ai_model_guidance.png)

最終的な回答では、2 つのモデルの詳細比較と、このプロジェクト向けの推奨が提示されるはずです。

## Step 6: Microsoft Foundry から選択したモデルを利用する

比較が終わったら、次のセクションでのプロトタイピングに進むため、どちらかのモデルを選択します。この演習では **GPT-5.3-chat** を選びます。

> [!TIP]
> 通常の Playground（単一ペイン＋単一モデル）に戻すには、モデル名右側の **Select this model** をクリックします。
>
> ![Select this model](../../img/select_this_model.png)

## まとめ（Key Takeaways）

- Model Catalog は複数プロバイダーの AI モデルを一覧できる
- フィルター機能で要件に合うモデルを素早く絞り込める
- Playground の比較機能で、データに基づいた意思決定ができる
- ホスティング オプションにより、開発段階に応じたメリットが異なる
- 比較 UI を使ってマルチモーダル能力も効率よくテストできる

このプロセスにより、性能、コスト、機能、デプロイ要件などのバランスを取りながら、ユースケースに最適なモデルを選べます。
**Next** をクリックして、ラボの次のセクションへ進んでください。
