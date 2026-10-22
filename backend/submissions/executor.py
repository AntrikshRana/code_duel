import os
import sys
import time
import subprocess
import tempfile
from django.utils import timezone

def run_isolated_code(language, code, input_data, time_limit_sec=2.0):
    """
    Executes user code in a temporary isolated subprocess with input and strict timeout.
    Returns: dict(verdict, output, error, execution_time_ms)
    """
    start_time = time.time()
    temp_dir = tempfile.mkdtemp(prefix="codeduel_")
    
    try:
        if language == 'python':
            script_path = os.path.join(temp_dir, "solution.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            cmd = [sys.executable, script_path]
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=temp_dir
            )
            try:
                stdout, stderr = process.communicate(input=input_data, timeout=time_limit_sec)
                exec_time_ms = round((time.time() - start_time) * 1000, 2)
                
                if process.returncode != 0:
                    return {
                        "verdict": "RUNTIME_ERROR",
                        "output": stdout,
                        "error": stderr,
                        "time_ms": exec_time_ms
                    }
                return {
                    "verdict": "SUCCESS",
                    "output": stdout,
                    "error": stderr,
                    "time_ms": exec_time_ms
                }
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    "verdict": "TIME_LIMIT_EXCEEDED",
                    "output": "",
                    "error": f"Execution timed out (> {time_limit_sec}s)",
                    "time_ms": int(time_limit_sec * 1000)
                }

        elif language == 'javascript':
            script_path = os.path.join(temp_dir, "solution.js")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            cmd = ["node", script_path]
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=temp_dir
            )
            try:
                stdout, stderr = process.communicate(input=input_data, timeout=time_limit_sec)
                exec_time_ms = round((time.time() - start_time) * 1000, 2)
                if process.returncode != 0:
                    return {"verdict": "RUNTIME_ERROR", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
                return {"verdict": "SUCCESS", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
            except subprocess.TimeoutExpired:
                process.kill()
                return {"verdict": "TIME_LIMIT_EXCEEDED", "output": "", "error": f"Execution timed out (> {time_limit_sec}s)", "time_ms": int(time_limit_sec * 1000)}

        elif language == 'cpp':
            cpp_path = os.path.join(temp_dir, "solution.cpp")
            exe_path = os.path.join(temp_dir, "solution.exe" if os.name == 'nt' else "solution")
            with open(cpp_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Compile step
            compile_cmd = ["g++", "-O2", cpp_path, "-o", exe_path]
            try:
                compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
                if compile_proc.returncode != 0:
                    return {
                        "verdict": "COMPILATION_ERROR",
                        "output": "",
                        "error": compile_proc.stderr,
                        "time_ms": 0
                    }
            except FileNotFoundError:
                return {
                    "verdict": "RUNTIME_ERROR",
                    "output": "",
                    "error": "C++ compiler (g++) not installed on server host.",
                    "time_ms": 0
                }

            # Run compiled binary
            run_proc = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=temp_dir
            )
            try:
                stdout, stderr = run_proc.communicate(input=input_data, timeout=time_limit_sec)
                exec_time_ms = round((time.time() - start_time) * 1000, 2)
                if run_proc.returncode != 0:
                    return {"verdict": "RUNTIME_ERROR", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
                return {"verdict": "SUCCESS", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
            except subprocess.TimeoutExpired:
                run_proc.kill()
                return {"verdict": "TIME_LIMIT_EXCEEDED", "output": "", "error": "Execution timed out", "time_ms": int(time_limit_sec * 1000)}

        elif language == 'c':
            c_path = os.path.join(temp_dir, "solution.c")
            exe_path = os.path.join(temp_dir, "solution.exe" if os.name == 'nt' else "solution")
            with open(c_path, "w", encoding="utf-8") as f:
                f.write(code)

            compile_cmd = ["gcc", "-O2", c_path, "-o", exe_path]
            try:
                compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
                if compile_proc.returncode != 0:
                    return {"verdict": "COMPILATION_ERROR", "output": "", "error": compile_proc.stderr, "time_ms": 0}
            except FileNotFoundError:
                return {"verdict": "RUNTIME_ERROR", "output": "", "error": "C compiler (gcc) not available.", "time_ms": 0}

            run_proc = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=temp_dir)
            try:
                stdout, stderr = run_proc.communicate(input=input_data, timeout=time_limit_sec)
                exec_time_ms = round((time.time() - start_time) * 1000, 2)
                if run_proc.returncode != 0:
                    return {"verdict": "RUNTIME_ERROR", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
                return {"verdict": "SUCCESS", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
            except subprocess.TimeoutExpired:
                run_proc.kill()
                return {"verdict": "TIME_LIMIT_EXCEEDED", "output": "", "error": "Execution timed out", "time_ms": int(time_limit_sec * 1000)}

        elif language == 'java':
            java_path = os.path.join(temp_dir, "Solution.java")
            with open(java_path, "w", encoding="utf-8") as f:
                f.write(code)

            compile_cmd = ["javac", java_path]
            try:
                compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=12)
                if compile_proc.returncode != 0:
                    return {"verdict": "COMPILATION_ERROR", "output": "", "error": compile_proc.stderr, "time_ms": 0}
            except FileNotFoundError:
                return {"verdict": "RUNTIME_ERROR", "output": "", "error": "Java compiler (javac) not available.", "time_ms": 0}

            run_proc = subprocess.Popen(["java", "Solution"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=temp_dir)
            try:
                stdout, stderr = run_proc.communicate(input=input_data, timeout=time_limit_sec + 1.0)
                exec_time_ms = round((time.time() - start_time) * 1000, 2)
                if run_proc.returncode != 0:
                    return {"verdict": "RUNTIME_ERROR", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
                return {"verdict": "SUCCESS", "output": stdout, "error": stderr, "time_ms": exec_time_ms}
            except subprocess.TimeoutExpired:
                run_proc.kill()
                return {"verdict": "TIME_LIMIT_EXCEEDED", "output": "", "error": "Execution timed out", "time_ms": int((time_limit_sec + 1.0) * 1000)}

        else:
            return {"verdict": "COMPILATION_ERROR", "output": "", "error": f"Unsupported language: {language}", "time_ms": 0}

    except Exception as e:
        return {"verdict": "RUNTIME_ERROR", "output": "", "error": str(e), "time_ms": 0}
    finally:
        # Cleanup temp directory
        try:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


def execute_submission(submission):
    """
    Evaluates a submission against all problem test cases (samples and hidden).
    Updates submission verdict, passed counts, and battle state if applicable.
    """
    problem = submission.problem
    test_cases = list(problem.test_cases.all().order_by('order', 'id'))
    
    if not test_cases:
        submission.verdict = 'ACCEPTED'
        submission.test_cases_passed = 0
        submission.total_test_cases = 0
        submission.save()
        return submission

    submission.total_test_cases = len(test_cases)
    passed_count = 0
    max_time_ms = 0.0

    for idx, tc in enumerate(test_cases):
        res = run_isolated_code(
            language=submission.language,
            code=submission.code,
            input_data=tc.input_data,
            time_limit_sec=problem.time_limit_sec
        )

        max_time_ms = max(max_time_ms, res.get("time_ms", 0.0))

        if res["verdict"] != "SUCCESS":
            submission.verdict = res["verdict"]
            submission.test_cases_passed = passed_count
            submission.execution_time_ms = max_time_ms
            submission.error_output = res.get("error", "")
            submission.save()
            return submission

        # Compare outputs
        user_out = res["output"].strip().replace('\r\n', '\n')
        expected = tc.expected_output.strip().replace('\r\n', '\n')

        if user_out != expected:
            submission.verdict = "WRONG_ANSWER"
            submission.test_cases_passed = passed_count
            submission.execution_time_ms = max_time_ms
            if not tc.is_hidden:
                submission.error_output = f"Sample Test Case #{idx + 1} Failed:\nExpected:\n{expected}\n\nGot:\n{user_out}"
            else:
                submission.error_output = f"Hidden Test Case #{idx + 1} Failed."
            submission.save()
            return submission

        passed_count += 1

    # All tests passed!
    submission.verdict = "ACCEPTED"
    submission.test_cases_passed = passed_count
    submission.execution_time_ms = max_time_ms
    submission.error_output = "All test cases passed successfully!"
    submission.save()

    # Check battle win conditions
    if submission.battle and submission.battle.status in ['IN_PROGRESS', 'COUNTDOWN']:
        battle = submission.battle
        now = timezone.now()
        is_p1 = (submission.user == battle.player1)
        is_p2 = (submission.user == battle.player2)

        if is_p1 and not battle.player1_solved_at:
            battle.player1_solved_at = now
        elif is_p2 and not battle.player2_solved_at:
            battle.player2_solved_at = now

        # Determine winner if no winner set yet
        if not battle.winner:
            battle.winner = submission.user
            battle.status = 'COMPLETED'
            battle.end_time = now
            
            # Complexity & Performance points formula
            diff = problem.difficulty.upper()
            base_points = 25 if diff == 'EASY' else (45 if diff == 'MEDIUM' else 70)
            
            # Time complexity execution speed bonus (lower runtime_ms indicates optimal time complexity)
            if max_time_ms < 40:
                comp_bonus = 25 # Highly optimal O(1) / O(N)
            elif max_time_ms < 120:
                comp_bonus = 15 # Efficient O(N log N)
            elif max_time_ms < 250:
                comp_bonus = 8  # Moderate
            else:
                comp_bonus = 4

            total_gain = base_points + comp_bonus
            battle.winner_points_gained = total_gain
            battle.complexity_bonus = comp_bonus

            # Update user ratings
            winner_prof = submission.user.profile
            winner_prof.rating += total_gain
            winner_prof.wins += 1
            winner_prof.save()

            opponent = battle.player2 if is_p1 else battle.player1
            if opponent:
                opp_prof = opponent.profile
                penalty = 12 if diff == 'EASY' else (18 if diff == 'MEDIUM' else 24)
                opp_prof.rating = max(0, opp_prof.rating - penalty)
                opp_prof.losses += 1
                opp_prof.save()

        battle.save()

    return submission
