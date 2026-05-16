import os
import hashlib
import json

def calculate_md5(file_path):
    """计算单个文件的 MD5 值（分块读取，防止大文件撑爆内存）"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def generate_manifest():
    print("=== HAZK 自动打包与 MD5 生成工具 (V2 净化版) ===")
    version = input("请输入新版本号 (例如 1.0.1): ")
    changelog = input("请输入更新日志: ")

    manifest = {
        "version": version,
        "changelog": changelog,
        "files": {}
    }

    # 遍历当前文件夹下的所有文件
    for root, dirs, files in os.walk("."):
        
        # 【核心修复】：强制从遍历目录中剔除所有以点开头的隐藏文件夹（如 .git, .vscode, .update_temp）
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            # 忽略脚本自身、生成的 json、以及隐藏文件
            if file in ["build_manifest.py", "manifest.json"] or file.startswith('.'):
                continue

            file_path = os.path.join(root, file)
            # 获取相对路径，并把 Windows 的反斜杠 \ 统一换成正斜杠 / 供网络使用
            rel_path = os.path.relpath(file_path, ".").replace('\\', '/')

            print(f"正在计算指纹: {rel_path} ...", end="")
            md5_hash = calculate_md5(file_path)
            manifest["files"][rel_path] = {"md5": md5_hash}
            print(" [完成]")

    # 写入 json 文件
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

    print(f"\n✅ manifest.json 生成成功！共纯净扫描 {len(manifest['files'])} 个文件。")
    print("注意：如果文件数量依然超过 1000，建议删掉 translations 文件夹里不需要的国外语言包。")
    input("按回车键退出...")

if __name__ == "__main__":
    generate_manifest()