import click
from moyanlib.http import request
import moyanlib
import platform as pf
import time as _time
import hashlib as h
import os
import moyanlib.cli.poject as pj
import moyanlib.cli.initpj as initpj


@click.group()
def cli():
    pass


@cli.command(help="发起HTTP请求")
# 参数
@click.option('--url', '-u', help="请求地址")
@click.option('--method', '-m', default='GET', help="请求方法")
@click.option('--cookies', '-c', help="请求cookie", default='')
def requests(url, method, cookies):
    req = request()
    header = {}
    header["cookie"] = cookies
    requ = req.send({
        "url": url,
        "method": method
    })
    click.echo(requ.text)


@cli.command(help="清除pyc")
def clear_pyc():
    # 使用os遍历所有目录
    for root, dirs, files in os.walk("."):
        for file in files:

            if file.split(".")[-1] == "pyc":
                path = os.path.join(root, file)
                print("正在删除："+path)
                os.remove(path)
    click.echo("清除完成")


@cli.command(help="生成设备ID")
def DeviceId():
    click.echo(moyanlib.getDeviceID())


@cli.group(help="获取当前时间")
def time():
    click.echo(_time.strftime("%Y-%m-%d %H:%M:%S", _time.localtime()))


@time.command(help="获取当前时间戳")
@click.option("--three", help="13位时间戳", is_flag=True, default=False)
def get_timestamp(three):
    if three:
        click.echo(_time.time())
    else:
        click.echo(int(_time.time()))


@time.command(help="获取当前时间（可自定义）")
@click.option("--format", "-f",help="时间格式", default="%Y-%m-%d %H:%M:%S")
def get_time(format):
    click.echo(_time.strftime(format, _time.localtime()))


@cli.group(help="文件操作")
def file():
    pass


@file.command(help="创建文件夹")
@click.argument("path")
def mkdir(path):
    if os.path.exists(path):
        click.echo("文件夹已存在")
    else:
        os.mkdir(path)
        click.echo("文件夹创建成功")

@cli.group(help="项目")
def project():
    pass

@project.command(help="创建项目")
@click.option("--path", "-p", help="项目路径",default="./")
@click.argument("types")
def create(path,types):
    try:
        func = getattr(pj, types)
    except AttributeError:
        click.echo("项目类型错误")
    else:
        PJ_name=input("项目名: ")
        PJ_author=input("作者: ")
        PJ_site=input("项目地址: ")
        PJ_license=input("许可证: ")
        func(path,PJ_name,PJ_author,PJ_site,PJ_license)
    

@project.command(help="配置项目")
@click.argument("types")
def init(types):
    try:
        func = getattr(pj, types)
    except AttributeError:
        click.echo("项目类型错误")
    else:
        func()


