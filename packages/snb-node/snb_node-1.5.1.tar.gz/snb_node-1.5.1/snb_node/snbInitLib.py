import traceback
from pip._internal.cli.main import main as pip_main


def snbPipLib():
    # node 需要添加安装包，参照此执行
    try:
        import schema
        print("schema success!")
        ##pip_main(['uninstall', 'schema'])
    except Exception as e:
        log=traceback.format_exc()
        print(log)
        pip_main(['install', 'schema'])

    try:
        import pyecharts
        print("pyecharts success!")
        ##pip_main(['uninstall', 'schema'])
    except Exception as e:
        log=traceback.format_exc()
        print(log)
        pip_main(['install', 'pyecharts'])
    # node 需要添加安装包，参照此执行
    # 按照上面的逻辑重复添加

    try:
        import neo4j
        print("neo4j success!")
        ##pip_main(['uninstall', 'schema'])
    except Exception as e:
        log=traceback.format_exc()
        print(log)
        pip_main(['install', 'neo4j'])

    try:
        import duckdb
        print("duckdb success!")
        ##pip_main(['uninstall', 'schema'])
    except Exception as e:
        log=traceback.format_exc()
        print(log)
        pip_main(['install', 'duckdb'])

    try:
        import duckdb_engine
        print("duckdb-engine success!")
        ##pip_main(['uninstall', 'schema'])
    except Exception as e:
        log=traceback.format_exc()
        print(log)
        pip_main(['install', 'duckdb-engine'])


##snbPipLib()
