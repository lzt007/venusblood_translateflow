import requests
import json
import time

history_record = []
glossory = {}
glossory_str = ""


def translate_japanese_to_chinese(sentence, history="", glossary="", role="",
                                  model_url="http://localhost:6006/v1/chat/completions"):
    """
    将日语句子翻译成中文

    :param sentence: 要翻译的日语句子
    :param history: 历史上下文
    :param glossary: 术语表
    :param role: 对话的角色
    :param model_url: 本地大模型API地址
    :return: 翻译后的中文句子
    """
    # 构建system prompt
    system_prompt = "你是一个视觉小说翻译模型，可以通顺地使用给定的术语表以指定的风格将日文翻译成简体中文，" \
                    "并联系上下文正确使用人称代词，注意不要混淆使役态和被动态的主语和宾语，" \
                    "不要擅自添加原文中没有的内容或特殊符号，也不要擅自增加或减少换行。" \
                    "不要擅自丢弃原文中存在的标点符号，特殊符号和非日文内容" \
                    "仅返回翻译后的内容，不要描述你的思考过程或在答案中增加其他与原文无关的内容"\
                    "旁白的台词为第三方视角的陈述，避免使用第一人称"

    # 构建user prompt
    # user_prompt = f"[History]\n{history}\n\n参考以下术语表：\n[Glossary]\n{glossary}\n\n" \
    #               f"根据以上术语表的对应关系和备注，结合历史剧情和上下文，" \
    #               f"将下面的文本从日文翻译成简体中文：\n[Input]\n{sentence}"
    user_prompt = f"历史记录：{history}\n\n"\
                  f"参考以下术语表：{glossary}\n\n" \
                  f"根据以上术语表的对应关系和备注，结合历史剧情和上下文，以{role}的口吻" \
                  f"将下面的台词从日文翻译成简体中文：{sentence}"

    # 构建请求数据
    data = {
        # "model": "deepseek-r1:14b",  # 模型名称，根据实际情况调整
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "top_p": 0.8
    }

    try:
        # 发送请求
        response = requests.post(
            model_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            timeout=120
        )

        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            # 提取模型回复内容
            translated_text = result['choices'][0]['message']['content']
            print(f"原句：{sentence}")
            # final_text = translated_text.split('[Input]\n')[1]
            final_text = translated_text
            print(f"译文：{final_text}")
            return final_text
        else:
            print(f"翻译请求失败保留原句，状态码：{response.status_code}")
            print(f"错误信息：{response.text}")
            return sentence

    except Exception as e:
        print(f"翻译过程中发生错误,保留原句：{str(e)}")
        return sentence


def translate(j_str, new_glossory={}, role=""):
    if j_str == "":
        return ""
    if role == "":
        role = "旁白"
    global glossory, glossory_str, history_record
    if len(new_glossory) > len(glossory):
        glossory.update(new_glossory)
        glossory_str = ""
        for k, v in glossory.items():
            glossory_str = glossory_str + f"{k}->{v}"
    if len(history_record) == 0:
        c_str = translate_japanese_to_chinese(j_str, "", glossory_str, role)
    else:
        c_str = translate_japanese_to_chinese(j_str, "\n".join(history_record), glossory_str, role)
    if len(history_record) <= 10:
        history_record.append(c_str)
    else:
        history_record = history_record[:-9] + [c_str]
    return c_str


if __name__ == "__main__":
    # 示例术语表和历史上下文
    glossary_example = {
        "お姉さん": "姐姐",
        "先輩": "前辈"
    }

    history_example = """
    之前的剧情讲述了主角转学到新学校的第一天。
    """

    # 输入输出文件路径
    input_script = "japanese_script.txt"  # 日文台本文件
    output_script = "chinese_translation.txt"  # 中文翻译输出文件

    example = """おはよう、先輩！
あ、おはよう、優子ちゃん。今日も元気そうだね。
うん！実はね、昨日からずっと気になってたことがあって…
ん？どうしたの？
あの…この前、先輩が貸してくれた本、とっても面白かったです！
ああ、『星空の下で』だね。気に入ってくれて嬉しいよ。
でも最後のページが破れていて、結末が分からなくて…
えっ！？ごめん、気づかなかった。大丈夫、あらすじなら話せるよ。
本当ですか？でも…できれば自分で読みたいな。
分かった。じゃあ、今度新しいのを買ってくるから、それまで待っててくれる？
ありがとうございます！先輩って本当に優しいですね。
…いや、別に。それより、今日の放課後、図書館に来ない？
え？また本を貸してくれるんですか？
まあ、そうなんだけど…実は、優子ちゃんに会いたくて。
わ、私ですか！？そ、そんな…（顔を赤らめる）
…やっぱり、やめよう。忘れて。"""

    print("开始翻译台本...")
    for i in example.split("\n"):
        print(i)
        print(translate(i, glossary_example))
    print("台本翻译完成！")
