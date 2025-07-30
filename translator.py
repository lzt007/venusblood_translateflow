import requests
import json


def translate(text,glossary={},role=""):
    """
    将字符串中的日文翻译为中文，保留非日文部分，并处理《》包裹的专有名词

    参数:
        text: 包含日文的输入字符串

    返回:
        str: 翻译后的中文字符串
    """
    if text == "" or text == " ":
        return text
    # 构造包含翻译要求的prompt
    prompt = f"""你是一个日文galgame汉化专家，你将帮我汉化一款日文游戏。请将以下游戏对话文本中的日文翻译成中文，并遵守以下规则：
1. 非日文部分保持原样不变
2. 遇到以《-开头以-》结尾的内容时：
   - 跳过翻译
   - 在最终输出时移除开头的《-和结尾的-》符号
3. 这是对话内容，请保持上下文连贯性
4. 只返回翻译结果，不要添加任何额外说明
5. 如果输入了空字符串，则返回空字符串
6. 不要在结果中添加原文，结果中务必保证只有中文译文

需要翻译的内容：
{text}

翻译结果："""

    # Ollama API请求配置
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:14b",  # 可替换为实际使用的模型名
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,  # 较低温度保证结果稳定性
            "num_ctx": 4096,  # 足够大的上下文窗口
        }
    }

    try:
        # 发送API请求
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应
        result = json.loads(response.text)
        # print(result)
        translated_text = result.get("response", "").strip()
        # print(translated_text)
        # 移除可能出现的提示前缀
        if "翻译结果：" in translated_text:
            translated_text = translated_text.split("翻译结果：", 1)[-1].strip()
        if "</think>" in translated_text:
            translated_text = translated_text.split("</think>")[1]
        translated_text = translated_text.replace("\r", "").replace("\n", "")
        print(f"{text} -> {translated_text}")
        return translated_text

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ollama API请求失败: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError("API返回无效的JSON响应")


if __name__ == "__main__":
    print(translate("天運、我にあり《角色1》"))
