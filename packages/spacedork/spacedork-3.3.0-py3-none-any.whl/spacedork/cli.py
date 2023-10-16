import argparse
import asyncio
import os
import yaml
from spacedork import reps
home_directory = os.path.expanduser("~")
config_file_path = os.path.join(home_directory, ".config", 'spacedork', 'config.yaml')


def cmd_parser():
    parser = argparse.ArgumentParser(description='这是一个示例命令行参数解析程序')
    parser.add_argument('--list-module', required=False, help='列举所有模块', action='store_true')
    parser.add_argument('--config', '-c', required=False, help=f'配置文件路径({config_file_path})',
                        default=config_file_path)
    parser.add_argument('--dork', '-q', required=False, help='查询dork关键字')
    parser.add_argument('--module', '-m', required=False, default='zoomeye', help='使用查询模型')
    parser.add_argument('--start-page', '-sp', type=int, default=1, help='要处理的数量')
    parser.add_argument('--end-page', '-ep', type=int, default=1, help='要处理的数量')
    parser.add_argument('--thread', '-t', type=int, default=2, help='协程数')
    parser.add_argument('--fields', '-f', default="url", help='输出字段(url|ip|port|address)')
    args = parser.parse_args()
    if args.fields not in ("url","ip","port","address"):
        print("请选择输出字段(url|ip|port)")
        exit()
    if args.list_module:
        for k, v in reps.repo.items():
            print(k)
        exit()
    elif not args.dork:
        print("请提供dork关键字")
        exit()
    if not os.path.exists(args.config):
        print("配置文件不存在:{}".format(args.config))
        exit()
    return args


def main():
    args = cmd_parser()
    with open(args.config, "r") as yaml_file:
        try:
            yaml_data = yaml.safe_load(yaml_file)
        except yaml.YAMLError as e:
            print(f"YAML解析错误: {e}")
            return
    plugin = reps.repo.get(args.module)
    plugin_config = yaml_data.get(args.module, {})
    cls = plugin(**plugin_config,thread=args.thread,fields=args.fields)
    coroutine = cls.search(args.dork, args.start_page, args.end_page)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine)


if __name__ == '__main__':
    main()
