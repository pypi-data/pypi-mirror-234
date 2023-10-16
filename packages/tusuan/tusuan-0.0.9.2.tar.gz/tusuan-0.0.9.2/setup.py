from setuptools import setup, find_packages


def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


setup(name='tusuan',  # 包名
      python_requires='>=3.8.0',  # python环境
      version='0.0.9.2',  # 包的版本
      description="useful functions.",  # 包简介，显示在PyPI上

      long_description=read('README.md'),  # 读取的Readme文档内容，一整块字符串
      long_description_content_type="text/markdown",  # 指定包文档格式为markdown

      author="tusuan",  # 作者相关信息
      author_email='btk@qq.com',
      url='https://github.com/tusuan',

      # 指定包信息，还可以用find_packages()函数  # find_packages(where="./", include=["tusuan*"]),
      # packages=["tusuan",
      #           "tusuan.image_video_utils"],
      packages=find_packages(where=".", include=["tusuan*"]),
      install_requires=read('requirements.txt').splitlines(),  # 指定需要安装的依赖, 需要是一个列表

      include_package_data=True,  # 不知道做啥的
      license="MIT",
      keywords=['tusuan'],
      classifiers=[  # 一些网站的分类信息，方便用户检索
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10'
      ])

"""
rm -rf ./dist
pipreqs ./ --encoding=utf8 --force --mode no-pin
python3 setup.py sdist 
twine upload --repository tusuan@testpypi dist/*
pip install -i https://test.pypi.org/simple/ -U tusuan

twine upload --repository tusuan@pypi dist/*
"""
