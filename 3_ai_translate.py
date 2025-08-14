from scenario.translate import run

keyjson_dir = "./keyjson"
translated_dir = "./translated"
roles_path = "./static/roles.json"
subTitles_path = "./static/subTitles.json"
sub_role = "罗兰"

run(keyjson_dir, translated_dir, roles_path, subTitles_path, sub_role)
