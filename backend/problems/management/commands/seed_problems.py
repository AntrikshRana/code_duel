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

        # ==========================================
        # 11. REVERSE STRING (EASY)
        # ==========================================
        rev_str = Problem.objects.create(
            title="Reverse String",
            difficulty="EASY",
            description=(
                "Given a string `s`, return the string reversed.\n\n"
                "**Input format:**\n"
                "A single line containing string `s`.\n\n"
                "**Output format:**\n"
                "The reversed string."
            ),
            input_format="A single line containing string s",
            output_format="Reversed string",
            constraints="1 <= s.length <= 10^5\ns consists of printable ASCII characters.",
            starter_code_python="import sys\n\ndef solve():\n    s = sys.stdin.read().rstrip('\\r\\n')\n    print(s[::-1])\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s;\n    if (getline(cin, s)) {\n        reverse(s.begin(), s.end());\n        cout << s << endl;\n    }\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').replace(/\\r?\\n$/, '');\n    console.log(s.split('').reverse().join(''));\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=rev_str, input_data="hello", expected_output="olleh", is_hidden=False, order=1)
        TestCase.objects.create(problem=rev_str, input_data="algorithm", expected_output="mhtirogla", is_hidden=False, order=2)
        TestCase.objects.create(problem=rev_str, input_data="a", expected_output="a", is_hidden=True, order=3)
        TestCase.objects.create(problem=rev_str, input_data="CodeDuel", expected_output="leuDedoC", is_hidden=True, order=4)
        TestCase.objects.create(problem=rev_str, input_data="racecar", expected_output="racecar", is_hidden=True, order=5)

        # ==========================================
        # 12. VALID ANAGRAM (EASY)
        # ==========================================
        anagram = Problem.objects.create(
            title="Valid Anagram",
            difficulty="EASY",
            description=(
                "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.\n\n"
                "An **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, "
                "typically using all the original letters exactly once."
            ),
            input_format="Line 1: string s\nLine 2: string t",
            output_format="true or false",
            constraints="1 <= s.length, t.length <= 5 * 10^4\ns and t consist of lowercase English letters.",
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    s = lines[0].strip()\n    t = lines[1].strip()\n    print('true' if sorted(s) == sorted(t) else 'false')\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s, t;\n    if (cin >> s >> t) {\n        sort(s.begin(), s.end());\n        sort(t.begin(), t.end());\n        cout << (s == t ? \"true\" : \"false\") << endl;\n    }\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    if (lines.length < 2) return;\n    const s = lines[0].trim().split('').sort().join('');\n    const t = lines[1].trim().split('').sort().join('');\n    console.log(s === t ? 'true' : 'false');\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=anagram, input_data="anagram\nnagaram", expected_output="true", is_hidden=False, order=1)
        TestCase.objects.create(problem=anagram, input_data="rat\ncar", expected_output="false", is_hidden=False, order=2)
        TestCase.objects.create(problem=anagram, input_data="listen\nsilent", expected_output="true", is_hidden=True, order=3)
        TestCase.objects.create(problem=anagram, input_data="a\nb", expected_output="false", is_hidden=True, order=4)
        TestCase.objects.create(problem=anagram, input_data="ab\na", expected_output="false", is_hidden=True, order=5)

        # ==========================================
        # 13. BINARY SEARCH (EASY)
        # ==========================================
        bsearch = Problem.objects.create(
            title="Binary Search",
            difficulty="EASY",
            description=(
                "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, "
                "write a function to search `target` in `nums`. If `target` exists, then return its 0-based index. "
                "Otherwise, return `-1`.\n\n"
                "You must write an algorithm with `O(log n)` runtime complexity."
            ),
            input_format="Line 1: space-separated sorted integers (nums)\nLine 2: target integer",
            output_format="0-based index or -1",
            constraints="1 <= nums.length <= 10^5\n-10^4 < nums[i], target < 10^4\nAll the integers in nums are unique.\nnums is sorted in ascending order.",
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    nums = list(map(int, lines[0].split()))\n    target = int(lines[1].strip())\n    l, r = 0, len(nums) - 1\n    ans = -1\n    while l <= r:\n        mid = (l + r) // 2\n        if nums[mid] == target:\n            ans = mid\n            break\n        elif nums[mid] < target:\n            l = mid + 1\n        else:\n            r = mid - 1\n    print(ans)\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string line;\n    if (!getline(cin, line)) return 0;\n    stringstream ss(line);\n    vector<int> nums;\n    int v;\n    while (ss >> v) nums.push_back(v);\n    int target;\n    if (!(cin >> target)) return 0;\n    int l = 0, r = (int)nums.size() - 1, ans = -1;\n    while (l <= r) {\n        int mid = l + (r - l) / 2;\n        if (nums[mid] == target) { ans = mid; break; }\n        else if (nums[mid] < target) l = mid + 1;\n        else r = mid - 1;\n    }\n    cout << ans << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    if (lines.length < 2) return;\n    const nums = lines[0].trim().split(/\\s+/).map(Number);\n    const target = Number(lines[1].trim());\n    let l = 0, r = nums.length - 1, ans = -1;\n    while (l <= r) {\n        const mid = Math.floor((l + r) / 2);\n        if (nums[mid] === target) { ans = mid; break; }\n        else if (nums[mid] < target) l = mid + 1;\n        else r = mid - 1;\n    }\n    console.log(ans);\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=bsearch, input_data="-1 0 3 5 9 12\n9", expected_output="4", is_hidden=False, order=1)
        TestCase.objects.create(problem=bsearch, input_data="-1 0 3 5 9 12\n2", expected_output="-1", is_hidden=False, order=2)
        TestCase.objects.create(problem=bsearch, input_data="5\n5", expected_output="0", is_hidden=True, order=3)
        TestCase.objects.create(problem=bsearch, input_data="1 3 5 7 9 11 15 20\n20", expected_output="7", is_hidden=True, order=4)
        TestCase.objects.create(problem=bsearch, input_data="2 4 6 8 10\n1", expected_output="-1", is_hidden=True, order=5)

        # ==========================================
        # 14. CLIMBING STAIRS (EASY)
        # ==========================================
        stairs = Problem.objects.create(
            title="Climbing Stairs",
            difficulty="EASY",
            description=(
                "You are climbing a staircase. It takes `n` steps to reach the top.\n\n"
                "Each time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?"
            ),
            input_format="A single integer n",
            output_format="A single integer representing the number of distinct ways",
            constraints="1 <= n <= 45",
            starter_code_python="import sys\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw:\n        return\n    n = int(raw)\n    if n <= 2:\n        print(n)\n        return\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    print(b)\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\nusing namespace std;\n\nint main() {\n    long long n;\n    if (!(cin >> n)) return 0;\n    if (n <= 2) { cout << n << endl; return 0; }\n    long long a = 1, b = 2;\n    for (int i = 3; i <= n; i++) {\n        long long c = a + b;\n        a = b;\n        b = c;\n    }\n    cout << b << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const raw = fs.readFileSync(0, 'utf-8').trim();\n    if (!raw) return;\n    const n = Number(raw);\n    if (n <= 2) { console.log(n); return; }\n    let a = 1, b = 2;\n    for (let i = 3; i <= n; i++) {\n        const c = a + b;\n        a = b;\n        b = c;\n    }\n    console.log(b);\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=stairs, input_data="2", expected_output="2", is_hidden=False, order=1)
        TestCase.objects.create(problem=stairs, input_data="3", expected_output="3", is_hidden=False, order=2)
        TestCase.objects.create(problem=stairs, input_data="1", expected_output="1", is_hidden=True, order=3)
        TestCase.objects.create(problem=stairs, input_data="5", expected_output="8", is_hidden=True, order=4)
        TestCase.objects.create(problem=stairs, input_data="10", expected_output="89", is_hidden=True, order=5)
        TestCase.objects.create(problem=stairs, input_data="20", expected_output="10946", is_hidden=True, order=6)

        # ==========================================
        # 15. MERGE TWO SORTED ARRAYS (EASY)
        # ==========================================
        merge_arr = Problem.objects.create(
            title="Merge Two Sorted Arrays",
            difficulty="EASY",
            description=(
                "You are given two sorted integer arrays `arr1` and `arr2`.\n\n"
                "Merge them into a single sorted array and output the resulting space-separated numbers in non-decreasing order."
            ),
            input_format="Line 1: space-separated integers for arr1\nLine 2: space-separated integers for arr2",
            output_format="Space-separated sorted integers",
            constraints="0 <= arr1.length, arr2.length <= 10^5\n-10^9 <= arr1[i], arr2[j] <= 10^9",
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    a1 = list(map(int, lines[0].split())) if len(lines) > 0 and lines[0].strip() else []\n    a2 = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []\n    merged = sorted(a1 + a2)\n    print(\" \".join(map(str, merged)))\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string l1, l2;\n    vector<int> res;\n    if (getline(cin, l1)) {\n        stringstream ss(l1);\n        int x; while (ss >> x) res.push_back(x);\n    }\n    if (getline(cin, l2)) {\n        stringstream ss(l2);\n        int x; while (ss >> x) res.push_back(x);\n    }\n    sort(res.begin(), res.end());\n    for (size_t i = 0; i < res.size(); i++) {\n        cout << res[i] << (i + 1 == res.size() ? \"\" : \" \");\n    }\n    cout << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    const a1 = lines[0] && lines[0].trim() ? lines[0].trim().split(/\\s+/).map(Number) : [];\n    const a2 = lines[1] && lines[1].trim() ? lines[1].trim().split(/\\s+/).map(Number) : [];\n    const res = a1.concat(a2).sort((a, b) => a - b);\n    console.log(res.join(' '));\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=merge_arr, input_data="1 3 5\n2 4 6", expected_output="1 2 3 4 5 6", is_hidden=False, order=1)
        TestCase.objects.create(problem=merge_arr, input_data="1 2 3\n", expected_output="1 2 3", is_hidden=False, order=2)
        TestCase.objects.create(problem=merge_arr, input_data="\n5 10", expected_output="5 10", is_hidden=True, order=3)
        TestCase.objects.create(problem=merge_arr, input_data="-5 0 20\n-10 -2 30", expected_output="-10 -5 -2 0 20 30", is_hidden=True, order=4)
        TestCase.objects.create(problem=merge_arr, input_data="7\n3", expected_output="3 7", is_hidden=True, order=5)

        # ==========================================
        # 16. 3SUM (MEDIUM)
        # ==========================================
        three_sum = Problem.objects.create(
            title="3Sum",
            difficulty="MEDIUM",
            description=(
                "Given an integer array `nums`, return the count of distinct triplets `[nums[i], nums[j], nums[k]]` "
                "such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\n"
                "Notice that the solution set must not contain duplicate triplets."
            ),
            input_format="Space-separated integers representing nums",
            output_format="A single integer representing the count of unique triplets",
            constraints="3 <= nums.length <= 3000\n-10^5 <= nums[i] <= 10^5",
            starter_code_python="import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    nums.sort()\n    n = len(nums)\n    count = 0\n    for i in range(n - 2):\n        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n        l, r = i + 1, n - 1\n        while l < r:\n            s = nums[i] + nums[l] + nums[r]\n            if s == 0:\n                count += 1\n                while l < r and nums[l] == nums[l + 1]:\n                    l += 1\n                while l < r and nums[r] == nums[r - 1]:\n                    r -= 1\n                l += 1\n                r -= 1\n            elif s < 0:\n                l += 1\n            else:\n                r -= 1\n    print(count)\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int v;\n    vector<int> nums;\n    while (cin >> v) nums.push_back(v);\n    sort(nums.begin(), nums.end());\n    int n = nums.size(), count = 0;\n    for (int i = 0; i < n - 2; i++) {\n        if (i > 0 && nums[i] == nums[i - 1]) continue;\n        int l = i + 1, r = n - 1;\n        while (l < r) {\n            int s = nums[i] + nums[l] + nums[r];\n            if (s == 0) {\n                count++;\n                while (l < r && nums[l] == nums[l + 1]) l++;\n                while (l < r && nums[r] == nums[r - 1]) r--;\n                l++; r--;\n            } else if (s < 0) l++;\n            else r--;\n        }\n    }\n    cout << count << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const nums = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\n    nums.sort((a, b) => a - b);\n    let count = 0;\n    const n = nums.length;\n    for (let i = 0; i < n - 2; i++) {\n        if (i > 0 && nums[i] === nums[i - 1]) continue;\n        let l = i + 1, r = n - 1;\n        while (l < r) {\n            const s = nums[i] + nums[l] + nums[r];\n            if (s === 0) {\n                count++;\n                while (l < r && nums[l] === nums[l + 1]) l++;\n                while (l < r && nums[r] === nums[r - 1]) r--;\n                l++; r--;\n            } else if (s < 0) l++;\n            else r--;\n        }\n    }\n    console.log(count);\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=three_sum, input_data="-1 0 1 2 -1 -4", expected_output="2", is_hidden=False, order=1)
        TestCase.objects.create(problem=three_sum, input_data="0 1 1", expected_output="0", is_hidden=False, order=2)
        TestCase.objects.create(problem=three_sum, input_data="0 0 0", expected_output="1", is_hidden=True, order=3)
        TestCase.objects.create(problem=three_sum, input_data="-2 0 1 1 2", expected_output="2", is_hidden=True, order=4)
        TestCase.objects.create(problem=three_sum, input_data="-4 -2 -2 -2 0 1 2 2 2 3 3 4 4 6 6", expected_output="6", is_hidden=True, order=5)

        # ==========================================
        # 17. ROTATE IMAGE (MEDIUM)
        # ==========================================
        rotate_img = Problem.objects.create(
            title="Rotate Image",
            difficulty="MEDIUM",
            description=(
                "You are given an `n x n` 2D matrix representing an image. Rotate the image by **90 degrees (clockwise)**.\n\n"
                "**Input format:**\n"
                "Line 1: single integer `n`\n"
                "Next `n` lines: `n` space-separated integers representing each row\n\n"
                "**Output format:**\n"
                "The rotated matrix, one row per line, elements space-separated."
            ),
            input_format="Line 1: integer n\nNext n lines: n space-separated integers",
            output_format="n lines of space-separated integers",
            constraints="1 <= n <= 50\n-1000 <= matrix[i][j] <= 1000",
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if not lines:\n        return\n    n = int(lines[0].strip())\n    matrix = [list(map(int, lines[i + 1].split())) for i in range(n)]\n    rotated = [[matrix[n - 1 - r][c] for r in range(n)] for c in range(n)]\n    for row in rotated:\n        print(\" \".join(map(str, row)))\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    if (!(cin >> n)) return 0;\n    vector<vector<int>> m(n, vector<int>(n));\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            cin >> m[i][j];\n    for (int c = 0; c < n; c++) {\n        for (int r = n - 1; r >= 0; r--) {\n            cout << m[r][c] << (r == 0 ? \"\" : \" \");\n        }\n        cout << endl;\n    }\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/).filter(l => l.trim().length > 0);\n    if (!lines.length) return;\n    const n = Number(lines[0].trim());\n    const m = [];\n    for (let i = 0; i < n; i++) {\n        m.push(lines[i + 1].trim().split(/\\s+/).map(Number));\n    }\n    for (let c = 0; c < n; c++) {\n        const row = [];\n        for (let r = n - 1; r >= 0; r--) {\n            row.push(m[r][c]);\n        }\n        console.log(row.join(' '));\n    }\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=rotate_img, input_data="3\n1 2 3\n4 5 6\n7 8 9", expected_output="7 4 1\n8 5 2\n9 6 3", is_hidden=False, order=1)
        TestCase.objects.create(problem=rotate_img, input_data="2\n1 2\n3 4", expected_output="3 1\n4 2", is_hidden=False, order=2)
        TestCase.objects.create(problem=rotate_img, input_data="1\n42", expected_output="42", is_hidden=True, order=3)
        TestCase.objects.create(problem=rotate_img, input_data="4\n5 1 9 11\n2 4 8 10\n13 3 6 7\n15 14 12 16", expected_output="15 13 2 5\n14 3 4 1\n12 6 8 9\n16 7 10 11", is_hidden=True, order=4)

        # ==========================================
        # 18. LONGEST PALINDROMIC SUBSTRING (MEDIUM)
        # ==========================================
        longest_pal = Problem.objects.create(
            title="Longest Palindromic Substring",
            difficulty="MEDIUM",
            description=(
                "Given a string `s`, return the length of the longest palindromic substring in `s`.\n\n"
                "A string is palindromic if it reads the same forward and backward."
            ),
            input_format="A single line containing string s",
            output_format="A single integer representing the length of the longest palindromic substring",
            constraints="1 <= s.length <= 1000\ns consists of only digits and English letters.",
            starter_code_python="import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        print(0)\n        return\n    n = len(s)\n    def expand(l, r):\n        while l >= 0 and r < n and s[l] == s[r]:\n            l -= 1\n            r += 1\n        return r - l - 1\n\n    max_len = 1\n    for i in range(n):\n        l1 = expand(i, i)\n        l2 = expand(i, i + 1)\n        max_len = max(max_len, l1, l2)\n    print(max_len)\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <algorithm>\nusing namespace std;\n\nint expand(const string& s, int l, int r) {\n    int n = s.size();\n    while (l >= 0 && r < n && s[l] == s[r]) { l--; r++; }\n    return r - l - 1;\n}\n\nint main() {\n    string s;\n    if (!(cin >> s)) { cout << 0 << endl; return 0; }\n    int max_len = 1, n = s.size();\n    for (int i = 0; i < n; i++) {\n        max_len = max({max_len, expand(s, i, i), expand(s, i, i + 1)});\n    }\n    cout << max_len << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').trim();\n    if (!s) { console.log(0); return; }\n    const n = s.length;\n    function expand(l, r) {\n        while (l >= 0 && r < n && s[l] === s[r]) { l--; r++; }\n        return r - l - 1;\n    }\n    let maxLen = 1;\n    for (let i = 0; i < n; i++) {\n        maxLen = Math.max(maxLen, expand(i, i), expand(i, i + 1));\n    }\n    console.log(maxLen);\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=longest_pal, input_data="babad", expected_output="3", is_hidden=False, order=1)
        TestCase.objects.create(problem=longest_pal, input_data="cbbd", expected_output="2", is_hidden=False, order=2)
        TestCase.objects.create(problem=longest_pal, input_data="a", expected_output="1", is_hidden=True, order=3)
        TestCase.objects.create(problem=longest_pal, input_data="racecar", expected_output="7", is_hidden=True, order=4)
        TestCase.objects.create(problem=longest_pal, input_data="forgeeksskeegfor", expected_output="10", is_hidden=True, order=5)

        # ==========================================
        # 19. WORD BREAK (MEDIUM)
        # ==========================================
        word_break = Problem.objects.create(
            title="Word Break",
            difficulty="MEDIUM",
            description=(
                "Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be "
                "segmented into a space-separated sequence of one or more dictionary words, or `false` otherwise.\n\n"
                "Note that the same word in the dictionary may be reused multiple times in the segmentation."
            ),
            input_format="Line 1: string s\nLine 2: space-separated dictionary words",
            output_format="true or false",
            constraints="1 <= s.length <= 300\n1 <= wordDict.length <= 1000\n1 <= wordDict[i].length <= 20\ns and wordDict[i] consist of lowercase English letters.",
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    s = lines[0].strip()\n    words = set(lines[1].split())\n    dp = [False] * (len(s) + 1)\n    dp[0] = True\n    for i in range(1, len(s) + 1):\n        for j in range(i):\n            if dp[j] and s[j:i] in words:\n                dp[i] = True\n                break\n    print('true' if dp[len(s)] else 'false')\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <vector>\n#include <unordered_set>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string s, dict_line;\n    if (!getline(cin, s)) return 0;\n    if (!getline(cin, dict_line)) return 0;\n    stringstream ss(dict_line);\n    unordered_set<string> words;\n    string w;\n    while (ss >> w) words.insert(w);\n    int n = s.size();\n    vector<bool> dp(n + 1, false);\n    dp[0] = true;\n    for (int i = 1; i <= n; i++) {\n        for (int j = 0; j < i; j++) {\n            if (dp[j] && words.count(s.substr(j, i - j))) {\n                dp[i] = true;\n                break;\n            }\n        }\n    }\n    cout << (dp[n] ? \"true\" : \"false\") << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    if (lines.length < 2) return;\n    const s = lines[0].trim();\n    const words = new Set(lines[1].trim().split(/\\s+/));\n    const dp = new Array(s.length + 1).fill(false);\n    dp[0] = true;\n    for (let i = 1; i <= s.length; i++) {\n        for (let j = 0; j < i; j++) {\n            if (dp[j] && words.has(s.substring(j, i))) {\n                dp[i] = true;\n                break;\n            }\n        }\n    }\n    console.log(dp[s.length] ? 'true' : 'false');\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=word_break, input_data="leetcode\nleet code", expected_output="true", is_hidden=False, order=1)
        TestCase.objects.create(problem=word_break, input_data="applepenapple\napple pen", expected_output="true", is_hidden=False, order=2)
        TestCase.objects.create(problem=word_break, input_data="catsandog\ncats dog sand and cat", expected_output="false", is_hidden=True, order=3)
        TestCase.objects.create(problem=word_break, input_data="cars\ncar ca rs", expected_output="true", is_hidden=True, order=4)
        TestCase.objects.create(problem=word_break, input_data="aaaaaaa\naaa aaaa", expected_output="true", is_hidden=True, order=5)

        # ==========================================
        # 20. EDIT DISTANCE (HARD)
        # ==========================================
        edit_dist = Problem.objects.create(
            title="Edit Distance",
            difficulty="HARD",
            description=(
                "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.\n\n"
                "You have the following three operations permitted on a word:\n"
                "1. Insert a character\n"
                "2. Delete a character\n"
                "3. Replace a character"
            ),
            input_format="Line 1: word1\nLine 2: word2",
            output_format="A single integer representing minimum operations",
            constraints="0 <= word1.length, word2.length <= 500\nword1 and word2 consist of lowercase English letters.",
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    w1 = lines[0].strip() if len(lines) > 0 else \"\"\n    w2 = lines[1].strip() if len(lines) > 1 else \"\"\n    m, n = len(w1), len(w2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1): dp[i][0] = i\n    for j in range(n + 1): dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if w1[i - 1] == w2[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1]\n            else:\n                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n    print(dp[m][n])\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string w1, w2;\n    getline(cin, w1);\n    getline(cin, w2);\n    int m = w1.size(), n = w2.size();\n    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));\n    for (int i = 0; i <= m; i++) dp[i][0] = i;\n    for (int j = 0; j <= n; j++) dp[0][j] = j;\n    for (int i = 1; i <= m; i++) {\n        for (int j = 1; j <= n; j++) {\n            if (w1[i - 1] == w2[j - 1]) dp[i][j] = dp[i - 1][j - 1];\n            else dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});\n        }\n    }\n    cout << dp[m][n] << endl;\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').split(/\\r?\\n/);\n    const w1 = lines[0] ? lines[0].trim() : '';\n    const w2 = lines[1] ? lines[1].trim() : '';\n    const m = w1.length, n = w2.length;\n    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));\n    for (let i = 0; i <= m; i++) dp[i][0] = i;\n    for (let j = 0; j <= n; j++) dp[0][j] = j;\n    for (let i = 1; i <= m; i++) {\n        for (let j = 1; j <= n; j++) {\n            if (w1[i - 1] === w2[j - 1]) dp[i][j] = dp[i - 1][j - 1];\n            else dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);\n        }\n    }\n    console.log(dp[m][n]);\n}\nsolve();\n"
        )
        TestCase.objects.create(problem=edit_dist, input_data="horse\nros", expected_output="3", is_hidden=False, order=1)
        TestCase.objects.create(problem=edit_dist, input_data="intention\nexecution", expected_output="5", is_hidden=False, order=2)
        TestCase.objects.create(problem=edit_dist, input_data="abc\nabc", expected_output="0", is_hidden=True, order=3)
        TestCase.objects.create(problem=edit_dist, input_data="kitten\nsitting", expected_output="3", is_hidden=True, order=4)
        TestCase.objects.create(problem=edit_dist, input_data="\na", expected_output="1", is_hidden=True, order=5)

        # ==========================================
        # ENSURE DEMO TEST ACCOUNT EXISTS
        # ==========================================
        from django.contrib.auth.models import User
        if not User.objects.filter(username="demo_coder").exists():
            demo_user = User.objects.create_user(
                username="demo_coder",
                email="demo@codeduel.dev",
                password="password123"
            )
            demo_user.profile.rating = 150
            demo_user.profile.wins = 3
            demo_user.profile.losses = 1
            demo_user.profile.save()
            self.stdout.write(self.style.SUCCESS("Created demo user 'demo_coder' (password: password123)"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded 20 comprehensive DSA problems with sample & hidden test cases!"))


