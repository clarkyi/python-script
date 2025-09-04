#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Clarkyi clarkywq@gmail.com
#
# Distributed under terms of the MIT license.
import subprocess
import argparse
from datetime import datetime, timedelta

# 受保护的分支，不允许删除
PROTECTED_BRANCHES = {
    'feature/test_merge',
    'feature/dev_merge',
    'develop',
    'master'
}

def run_git_command(command):
    """执行Git命令并返回输出结果"""
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"执行命令失败: {command}")
        print(f"错误信息: {e.stderr}")
        return None

def get_local_branches():
    """获取所有本地分支"""
    output = run_git_command("git branch --format='%(refname:short)'")
    if output:
        return [branch.strip("'") for branch in output.splitlines()]
    return []

def get_remote_branches():
    """拉取远程最新信息，并清理本地缓存的已删除远程分支"""
    run_git_command("git fetch --prune origin")
    """获取所有远程分支（去除origin/前缀）"""
    output = run_git_command("git branch -r --format='%(refname:short)'")
    if output:
        return [branch.strip("'").replace('origin/', '') for branch in output.splitlines()]
    return []

def get_branch_creation_time(branch_name, is_remote=False):
    """获取分支的创建时间（基于最早提交）"""
    ref = f"origin/{branch_name}" if is_remote else branch_name
    # 获取分支最早提交的时间
    output = run_git_command(f"git log --reverse --pretty=format:'%ci' {ref} | head -1")
    if output:
        try:
            # 解析时间字符串，忽略时区部分
            time_str = output.strip("'").split(' +')[0]
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(f"无法解析 {branch_name} 的时间格式: {output}")
    return None

def filter_branches_by_time(branches, is_remote, min_time=None, max_time=None):
    """根据时间范围过滤分支"""
    filtered = []
    for branch in branches:
        create_time = get_branch_creation_time(branch, is_remote)
        if not create_time:
            continue
            
        include = True
        if min_time and create_time < min_time:
            include = False
        if max_time and create_time > max_time:
            include = False
            
        if include:
            filtered.append(branch)
    return filtered

def delete_branches(branches, is_remote=False, dry_run=False):
    """删除指定的分支"""
    if not branches:
        print("没有符合条件的分支需要删除")
        return
        
    print(f"\n准备{'模拟' if dry_run else ''}删除{'远程' if is_remote else '本地'}分支:")
    for branch in branches:
        print(f"- {branch}")
    
    confirm = input("\n确认执行删除操作? (y/N): ").strip().lower()
    if confirm != 'y':
        print("已取消删除操作")
        return
    
    for branch in branches:
        if is_remote:
            cmd = f"git push origin --delete {branch}"
        else:
            cmd = f"git branch -D {branch}"
            
        if dry_run:
            print(f"[模拟] 执行: {cmd}")
        else:
            print(f"删除 {branch}...")
            run_git_command(cmd)

def main():
    parser = argparse.ArgumentParser(description='清理Git本地和远程分支工具')
    parser.add_argument('--delete', nargs='+', help='指定要删除的分支名称')
    parser.add_argument('--skip', nargs='+', default=[], help='指定要跳过的分支名称')
    parser.add_argument('--older-than', type=int, help='删除创建时间早于指定天数的分支')
    parser.add_argument('--newer-than', type=int, help='删除创建时间晚于指定天数的分支')
    parser.add_argument('--remote', action='store_true', help='操作远程分支')
    parser.add_argument('--dry-run', action='store_true', help='模拟操作，不实际删除')
    
    args = parser.parse_args()
    
    # 获取分支列表
    branches = get_remote_branches() if args.remote else get_local_branches()
    if not branches:
        print("没有找到任何分支")
        return
    
    # 过滤受保护的分支
    branches = [b for b in branches if b not in PROTECTED_BRANCHES]
    print(f"找到符合条件的分支 {len(branches)} 个（已排除受保护分支）")
    
    # 应用过滤条件
    filtered_branches = branches
    
    # 按名称删除
    if args.delete:
        filtered_branches = [b for b in filtered_branches if b in args.delete]
    
    # 按跳过列表过滤
    if args.skip:
        filtered_branches = [b for b in filtered_branches if b not in args.skip]
    
    # 按时间过滤
    time_filters = []
    if args.older_than:
        max_time = datetime.now() - timedelta(days=args.older_than)
        time_filters.append(f"早于 {args.older_than} 天")
    else:
        max_time = None
        
    if args.newer_than:
        min_time = datetime.now() - timedelta(days=args.newer_than)
        time_filters.append(f"晚于 {args.newer_than} 天")
    else:
        min_time = None
    
    if max_time or min_time:
        filtered_branches = filter_branches_by_time(
            filtered_branches, 
            args.remote,
            min_time,
            max_time
        )
        if time_filters:
            print(f"应用时间过滤: {', '.join(time_filters)}，剩余 {len(filtered_branches)} 个分支")
    
    # 执行删除
    delete_branches(filtered_branches, args.remote, args.dry_run)

if __name__ == "__main__":
    main()
