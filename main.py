"""Git 변경 사항을 수집해 AI 커밋/PR 초안 생성의 재료로 쓰는 도구 (2단계: 변경 사항 수집)."""

import subprocess
import sys


def run_git(args):
    """git 명령을 실행하고 표준 출력 글자를 돌려준다. 실패하면 원인을 담아 종료한다."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError:
        print("[ERROR] git 명령을 찾을 수 없습니다. Git이 설치되어 있는지 확인하세요.")
        sys.exit(1)

    if result.returncode != 0:
        print(f"[ERROR] git {' '.join(args)} 실행 실패: {result.stderr.strip()}")
        sys.exit(1)

    return result.stdout


def collect_git_changes():
    """변경된 파일 목록(status)과 변경 내용(diff)을 수집한다. 변경이 없으면 None."""
    status = run_git(["status", "--porcelain"])
    if not status.strip():
        return None

    # HEAD 기준 diff: 커밋 전에 add 한 변경(staged)과 add 안 한 변경(unstaged)을 모두 포함한다.
    diff = run_git(["diff", "HEAD"])

    changed_files = status.splitlines()
    print(f"[INFO] Git status 수집 완료: {len(changed_files)}개 파일 변경 감지")
    print(f"[INFO] Git diff 수집 완료: {len(diff.splitlines())}줄")
    return {"status": status, "diff": diff}


def main():
    changes = collect_git_changes()
    if changes is None:
        print("[INFO] 변경 사항이 없습니다. 종료합니다.")
        return

    # 3단계부터는 이 changes를 AI API로 보낸다. 지금은 수집 결과만 확인한다.
    print("--- git status ---")
    print(changes["status"])


if __name__ == "__main__":
    main()
