from setuptools import setup, find_packages

VERSION = '0.0.6'

setup(
    name="mkdocs-aliyun-computenest",
    version=VERSION,
    url='https://github.com/aliyun-computenest/quickstart-demo',
    license='BSD',
    description='Aliyun computenest theme for MkDocs',
    author='liuqi.lq',
    author_email='liuqi.lq@alibaba-inc.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'aliyuncomputenest = aliyun_computenest',
        ]
    },
    zip_safe=False
)