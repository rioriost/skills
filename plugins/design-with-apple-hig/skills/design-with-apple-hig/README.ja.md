<div align="center">
  <img src="assets/mark.svg" width="112" alt="Apple HIG Design Skill マーク">
  <h1>Apple HIG Design Skill</h1>
  <p><code>design-with-apple-hig</code></p>
  <p>Appleプラットフォームの設計・実装・レビュー・監査を、一次情報から進めるCodexスキルです。</p>

  [![Validate](https://github.com/rioriost/design-with-apple-hig/actions/workflows/validate.yml/badge.svg)](https://github.com/rioriost/design-with-apple-hig/actions/workflows/validate.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f.svg)](LICENSE)

  [English](README.md)
</div>

[Sunwood-ai-labs/design-with-apple-hig](https://github.com/Sunwood-ai-labs/design-with-apple-hig) のforkです。一次情報を重視する設計とMITライセンスを維持し、鮮度・OS世代の確認、ポリシーの独立分類、プラットフォーム別検証、レビュー記録、取得処理の回帰テストを追加しています。

## ✨ 概要

`design-with-apple-hig` は、最新のApple公式ガイダンス、SDKの事実、アクセシビリティ根拠、画面上の観察、専門スキルのヒューリスティック、静的監査の検出結果を、権威の異なる証拠として整理して扱います。

主な対象は次のとおりです。

- iOS、iPadOS、macOS、watchOS、tvOS、visionOS
- SwiftUI、UIKit、AppKitによる実装
- 設計、実装、レビュー、採点、リファクタリング、監査
- Dynamic Type、VoiceOver、semantic color、適応レイアウト、Reduce Motion、代表状態の検証
- ホスト側の規範を守ったApple-inspired WebおよびクロスプラットフォームUI

## 🧭 このスキルが必要な理由

コミュニティ製HIGスキルには、公式要件、古いスナップショット、個人的なヒューリスティック、固定数値、プラットフォームをまたぐ一般化が混在する場合があります。本スキルは次の優先順位を守ります。

1. Appleのデザイン判断は、最新のApple HIGと公式Design Resourcesで裁定する。
2. APIと実装挙動は、現行SDKドキュメントで裁定する。
3. アクセシビリティ上の主張は、適用可能な標準とプラットフォーム機能で裏付ける。
4. 第三者スキルは限定的な専門家として使い、規範の裁定者にはしない。
5. 静的監査結果を、HIG準拠の証明として扱わない。

## 🚀 インストール

macOS/LinuxではCodexのskillsディレクトリへcloneします。

```bash
git clone https://github.com/rioriost/design-with-apple-hig.git "${CODEX_HOME:-$HOME/.codex}/skills/design-with-apple-hig"
```

Windowsの場合:

```powershell
git clone https://github.com/rioriost/design-with-apple-hig.git "$env:USERPROFILE\.codex\skills\design-with-apple-hig"
```

同名のスキルが既にある場合は、既存の作業内容を確認してから更新してください。インストールせず参照資料として利用することもできます。

## 💬 使い方

スキルを明示的に呼び出します。

```text
Use $design-with-apple-hig to review and refactor this SwiftUI screen.
```

証拠の種類を分離してレビューする例です。

```text
Use $design-with-apple-hig to review this interface. Separate Apple guidance,
framework facts, accessibility evidence, visible observations, audit signals,
and heuristics. Score only verified dimensions.
```

## 🏗️ 構成

```text
SKILL.md
├── タスク、PF、Framework、成果物、入力方式を分類
├── 必要最小限の最新一次資料を取得
├── 原典の適用範囲と表現強度を維持
├── 関係する専門機能だけをルーティング
└── 実装、描画、アクセシビリティ、findingを再検証

references/
├── official-source-map.md   Apple一次資料へのルーティング
├── source-routing.md        根拠の分類と競合解決
├── freshness.md             正式版・ベータ版、参照日、変更検出
├── codex-workflows.md       設計レビューと実装レビューの使い分け
├── platform-routing.md      Apple-native、Web、cross-platformの境界
├── review-rubric.md         証拠ベースの重大度と採点
├── verification-loop.md     build、描画、操作、再テスト
├── review-record-template.md 出典、finding、検証結果の記録
├── regression-scenarios.md  スキル自体の動作評価シナリオ
└── bibliography.md          過去に精査した資料と採用方針
```

## 🔎 証拠モデル

重要な推奨を次のクラスへ分離します。

| Evidence | 意味 |
| --- | --- |
| `APPLE-HIG` | 適用範囲を確認した現在のAppleデザイン指針 |
| `APPLE-SDK` | 文書化されたAPI仕様と利用可能なOS |
| `APPLE-POLICY` | 適用条件を確認したApp Review・配布ポリシー |
| `APPLE-RESOURCE` | 公式デザインキットやアセットの指針 |
| `ACCESSIBILITY` | 適用可能なアクセシビリティ標準または機能で裏付け済み |
| `OBSERVATION` | コード、スクリーンショット、プロトタイプ、実動UIから観察可能 |
| `AUDIT` | 静的解析の検出結果。文脈確認が必要 |
| `HEURISTIC` | 妥当な設計提案だがApple公式要件ではない |

## ✅ 検証

Python 3.10以降が必要です。ヘルパーとテストは標準ライブラリのみを使います。リポジトリのルートで実行します。

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/fetch_apple_hig.py scripts/validate_repository.py
```

Apple公式DocC JSONから、現在のHIGトピックを確認できます。

```bash
python3 scripts/fetch_apple_hig.py materials --metadata-only
```

GitHub Actionsではmainへのpushとpull requestに対し、Python 3.10・3.12・3.13で構造・ローカルリンク・コンパイル・CLI・オフライン回帰テストを実行します。テストは抽出、適用範囲の保持、変更検出、取得失敗、リンク切れを対象とし、ネットワークを使いません。Apple資料の鮮度やエージェントの動作を保証するものではありません。スキルの評価には[動作シナリオ](references/regression-scenarios.md)を使用します。

## ライブ資料と検証記録

同梱資料は参照先と手順を示す独自文書です。HIG本文のスナップショットではありません。重要なデザイン判断、数値、表現の強さ、APIの利用可能性、OSの正式版・ベータ版、App ReviewポリシーはライブのApple一次資料で確認します。同一タスク内の出典記録は状況が変わらなければ再利用でき、オフライン時は鮮度の未確認を明示します。[鮮度確認の手順](references/freshness.md)を参照してください。

取得ヘルパーの`--compare-metadata PATH`で、過去の`--metadata-only` JSONと比較できます。取得日時、Appleの更新情報、本文を含む応答全体のハッシュ、抽出上の注意点を記録します。ハッシュの変化は内容確認のきっかけであり、不変でも最新OSへの対応や完全な抽出を保証しません。主張の根拠には本文を読み、画像・動画・複雑な表は公式ページで確認します。

[Codexのワークフロー](references/codex-workflows.md)で設計レビューと実装レビューを使い分け、[記録テンプレート](references/review-record-template.md)に出典、継続使用するfinding ID、スクリーンショット、検証結果を残します。ビルド、実際の描画、アクセシビリティ自動監査、VoiceOver実操作、キーボードとフォーカス、Reduce Motionは別々の証拠です。実機や支援技術で確認できなかった項目は未検証として残します。

## 📚 参考文献と出典管理

[参考文献](references/bibliography.md)には、Apple一次資料と、限定的な専門ロールの参考にしたコミュニティスキル・ツールを記録しています。第三者のHIGコーパスやApple文書本文は複製せず、参照先と採用判断だけを保持します。

実行時の参照先は[公式資料マップ](references/official-source-map.md)を確認してください。正確な数値、現行API、OS固有の挙動、規範的な主張は、スキル実行時に最新のApple公式資料で再確認します。

## ⚖️ ライセンス

本プロジェクト独自のコードと文書は[MIT License](LICENSE)で公開します。リンク先のApple資料、商標、Design Resources、第三者プロジェクトには、それぞれの利用条件とライセンスが適用されます。

## ℹ️ 免責事項

本プロジェクトは独立したコミュニティプロジェクトであり、Apple Inc.との提携、承認、支援関係はありません。「Apple」および各プラットフォーム名等はApple Inc.の商標です。本スキルによるレビューは証拠に基づく設計支援であり、Appleによる認証ではありません。
