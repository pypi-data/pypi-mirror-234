from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fp_th_di',
    packages=find_packages(include=[
        'fp_th_di',
        'fp_th_di.mail_box'
    ]),
    version='3.0.4',
    description='Foodpanda Thailand Data & Insight team utility functions',
    author='Mathara Rojanamontien',
    author_email="mathara.rojanamontien@foodpanda.co.th",
    license='Delivery Hero (Thailand) Co., Ltd.',
    long_description=long_description,
    classifiers=(
        "Programming Language :: Python :: 3",
    ),
)
