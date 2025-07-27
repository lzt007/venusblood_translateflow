import os
import json
import traceback
import UnityPy

scenario_path = "./scenario"
translated_dir = "./translated"
output_path = "./output"


def translate(jp_str):
    ch_str = jp_str
    return ch_str


for root, dirs, files in os.walk(scenario_path):
    for file in files:
        try:
            env = UnityPy.load(os.path.join(root, file))
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    # edit asset
                    data = obj.read()
                    origin_data = json.loads(data.m_Script.encode("utf-8", "surrogateescape"))
                    with open(os.path.join(translated_dir, f"{data.m_Name}.json"), "r", encoding="utf-8") as f:
                        keyjson: list = json.load(f)
                    if len(keyjson) != len(origin_data["cuts"]) or origin_data.get("cuts") is None:
                        raise ValueError("数据异常！")
                    for i in range(0, len(keyjson)):
                        origin_data["cuts"][i]["subTitle"] = keyjson[i]["subTitle"]
                        if origin_data["cuts"][i]["window"] is not None:
                            origin_data["cuts"][i]["window"]["texts"] = keyjson[i]["window"]["texts"]
                            origin_data["cuts"][i]["window"]["name"] = keyjson[i]["window"]["name"]
                        # 不要更新原数据里的tag字段
                    data.m_Script = json.dumps(origin_data, ensure_ascii=False)
                    data.save()
                    with open(os.path.join(output_path,file), "wb") as f:
                        f.write(env.file.save())
        except BaseException as e:
            print(f"解析{file}时发生错误：{e}\n{traceback.format_exc()}")
