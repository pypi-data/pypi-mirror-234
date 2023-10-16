import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = "4.0.0a1"

py_modules = [
    "phapbm",
]

project_urls={
    "Github": "https://github.com/DashStudio/phap",
    "Old Project Version(stralgo)": "https://pypi.org/project/stralgo/"
}  #额外链接

classifiers=[
    #"Development Status :: 1 - Planning",
    #"Development Status :: 2 - Pre-Alpha",
    #"Development Status :: 3 - Alpha",
    #"Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    "Development Status :: 6 - Mature",
    "Development Status :: 7 - Inactive",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: 3.11",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: BSD License",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    #"Operating System :: Microsoft :: Windows",
    "Natural Language :: English",
    "Natural Language :: Chinese (Simplified)",
]

install_requires = []

extras_require = {
#    ':python_version<"3.4"': ['pathlib2'],
#    ':python_version<"3.3"': ['backports.shutil_get_terminal_size'],
#    ':python_version<="2.7"': [
#        'decorator<5',
#        'pyte<0.8.1'
#    ],
#    ':python_version>"2.7"': [
#        'decorator',
#        'pyte'
#    ],
#    ":sys_platform=='win32'": [
#        'win_unicode_console'
#    ]
}

entry_points={
#    'console_scripts': [
#        'test-stralgo = stralgo-tools:test',
#    ],
}

scripts=[]

python_requires=">=3.9"

setuptools.setup(
    name = "phap",
    version = VERSION,
    author = "DashBing",
    author_email = "mcbbkf@outlook.com",
    description = "Programing Helpful Algorithm Package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    #license="Apache 2.0",
    scripts = scripts,
    url = "https://github.com/DashStudio/phap",
    project_urls = project_urls,
    classifiers = classifiers,
    install_requires = install_requires,  #依赖项定义
    extras_require = extras_require,
    entry_points = entry_points,  #scripts定义
    package_dir = {"": "src"},  #包名和值的目录 有效包存放根目录
    packages = setuptools.find_packages(where="src"),
    py_modules = py_modules,
    python_requires = python_requires,  #支持版本
    #platforms=["Windows"],  #支持系统
)
