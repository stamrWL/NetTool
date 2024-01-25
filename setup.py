from setuptools import setup, find_packages

setup(
    name="NetTool",  # 包的名称
    version="0.1.0",    # 版本号
    description="NetTool",  # 包的描述
    author="stamr",  # 作者名字
    author_email="stamrwl@163.com",  # 作者电子邮件
    url="https://github.com/stamrWL/NetTool",  # 项目的 URL

    packages=find_packages(),  # 自动查找并包含所有的包
    install_requires=[  # 依赖的其他包
    ],

    # 可选项：包含额外的文件，如配置文件、数据文件等
    # data_files=[("config", ["config.ini"]), ("data", ["data_file.csv"])],

    # 可选项：指定入口点，用于命令行脚本
    # entry_points={
    #     "console_scripts": [
    #         "myscript = mypackage.mymodule:main",
    #     ],
    # },

    # 可选项：其他配置，如指定包含的文件、排除文件等
    # include_package_data=True,
    # package_data={
    #     "mypackage": ["data/*.dat"],
    # },
)
