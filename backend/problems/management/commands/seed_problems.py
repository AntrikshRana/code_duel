from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from problems.models import Problem, TestCase

class Command(BaseCommand):
    help = 'Seeds initial competitive programming problems and test cases'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Code Duel problems...")

        # 1. Two Sum
        two_sum, _ = Problem.objects.get_or_create(
            title="Two Sum",
            defaults={
                "difficulty": "EASY",
                "description": (
                    "Given an array of integers `nums` and an integer `target`, return the 0-indexed positions "
                    "of the two numbers such that they add up to `target`.\n\n"
                    "You may assume that each input would have exactly one solution, and you may not use the same element twice.\n\n"
                    "**Input format:**\n"
                    "Line 1: space-separated integers representing `nums`\n"
                    "Line 2: single integer representing `target`\n\n"
                    "**Output format:**\n"
                    "Output two space-separated indices in ascending order."
                ),
                "input_format": "nums (space separated integers)\ntarget (integer)",
                "output_format": "idx1 idx2",
                "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\nOnly one valid answer exists.",
                "starter_code_python": "import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if not lines:\n        return\n    nums = list(map(int, lines[0].split()))\n    target = int(lines[1].strip())\n    \n    lookup = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in lookup:\n            print(f\"{lookup[diff]} {i}\")\n            return\n        lookup[num] = i\n\nif __name__ == '__main__':\n    solve()\n",
                "starter_code_cpp": "#include <iostream>\n#include <vector>\n#include <sstream>\n#include <unordered_map>\nusing namespace std;\n\nint main() {\n    string line;\n    if (!getline(cin, line)) return 0;\n    stringstream ss(line);\n    vector<int> nums;\n    int val;\n    while (ss >> val) nums.push_back(val);\n    int target;\n    if (!(cin >> target)) return 0;\n    \n    unordered_map<int, int> seen;\n    for (int i = 0; i < nums.size(); i++) {\n        int diff = target - nums[i];\n        if (seen.count(diff)) {\n            cout << seen[diff] << \" \" << i << endl;\n            return 0;\n        }\n        seen[nums[i]] = i;\n    }\n    return 0;\n}\n",
                "starter_code_javascript": "const fs = require('fs');\n\nfunction solve() {\n    const input = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n    if (input.length < 2) return;\n    const nums = input[0].trim().split(/\\s+/).map(Number);\n    const target = Number(input[1].trim());\n    \n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const diff = target - nums[i];\n        if (map.has(diff)) {\n            console.log(`${map.get(diff)} ${i}`);\n            return;\n        }\n        map.set(nums[i], i);\n    }\n}\nsolve();\n"
            }
        )
        
        # Test cases for Two Sum
        TestCase.objects.get_or_create(
            problem=two_sum,
            input_data="2 7 11 15\n9",
            expected_output="0 1",
            is_hidden=False,
            order=1
        )
        TestCase.objects.get_or_create(
            problem=two_sum,
            input_data="3 2 4\n6",
            expected_output="1 2",
            is_hidden=False,
            order=2
        )
        TestCase.objects.get_or_create(
            problem=two_sum,
            input_data="3 3\n6",
            expected_output="0 1",
            is_hidden=True,
            order=3
        )
        TestCase.objects.get_or_create(
            problem=two_sum,
            input_data="1 5 8 10 14 20\n24",
            expected_output="3 4",
            is_hidden=True,
            order=4
        )

        # 2. Valid Parentheses
        val_par, _ = Problem.objects.get_or_create(
            title="Valid Parentheses",
            defaults={
                "difficulty": "EASY",
                "description": (
                    "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\n"
                    "An input string is valid if:\n"
                    "1. Open brackets must be closed by the same type of brackets.\n"
                    "2. Open brackets must be closed in the correct order.\n"
                    "3. Every close bracket has a corresponding open bracket of the same type.\n\n"
                    "**Output format:**\n"
                    "Print `true` if valid, or `false` otherwise."
                ),
                "input_format": "A single line containing the string `s`",
                "output_format": "true or false",
                "constraints": "1 <= s.length <= 10^4",
                "starter_code_python": "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    \n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                print('false')\n                return\n        else:\n            stack.append(char)\n            \n    print('true' if not stack else 'false')\n\nif __name__ == '__main__':\n    solve()\n",
                "starter_code_cpp": "#include <iostream>\n#include <string>\n#include <stack>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!(cin >> s)) return 0;\n    stack<char> st;\n    for (char c : s) {\n        if (c == '(' || c == '{' || c == '[') {\n            st.push(c);\n        } else {\n            if (st.empty()) { cout << \"false\" << endl; return 0; }\n            char top = st.top(); st.pop();\n            if (c == ')' && top != '(') { cout << \"false\" << endl; return 0; }\n            if (c == '}' && top != '{') { cout << \"false\" << endl; return 0; }\n            if (c == ']' && top != '[') { cout << \"false\" << endl; return 0; }\n        }\n    }\n    cout << (st.empty() ? \"true\" : \"false\") << endl;\n    return 0;\n}\n",
                "starter_code_javascript": "const fs = require('fs');\n\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').trim();\n    const stack = [];\n    const map = { ')': '(', '}': '{', ']': '[' };\n    for (const char of s) {\n        if (map[char]) {\n            if (stack.pop() !== map[char]) {\n                console.log('false');\n                return;\n            }\n        } else {\n            stack.push(char);\n        }\n    }\n    console.log(stack.length === 0 ? 'true' : 'false');\n}\nsolve();\n"
            }
        )
        TestCase.objects.get_or_create(problem=val_par, input_data="()", expected_output="true", is_hidden=False, order=1)
        TestCase.objects.get_or_create(problem=val_par, input_data="()[]{}", expected_output="true", is_hidden=False, order=2)
        TestCase.objects.get_or_create(problem=val_par, input_data="(]", expected_output="false", is_hidden=False, order=3)
        TestCase.objects.get_or_create(problem=val_par, input_data="([{}])", expected_output="true", is_hidden=True, order=4)
        TestCase.objects.get_or_create(problem=val_par, input_data="(((((()", expected_output="false", is_hidden=True, order=5)

        # 3. Maximum Subarray (Kadane's Algorithm)
        max_sub, _ = Problem.objects.get_or_create(
            title="Maximum Subarray",
            defaults={
                "difficulty": "MEDIUM",
                "description": (
                    "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.\n\n"
                    "A subarray is a contiguous non-empty sequence of elements within an array.\n\n"
                    "**Input format:**\n"
                    "A single line of space-separated integers.\n\n"
                    "**Output format:**\n"
                    "A single integer representing the maximum sum."
                ),
                "input_format": "Space-separated integers",
                "output_format": "Single integer",
                "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4",
                "starter_code_python": "import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    if not nums: return\n    max_sum = cur_sum = nums[0]\n    for x in nums[1:]:\n        cur_sum = max(x, cur_sum + x)\n        max_sum = max(max_sum, cur_sum)\n    print(max_sum)\n\nif __name__ == '__main__':\n    solve()\n",
                "starter_code_cpp": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int val;\n    vector<int> nums;\n    while (cin >> val) nums.push_back(val);\n    if (nums.empty()) return 0;\n    int max_s = nums[0], cur_s = nums[0];\n    for (size_t i = 1; i < nums.size(); i++) {\n        cur_s = max(nums[i], cur_s + nums[i]);\n        max_s = max(max_s, cur_s);\n    }\n    cout << max_s << endl;\n    return 0;\n}\n",
                "starter_code_javascript": "const fs = require('fs');\nfunction solve() {\n    const nums = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\n    if (!nums.length) return;\n    let maxSum = nums[0];\n    let curSum = nums[0];\n    for (let i = 1; i < nums.length; i++) {\n        curSum = Math.max(nums[i], curSum + nums[i]);\n        maxSum = Math.max(maxSum, curSum);\n    }\n    console.log(maxSum);\n}\nsolve();\n"
            }
        )
        TestCase.objects.get_or_create(problem=max_sub, input_data="-2 1 -3 4 -1 2 1 -5 4", expected_output="6", is_hidden=False, order=1)
        TestCase.objects.get_or_create(problem=max_sub, input_data="1", expected_output="1", is_hidden=False, order=2)
        TestCase.objects.get_or_create(problem=max_sub, input_data="5 4 -1 7 8", expected_output="23", is_hidden=True, order=3)
        TestCase.objects.get_or_create(problem=max_sub, input_data="-5 -3 -1 -2", expected_output="-1", is_hidden=True, order=4)

        # Create demo users for testing & leaderboard
        u1, created = User.objects.get_or_create(username="algo_master", email="master@codeduel.com")
        if created:
            u1.set_password("password123")
            u1.save()
            u1.profile.rating = 1580
            u1.profile.wins = 28
            u1.profile.losses = 4
            u1.profile.bio = "C++ Grandmaster & Graph Theory enthusiast."
            u1.profile.save()

        u2, created = User.objects.get_or_create(username="py_ninja", email="ninja@codeduel.com")
        if created:
            u2.set_password("password123")
            u2.save()
            u2.profile.rating = 1420
            u2.profile.wins = 19
            u2.profile.losses = 9
            u2.profile.bio = "Fastest Python one-liner builder."
            u2.profile.save()

        u3, created = User.objects.get_or_create(username="code_gladiator", email="gladiator@codeduel.com")
        if created:
            u3.set_password("password123")
            u3.save()
            u3.profile.rating = 1350
            u3.profile.wins = 12
            u3.profile.losses = 7
            u3.profile.bio = "Ready for any 1v1 contest."
            u3.profile.save()

        self.stdout.write(self.style.SUCCESS("Successfully seeded problems, test cases, and demo users!"))
