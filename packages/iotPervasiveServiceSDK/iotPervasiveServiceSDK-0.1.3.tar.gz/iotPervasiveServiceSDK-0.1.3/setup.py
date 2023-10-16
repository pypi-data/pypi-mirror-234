import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iotPervasiveServiceSDK",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.1.3",  # 包版本号，便于维护版本
    author="whu贾向阳团队-葛家和",  # 作者，可以写自己的姓名
    author_email="2898534520@qq.com",  # 作者联系方式，可写自己的邮箱地址
    description="设备端直连框架python",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # Make sure to include 'where' argument
    zip_safe=False,  # Disable zip-safe mode for easier debugging
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
    install_requires=[  # 对应依赖信息
        "bottle==0.12.25",
        "netifaces==0.11.0",
        "paho_mqtt==1.6.1",
        "psutil==5.9.4",
        "Requests>=2.0.0",
        "ujson"
    ],
)
