import dll_file
import sys
def run():
    dbp_api = dll_file.DllMode(ip="172.18.240.191", user="admin", passwd_str="admin", port="12084")
    if not dbp_api.is_connect():
        print("服务器连接失败，请使用init_write_sis(ip, user, passwd port)强制刷新写sis的服务器连接信息后重试！")
        print("如果刷新后仍然连接失败，请检查设置参数是否正确！")
        print("写入SIS失败")
        return None
    if len(sys.argv) == 1:
        print("缺少命令行参数，need cmd parameters")
        print("写入SIS失败")
        return None
    json_str = sys.argv[1]
    tags_values = eval(json_str)
    tags = list(tags_values.keys())
    values = list(tags_values.values())
    dbp_api.write_snapshot_double(tags=tags, values=values)
    print("写入SIS成功")
run()
