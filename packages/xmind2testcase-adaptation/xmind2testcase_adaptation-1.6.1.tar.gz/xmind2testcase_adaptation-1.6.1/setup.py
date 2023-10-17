from setuptools import setup,find_packages
import io
with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xmind2testcase_adaptation',
    url='https://github.com/baby-five/xmind2testcase',
    version='1.6.1',
    author="baby-five",
    author_email='1073434718@qq.com',
    description='1、支持xmindzen 2、支持导出excel 3、根据gs禅道优化导出字段 4、修复部分问题',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[# 分类索引 ，pip 对所属包的分类
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    packages = find_packages(exclude=['tests', 'test.*', 'docs']),  # custom
    package_data={  # custom
        '': ['README.md'],
        'webtool': ['static/*', 'static/css/*', 'static/guide/*', 'templates/*', 'schema.sql'],
    },
    keywords=[
        'xmind2testCase, testcase, test, testing, xmind, 思维导图, XMind思维导图',
    ],

    # 需要安装的依赖
    install_requires=[
        "xmind",
        "flask",
        "arrow",
    ],
    # 入口模块 或者入口函数
    entry_points={
        'console_scripts': [
            'xmind2testcase=xmind2testcase.cli:cli_main',
        ]
    },
    zip_safe=False
)