# ClearBranch

## usage clear branch

### Step1
```
git clone https://github.com/clarkyi/python-script.git
```
### Step2
```
cd python-script
python clear-git-branch/init_script.py
```
### Step3
输入密码后可以切换至需要清理分支的项目下执行下面的命令
```
clear_branch --help
```
as
```
清理Git本地和远程分支工具

options:
  -h, --help            show this help message and exit
  --delete DELETE [DELETE ...]
                        指定要删除的分支名称
  --skip SKIP [SKIP ...]
                        指定要跳过的分支名称
  --older-than OLDER_THAN
                        删除创建时间早于指定天数的分支
  --newer-than NEWER_THAN
                        删除创建时间晚于指定天数的分支
  --remote              操作远程分支
  --dry-run             模拟操作，不实际删除

```

## 测试所依赖的版本如下
+ git  2.40.0
+ python 3.13.1


## ISSUES
如若发现其他版本欢迎提[issues](https://github.com/clarkyi/python-script/issues)和提pull request

