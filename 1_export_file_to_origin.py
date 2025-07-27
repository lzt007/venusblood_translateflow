import os
import UnityPy
import json
import traceback

scenario_path = "./scenario"
export_dir = "./export_origin"

for root, dirs, files in os.walk(scenario_path):
    for file in files:
        try:
            env = UnityPy.load(os.path.join(root, file))
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    # export_origin asset
                    data = obj.read()
                    json_data = json.loads(data.m_Script.encode("utf-8", "surrogateescape"))
                    print(json_data)
                    path = os.path.join(export_dir, f"{data.m_Name}.json")
                    with open(path, "wb") as f:
                        f.write(json.dumps(json_data, ensure_ascii=False).encode("utf-8"))
                    # # edit asset
                    # fp = os.path.join(replace_dir, f"{data.m_Name}.txt")
                    # with open(fp, "rb") as f:
                    #     data.m_Script = f.read().decode("utf-8", "surrogateescape"))
                    # data.save()
        except BaseException as e:
            print(f"解析{file}时发生错误：{e}\n{traceback.format_exc()}")
