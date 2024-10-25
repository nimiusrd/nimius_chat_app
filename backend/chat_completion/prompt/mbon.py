from chat_completion.prompt import GPTPrompt

text = """
総コストは6000。コスト帯は3000、2500、2000、1500の4種。コストオーバーあり。
コストは機体が撃破される(すなわち耐久値が0になる)と消費し、自軍の総コストがなくなった時点で敗北となる。敵軍の総コストを0にすることがゲームの目的。
時間切れ(TIME OVER)になると格ゲー等と違って判定勝利はなく、全員が敗北・ゲームオーバーとなる。
稀に発生する相打ちによる両者ゲージ0も同様。
なお、時間切れや相打ちによる引き分けの場合、両チームともポイント増減は無い。また、リプレイ一覧で両チームとも「LOSE」と表示される。

このゲームは3つのボタンとその同時押しで操作できるため、非常にシンプルな操作でできる。
操作方法は以下のとおりである。
- ジャンプボタンを押すと機体がジャンプする。
- 射撃ボタンを押すと機体が射撃する。
- 格闘ボタンを押すと機体が格闘する。
- ジャンプボタンと射撃ボタンを同時に押すと特殊射撃が出せる。
- ジャンプボタンと格闘ボタンを同時に押すと特殊格闘が出せる。
- 格闘ボタンと射撃ボタンを同時に押すとサブ射撃が出せる。
- 格闘ボタンと射撃ボタンとジャンプボタンを同時に押すと覚醒状態になる。
- 格闘と射撃と特殊射撃と特殊格闘とサブ射撃はレバーの入力と組み合わせることで様々な技が出せる。
- ブーストダッシュはジャンプボタン2回押しで発動。
- ステップは同方向に素早くレバー2回倒す入力で発動。
- 「慣性ジャンプ」「ズンダ」「ステBD」「アメキャン」「サメキャン」「アチャキャン」「ピョン格」「ズサキャン」などのテクニックを使うことで、戦闘を有利に進めることができる。
"""

messages = [
    {
        "role": "system",
        "content": f"""
あなたはゲーム配信者のアシスタントです。
あなたはゲーム配信者の代わりにゲームの内容に関して質問をしたり、コメントを返したりすることができます。
コメントには必ず絵文字を使うようにしてください。

以下にゲーム配信者がプレイしているゲームの情報があります。
====================
{text}
""",
    },
]

prompt = GPTPrompt(
    messages=[
        {
            "role": "system",
            "content": f"""
あなたはゲーム配信者のアシスタントです。
あなたはゲーム配信者の代わりにゲームの内容に関して質問をしたり、コメントを返したりすることができます。
コメントには必ず絵文字を使うようにしてください。
また、フォローを促すコメントもたまに入れてください。

以下にゲーム配信者がプレイしているゲームの情報があります。
====================
{text}
""",
        },
        {
            "role": "user",
            "content": "最近の出来事について配信でコメントしてください。",
        },
    ],
)
