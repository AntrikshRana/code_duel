from django.core.management.base import BaseCommand
from problems.models import Problem, TestCase

class Command(BaseCommand):
    help = 'Seeds initial competitive programming problems and test cases'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Code Duel problems and test cases...")

        # Clear existing problems to allow clean refresh
        Problem.objects.all().delete()

        # ==========================================
        # 1. TWO SUM (EASY)
        # ==========================================
        two_sum = Problem.objects.create(
            title="Two Sum",
            difficulty="EASY",
            description=(
                "Given an array of integers `nums` and an integer `target`, return the 0-indexed positions "
                "of the two numbers such that they add up to `target`.\n\n"
                "You may assume that each input has exactly one solution, and you may not use the same element twice.\n\n"
                "**Input format:**\n"
                "Line 1: space-separated integers representing `nums`\n"
                "Line 2: single integer representing `target`\n\n"
                "**Output format:**\n"
                "Output two space-separated indices in ascending order."
            ),
            input_format="Line 1: nums (space-separated integers)\nLine 2: target (integer)",
            output_format="idx1 idx2",
            constraints="2 <= nums.length <= 10^5\n-10^9 <= nums[i] <= 10^9\nExactly one valid solution exists.",
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if not lines:\n        return\n    nums = list(map(int, lines[0].split()))\n    target = int(lines[1].strip())\n    \n    lookup = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in lookup:\n            print(f\"{lookup[diff]} {i}\")\n            return\n        lookup[num] = i\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\n#include <unordered_map>\nusing namespace std;\n\nint main() {\n    string line;\n    if (!getline(cin, line)) return 0;\n    stringstream ss(line);\n    vector<int> nums;\n    int val;\n    while (ss >> val) nums.push_back(val);\n    int target;\n    if (!(cin >> target)) return 0;\n    \n    unordered_map<int, int> seen;\n    for (int i = 0; i < (int)nums.size(); i++) {\n        int diff = target - nums[i];\n        if (seen.count(diff)) {\n            cout << seen[diff] << \" \" << i << endl;\n            return 0;\n        }\n        seen[nums[i]] = i;\n    }\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const input = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n    if (input.length < 2) return;\n    const nums = input[0].trim().split(/\\s+/).map(Number);\n    const target = Number(input[1].trim());\n    \n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const diff = target - nums[i];\n        if (map.has(diff)) {\n            console.log(`${map.get(diff)} ${i}`);\n            return;\n        }\n        map.set(nums[i], i);\n    }\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=two_sum, input_data="2 7 11 15\n9", expected_output="0 1", is_hidden=False, order=1)
        TestCase.objects.create(problem=two_sum, input_data="3 2 4\n6", expected_output="1 2", is_hidden=False, order=2)
        TestCase.objects.create(problem=two_sum, input_data="3 3\n6", expected_output="0 1", is_hidden=True, order=3)
        TestCase.objects.create(problem=two_sum, input_data="1 5 8 10 14 20\n24", expected_output="3 4", is_hidden=True, order=4)
        TestCase.objects.create(problem=two_sum, input_data="-10 -5 0 5 10\n0", expected_output="1 3", is_hidden=True, order=5)

        # ==========================================
        # 2. VALID PARENTHESES (EASY)
        # ==========================================
        val_par = Problem.objects.create(
            title="Valid Parentheses",
            difficulty="EASY",
            description=(
                "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\n"
                "An input string is valid if:\n"
                "1. Open brackets are closed by the same type of brackets.\n"
                "2. Open brackets are closed in the correct order.\n"
                "3. Every close bracket has a matching open bracket.\n\n"
                "**Output format:**\n"
                "Print `true` if valid, or `false` otherwise."
            ),
            input_format="A single line containing string s",
            output_format="true or false",
            constraints="1 <= s.length <= 10^5\ns consists of parentheses only '()[]{}'.",
            starter_code_python="import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                print('false')\n                return\n        else:\n            stack.append(char)\n    print('true' if not stack else 'false')\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <stack>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!(cin >> s)) return 0;\n    stack<char> st;\n    for (char c : s) {\n        if (c == '(' || c == '{' || c == '[') st.push(c);\n        else {\n            if (st.empty()) { cout << \"false\" << endl; return 0; }\n            char top = st.top(); st.pop();\n            if (c == ')' && top != '(') { cout << \"false\" << endl; return 0; }\n            if (c == '}' && top != '{') { cout << \"false\" << endl; return 0; }\n            if (c == ']' && top != '[') { cout << \"false\" << endl; return 0; }\n        }\n    }\n    cout << (st.empty() ? \"true\" : \"false\") << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').trim();\n    const stack = [];\n    const map = { ')': '(', '}': '{', ']': '[' };\n    for (const char of s) {\n        if (map[char]) {\n            if (stack.pop() !== map[char]) {\n                console.log('false');\n                return;\n            }\n        } else stack.push(char);\n    }\n    console.log(stack.length === 0 ? 'true' : 'false');\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=val_par, input_data="()", expected_output="true", is_hidden=False, order=1)
        TestCase.objects.create(problem=val_par, input_data="()[]{}", expected_output="true", is_hidden=False, order=2)
        TestCase.objects.create(problem=val_par, input_data="(]", expected_output="false", is_hidden=False, order=3)
        TestCase.objects.create(problem=val_par, input_data="([{}])", expected_output="true", is_hidden=True, order=4)
        TestCase.objects.create(problem=val_par, input_data="(((((()", expected_output="false", is_hidden=True, order=5)
        TestCase.objects.create(problem=val_par, input_data="}{", expected_output="false", is_hidden=True, order=6)

        # ==========================================
        # 3. PALINDROME NUMBER (EASY)
        # ==========================================
        pal = Problem.objects.create(
            title="Palindrome Number",
            difficulty="EASY",
            description=(
                "Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.\n\n"
                "An integer is a palindrome when it reads the same backward as forward."
            ),
            input_format="A single integer x",
            output_format="true or false",
            constraints="-2^31 <= x <= 2^31 - 1",
            starter_code_python="import sys\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw: return\n    print('true' if raw == raw[::-1] else 'false')\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    string s;\n    if (cin >> s) {\n        string rev = string(s.rbegin(), s.rend());\n        cout << (s == rev ? \"true\" : \"false\") << endl;\n    }\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst s = fs.readFileSync(0, 'utf-8').trim();\nconst rev = s.split('').reverse().join('');\nconsole.log(s === rev ? 'true' : 'false');\n"
        )
        TestCase.objects.create(problem=pal, input_data="121", expected_output="true", is_hidden=False, order=1)
        TestCase.objects.create(problem=pal, input_data="-121", expected_output="false", is_hidden=False, order=2)
        TestCase.objects.create(problem=pal, input_data="10", expected_output="false", is_hidden=False, order=3)
        TestCase.objects.create(problem=pal, input_data="1234321", expected_output="true", is_hidden=True, order=4)
        TestCase.objects.create(problem=pal, input_data="0", expected_output="true", is_hidden=True, order=5)

        # ==========================================
        # 4. BEST TIME TO BUY AND SELL STOCK (EASY)
        # ==========================================
        stock = Problem.objects.create(
            title="Best Time to Buy and Sell Stock",
            difficulty="EASY",
            description=(
                "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\n"
                "You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\n"
                "Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0."
            ),
            input_format="Space-separated integers representing stock prices",
            output_format="A single integer representing maximum profit",
            constraints="1 <= prices.length <= 10^5\n0 <= prices[i] <= 10^4",
            starter_code_python="import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    if not nums: return\n    min_p = nums[0]\n    max_prof = 0\n    for p in nums[1:]:\n        max_prof = max(max_prof, p - min_p)\n        min_p = min(min_p, p)\n    print(max_prof)\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int p;\n    vector<int> prices;\n    while (cin >> p) prices.push_back(p);\n    if (prices.empty()) return 0;\n    int min_p = prices[0], max_prof = 0;\n    for (size_t i = 1; i < prices.size(); i++) {\n        max_prof = max(max_prof, prices[i] - min_p);\n        min_p = min(min_p, prices[i]);\n    }\n    cout << max_prof << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst p = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\nif (!p.length) process.exit(0);\nlet minP = p[0], maxProf = 0;\nfor (let i = 1; i < p.length; i++) {\n    maxProf = Math.max(maxProf, p[i] - minP);\n    minP = Math.min(minP, p[i]);\n}\nconsole.log(maxProf);\n"
        )
        TestCase.objects.create(problem=stock, input_data="7 1 5 3 6 4", expected_output="5", is_hidden=False, order=1)
        TestCase.objects.create(problem=stock, input_data="7 6 4 3 1", expected_output="0", is_hidden=False, order=2)
        TestCase.objects.create(problem=stock, input_data="2 4 1", expected_output="2", is_hidden=True, order=3)
        TestCase.objects.create(problem=stock, input_data="3 3 5 0 0 3 1 4", expected_output="4", is_hidden=True, order=4)
        TestCase.objects.create(problem=stock, input_data="1 2", expected_output="1", is_hidden=True, order=5)

        # ==========================================
        # 5. MAXIMUM SUBARRAY - KADANE'S (MEDIUM)
        # ==========================================
        max_sub = Problem.objects.create(
            title="Maximum Subarray",
            difficulty="MEDIUM",
            description=(
                "Given an integer array `nums`, find the contiguous subarray with the largest sum, and return its sum.\n\n"
                "A subarray is a contiguous non-empty sequence of elements within an array."
            ),
            input_format="Space-separated integers",
            output_format="A single integer representing the maximum subarray sum",
            constraints="1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4",
            starter_code_python="import sys\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    if not nums: return\n    max_s = cur_s = nums[0]\n    for x in nums[1:]:\n        cur_s = max(x, cur_s + x)\n        max_s = max(max_s, cur_s)\n    print(max_s)\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int val;\n    vector<int> nums;\n    while (cin >> val) nums.push_back(val);\n    if (nums.empty()) return 0;\n    int max_s = nums[0], cur_s = nums[0];\n    for (size_t i = 1; i < nums.size(); i++) {\n        cur_s = max(nums[i], cur_s + nums[i]);\n        max_s = max(max_s, cur_s);\n    }\n    cout << max_s << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst nums = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\nif (!nums.length) process.exit(0);\nlet maxS = nums[0], curS = nums[0];\nfor (let i = 1; i < nums.length; i++) {\n    curS = Math.max(nums[i], curS + nums[i]);\n    maxS = Math.max(maxS, curS);\n}\nconsole.log(maxS);\n"
        )
        TestCase.objects.create(problem=max_sub, input_data="-2 1 -3 4 -1 2 1 -5 4", expected_output="6", is_hidden=False, order=1)
        TestCase.objects.create(problem=max_sub, input_data="1", expected_output="1", is_hidden=False, order=2)
        TestCase.objects.create(problem=max_sub, input_data="5 4 -1 7 8", expected_output="23", is_hidden=True, order=3)
        TestCase.objects.create(problem=max_sub, input_data="-5 -3 -1 -2", expected_output="-1", is_hidden=True, order=4)
        TestCase.objects.create(problem=max_sub, input_data="-2 -1", expected_output="-1", is_hidden=True, order=5)

        # ==========================================
        # 6. CONTAINER WITH MOST WATER (MEDIUM)
        # ==========================================
        water = Problem.objects.create(
            title="Container With Most Water",
            difficulty="MEDIUM",
            description=(
                "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.\n\n"
                "Find two lines that together with the x-axis form a container, such that the container contains the most water.\n\n"
                "Return the maximum amount of water a container can store."
            ),
            input_format="Space-separated integers representing heights",
            output_format="A single integer representing maximum area",
            constraints="2 <= n <= 10^5\n0 <= height[i] <= 10^4",
            starter_code_python="import sys\ndef solve():\n    h = list(map(int, sys.stdin.read().split()))\n    if not h: return\n    l, r = 0, len(h) - 1\n    max_w = 0\n    while l < r:\n        max_w = max(max_w, min(h[l], h[r]) * (r - l))\n        if h[l] < h[r]: l += 1\n        else: r -= 1\n    print(max_w)\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nint main() {\n    int val;\n    vector<int> h;\n    while (cin >> val) h.push_back(val);\n    int l = 0, r = h.size() - 1, max_w = 0;\n    while (l < r) {\n        max_w = max(max_w, min(h[l], h[r]) * (r - l));\n        if (h[l] < h[r]) l++; else r--;\n    }\n    cout << max_w << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst h = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\nlet l = 0, r = h.length - 1, maxW = 0;\nwhile (l < r) {\n    maxW = Math.max(maxW, Math.min(h[l], h[r]) * (r - l));\n    if (h[l] < h[r]) l++; else r--;\n}\nconsole.log(maxW);\n"
        )
        TestCase.objects.create(problem=water, input_data="1 8 6 2 5 4 8 3 7", expected_output="49", is_hidden=False, order=1)
        TestCase.objects.create(problem=water, input_data="1 1", expected_output="1", is_hidden=False, order=2)
        TestCase.objects.create(problem=water, input_data="4 3 2 1 4", expected_output="16", is_hidden=True, order=3)
        TestCase.objects.create(problem=water, input_data="1 2 1", expected_output="2", is_hidden=True, order=4)
        TestCase.objects.create(problem=water, input_data="1 8 100 2 100 4 8 3 7", expected_output="200", is_hidden=True, order=5)

        # ==========================================
        # 7. LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS (MEDIUM)
        # ==========================================
        substr = Problem.objects.create(
            title="Longest Substring Without Repeating Characters",
            difficulty="MEDIUM",
            description=(
                "Given a string `s`, find the length of the longest substring without repeating characters."
            ),
            input_format="A single line containing string s",
            output_format="A single integer representing the length",
            constraints="0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.",
            starter_code_python="import sys\ndef solve():\n    s = sys.stdin.read().strip()\n    seen = {}\n    max_len = l = 0\n    for r, ch in enumerate(s):\n        if ch in seen and seen[ch] >= l:\n            l = seen[ch] + 1\n        seen[ch] = r\n        max_len = max(max_len, r - l + 1)\n    print(max_len)\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <unordered_map>\n#include <algorithm>\nusing namespace std;\nint main() {\n    string s;\n    if (!getline(cin, s)) { cout << 0 << endl; return 0; }\n    unordered_map<char, int> seen;\n    int max_len = 0, l = 0;\n    for (int r = 0; r < (int)s.size(); r++) {\n        if (seen.count(s[r]) && seen[s[r]] >= l) l = seen[s[r]] + 1;\n        seen[s[r]] = r;\n        max_len = max(max_len, r - l + 1);\n    }\n    cout << max_len << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst s = fs.readFileSync(0, 'utf-8').trim();\nlet seen = new Map(), maxLen = 0, l = 0;\nfor (let r = 0; r < s.length; r++) {\n    if (seen.has(s[r]) && seen.get(s[r]) >= l) l = seen.get(s[r]) + 1;\n    seen.set(s[r], r);\n    maxLen = Math.max(maxLen, r - l + 1);\n}\nconsole.log(maxLen);\n"
        )
        TestCase.objects.create(problem=substr, input_data="abcabcbb", expected_output="3", is_hidden=False, order=1)
        TestCase.objects.create(problem=substr, input_data="bbbbb", expected_output="1", is_hidden=False, order=2)
        TestCase.objects.create(problem=substr, input_data="pwwkew", expected_output="3", is_hidden=False, order=3)
        TestCase.objects.create(problem=substr, input_data="au", expected_output="2", is_hidden=True, order=4)
        TestCase.objects.create(problem=substr, input_data="dvdf", expected_output="3", is_hidden=True, order=5)
        TestCase.objects.create(problem=substr, input_data="tmmzuxt", expected_output="5", is_hidden=True, order=6)

        # ==========================================
        # 8. COIN CHANGE (MEDIUM)
        # ==========================================
        coin = Problem.objects.create(
            title="Coin Change",
            difficulty="MEDIUM",
            description=(
                "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\n"
                "Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.\n\n"
                "You may assume that you have an infinite number of each kind of coin.\n\n"
                "**Input format:**\n"
                "Line 1: space-separated integers representing `coins`\n"
                "Line 2: integer `amount`"
            ),
            input_format="Line 1: coins\nLine 2: amount",
            output_format="A single integer",
            constraints="1 <= coins.length <= 12\n1 <= coins[i] <= 2^31 - 1\n0 <= amount <= 10^4",
            starter_code_python="import sys\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if not lines: return\n    coins = list(map(int, lines[0].split()))\n    amount = int(lines[1].strip())\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for c in coins:\n        for x in range(c, amount + 1):\n            dp[x] = min(dp[x], dp[x - c] + 1)\n    print(dp[amount] if dp[amount] != float('inf') else -1)\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\n#include <algorithm>\nusing namespace std;\nint main() {\n    string line;\n    if (!getline(cin, line)) return 0;\n    stringstream ss(line);\n    vector<int> coins;\n    int c;\n    while (ss >> c) coins.push_back(c);\n    int amount;\n    if (!(cin >> amount)) return 0;\n    vector<int> dp(amount + 1, 1e9);\n    dp[0] = 0;\n    for (int coin : coins) {\n        for (int x = coin; x <= amount; x++) dp[x] = min(dp[x], dp[x - coin] + 1);\n    }\n    cout << (dp[amount] >= 1e9 ? -1 : dp[amount]) << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst lines = fs.readFileSync(0, 'utf-8').trim().split('\\n');\nif (lines.length < 2) process.exit(0);\nconst coins = lines[0].trim().split(/\\s+/).map(Number);\nconst amount = Number(lines[1].trim());\nconst dp = new Array(amount + 1).fill(Infinity);\ndp[0] = 0;\nfor (const c of coins) {\n    for (let x = c; x <= amount; x++) dp[x] = Math.min(dp[x], dp[x - c] + 1);\n}\nconsole.log(dp[amount] === Infinity ? -1 : dp[amount]);\n"
        )
        TestCase.objects.create(problem=coin, input_data="1 2 5\n11", expected_output="3", is_hidden=False, order=1)
        TestCase.objects.create(problem=coin, input_data="2\n3", expected_output="-1", is_hidden=False, order=2)
        TestCase.objects.create(problem=coin, input_data="1\n0", expected_output="0", is_hidden=False, order=3)
        TestCase.objects.create(problem=coin, input_data="186 419 83 408\n6249", expected_output="20", is_hidden=True, order=4)
        TestCase.objects.create(problem=coin, input_data="2 5 10 1\n27", expected_output="4", is_hidden=True, order=5)

        # ==========================================
        # 9. TRAPPING RAIN WATER (HARD)
        # ==========================================
        trap = Problem.objects.create(
            title="Trapping Rain Water",
            difficulty="HARD",
            description=(
                "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, "
                "compute how much water it can trap after raining."
            ),
            input_format="Space-separated non-negative integers representing elevation map",
            output_format="A single integer representing trapped water units",
            constraints="n == height.length\n1 <= n <= 2 * 10^5\n0 <= height[i] <= 10^5",
            starter_code_python="import sys\ndef solve():\n    h = list(map(int, sys.stdin.read().split()))\n    if not h: return\n    l, r = 0, len(h) - 1\n    l_max = r_max = water = 0\n    while l < r:\n        if h[l] < h[r]:\n            if h[l] >= l_max: l_max = h[l]\n            else: water += l_max - h[l]\n            l += 1\n        else:\n            if h[r] >= r_max: r_max = h[r]\n            else: water += r_max - h[r]\n            r -= 1\n    print(water)\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    int val;\n    vector<int> h;\n    while (cin >> val) h.push_back(val);\n    int l = 0, r = (int)h.size() - 1;\n    int l_max = 0, r_max = 0, water = 0;\n    while (l < r) {\n        if (h[l] < h[r]) {\n            if (h[l] >= l_max) l_max = h[l];\n            else water += l_max - h[l];\n            l++;\n        } else {\n            if (h[r] >= r_max) r_max = h[r];\n            else water += r_max - h[r];\n            r--;\n        }\n    }\n    cout << water << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst h = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\nlet l = 0, r = h.length - 1, lMax = 0, rMax = 0, water = 0;\nwhile (l < r) {\n    if (h[l] < h[r]) {\n        if (h[l] >= lMax) lMax = h[l];\n        else water += lMax - h[l];\n        l++;\n    } else {\n        if (h[r] >= rMax) rMax = h[r];\n        else water += rMax - h[r];\n        r--;\n    }\n}\nconsole.log(water);\n"
        )
        TestCase.objects.create(problem=trap, input_data="0 1 0 2 1 0 1 3 2 1 2 1", expected_output="6", is_hidden=False, order=1)
        TestCase.objects.create(problem=trap, input_data="4 2 0 3 2 5", expected_output="9", is_hidden=False, order=2)
        TestCase.objects.create(problem=trap, input_data="3 0 2 0 4", expected_output="7", is_hidden=True, order=3)
        TestCase.objects.create(problem=trap, input_data="1 2 3 4 5", expected_output="0", is_hidden=True, order=4)
        TestCase.objects.create(problem=trap, input_data="5 4 1 2", expected_output="1", is_hidden=True, order=5)

        # ==========================================
        # 10. MEDIAN OF TWO SORTED ARRAYS (HARD)
        # ==========================================
        median = Problem.objects.create(
            title="Median of Two Sorted Arrays",
            difficulty="HARD",
            description=(
                "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.\n\n"
                "The overall run time complexity should be `O(log (m+n))`.\n\n"
                "**Input format:**\n"
                "Line 1: space-separated integers representing `nums1`\n"
                "Line 2: space-separated integers representing `nums2`\n\n"
                "**Output format:**\n"
                "Single number formatted with 1 decimal place if fractional, or integer."
            ),
            input_format="Line 1: nums1\nLine 2: nums2",
            output_format="Single number (e.g. 2.0 or 2.5)",
            constraints="nums1.length == m\nnums2.length == n\n0 <= m <= 1000\n0 <= n <= 1000\n1 <= m + n <= 2000",
            starter_code_python="import sys\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    nums1 = list(map(int, lines[0].split())) if len(lines) > 0 and lines[0].strip() else []\n    nums2 = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []\n    arr = sorted(nums1 + nums2)\n    k = len(arr)\n    if k % 2 == 1:\n        print(float(arr[k // 2]))\n    else:\n        val = (arr[k // 2 - 1] + arr[k // 2]) / 2.0\n        print(val)\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\n#include <algorithm>\n#include <iomanip>\nusing namespace std;\nint main() {\n    string l1, l2;\n    vector<int> a;\n    if (getline(cin, l1)) {\n        stringstream ss(l1);\n        int v; while (ss >> v) a.push_back(v);\n    }\n    if (getline(cin, l2)) {\n        stringstream ss(l2);\n        int v; while (ss >> v) a.push_back(v);\n    }\n    sort(a.begin(), a.end());\n    int k = a.size();\n    if (k % 2 == 1) cout << fixed << setprecision(1) << (double)a[k / 2] << endl;\n    else cout << fixed << setprecision(1) << (double)(a[k / 2 - 1] + a[k / 2]) / 2.0 << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nconst lines = fs.readFileSync(0, 'utf-8').trim().split('\\n');\nconst a1 = lines[0] && lines[0].trim() ? lines[0].trim().split(/\\s+/).map(Number) : [];\nconst a2 = lines[1] && lines[1].trim() ? lines[1].trim().split(/\\s+/).map(Number) : [];\nconst arr = a1.concat(a2).sort((x, y) => x - y);\nconst k = arr.length;\nif (k % 2 === 1) console.log(arr[Math.floor(k / 2)].toFixed(1));\nelse console.log(((arr[k / 2 - 1] + arr[k / 2]) / 2).toFixed(1));\n"
        )
        TestCase.objects.create(problem=median, input_data="1 3\n2", expected_output="2.0", is_hidden=False, order=1)
        TestCase.objects.create(problem=median, input_data="1 2\n3 4", expected_output="2.5", is_hidden=False, order=2)
        TestCase.objects.create(problem=median, input_data="0 0\n0 0", expected_output="0.0", is_hidden=True, order=3)
        TestCase.objects.create(problem=median, input_data="\n1", expected_output="1.0", is_hidden=True, order=4)
        TestCase.objects.create(problem=median, input_data="2\n", expected_output="2.0", is_hidden=True, order=5)

        self.stdout.write(self.style.SUCCESS("Successfully seeded 10 comprehensive DSA problems with sample & hidden test cases (No demo accounts)!"))
