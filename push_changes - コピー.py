# -*- coding: utf-8 -*-
"""
ステップ2: PNG_clone (gitリポジトリ) 内の変更を commit & push する。
ファイルコピーは一切行わない。git操作のみ。

毎時40分にタスクスケジューラから実行する想定。
mirror_png.py (毎時35分) の後に実行することで、
コピーが完了してから安全にpushできるようにする。
"""

import subprocess
from pathlib import Path
from datetime import datetime

# ============ 設定項目 ============

# gitリポジトリの場所
REPO_DIR = Path(r"C:\Users\gutti\Desktop\Python\PNG_clone")

# push先のブランチ名
BRANCH = "main"

# gitコマンドの実行ファイル。"FileNotFoundError"が出る場合はフルパスに変更する
# 例: GIT_EXE = r"C:\Program Files\Git\cmd\git.exe"
GIT_EXE = "git"

# ログファイル (スクリプトと同じフォルダに作成)
LOG_FILE = Path(__file__).parent / "push_log.txt"

# ===================================


def log(msg: str) -> None:
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def run_git(args, cwd: Path):
    result = subprocess.run(
        [GIT_EXE] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def main() -> int:
    if not (REPO_DIR / ".git").exists():
        log(f"エラー: {REPO_DIR} はgitリポジトリではありません。")
        return 1

    try:
        status = run_git(["status", "--porcelain"], cwd=REPO_DIR)
        if not status:
            # ローカルに変更がなければ、リモートの変更だけ取り込んで終了
            run_git(["pull", "--rebase", "origin", BRANCH], cwd=REPO_DIR)
            log("差分がありませんでした（commit不要）。")
            return 0

        # 先にローカルの変更をcommitしてから、リモートの変更を取り込む
        run_git(["add", "-A"], cwd=REPO_DIR)
        commit_msg = f"Auto upload PNGs: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        run_git(["commit", "-m", commit_msg], cwd=REPO_DIR)
        run_git(["pull", "--rebase", "origin", BRANCH], cwd=REPO_DIR)
        run_git(["push", "origin", BRANCH], cwd=REPO_DIR)
        log("push完了しました。")
    except RuntimeError as e:
        log(f"エラー: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
