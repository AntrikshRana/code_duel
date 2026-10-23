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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if not lines:\n        return\n    nums = list(map(int, lines[0].split()))\n    target = int(lines[1].strip())\n    \n    # Write your solution here: print indices separated by space (e.g. 0 1)\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string line;\n    if (!getline(cin, line)) return 0;\n    stringstream ss(line);\n    vector<int> nums;\n    int val, target;\n    while (ss >> val) nums.push_back(val);\n    if (!(cin >> target)) return 0;\n    \n    // Write your solution here: output indices separated by space\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n    if (lines.length < 2) return;\n    const nums = lines[0].trim().split(/\\s+/).map(Number);\n    const target = Number(lines[1].trim());\n    \n    // Write your solution here: console.log(`${idx1} ${idx2}`)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    \n    # Write your solution here: print 'true' or 'false'\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!(cin >> s)) return 0;\n    \n    // Write your solution here: output \"true\" or \"false\"\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').trim();\n    \n    // Write your solution here: console.log('true' or 'false')\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw:\n        return\n    \n    # Write your solution here: print 'true' or 'false'\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!(cin >> s)) return 0;\n    \n    // Write your solution here: output \"true\" or \"false\"\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').trim();\n    \n    // Write your solution here: console.log('true' or 'false')\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    if not nums:\n        return\n    \n    # Write your solution here: print maximum profit\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int p;\n    vector<int> prices;\n    while (cin >> p) prices.push_back(p);\n    if (prices.empty()) return 0;\n    \n    // Write your solution here: output maximum profit\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const prices = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\n    if (!prices.length) return;\n    \n    // Write your solution here: console.log(maxProfit)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    if not nums:\n        return\n    \n    # Write your solution here: print maximum subarray sum\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int val;\n    vector<int> nums;\n    while (cin >> val) nums.push_back(val);\n    if (nums.empty()) return 0;\n    \n    // Write your solution here: output maximum subarray sum\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const nums = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\n    if (!nums.length) return;\n    \n    // Write your solution here: console.log(maxSubarraySum)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    h = list(map(int, sys.stdin.read().split()))\n    if not h:\n        return\n    \n    # Write your solution here: print max water area\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int val;\n    vector<int> h;\n    while (cin >> val) h.push_back(val);\n    \n    // Write your solution here: output maximum water area\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const h = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\n    \n    // Write your solution here: console.log(maxWaterArea)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    s = sys.stdin.read().rstrip('\\r\\n')\n    \n    # Write your solution here: print length of longest substring without duplicates\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!getline(cin, s)) { cout << 0 << endl; return 0; }\n    \n    // Write your solution here: output length of longest unique substring\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').replace(/\\r?\\n$/, '');\n    \n    // Write your solution here: console.log(longestSubstringLength)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    coins = list(map(int, lines[0].split()))\n    amount = int(lines[1].strip())\n    \n    # Write your solution here: print fewest coins needed, or -1\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string line;\n    if (!getline(cin, line)) return 0;\n    stringstream ss(line);\n    vector<int> coins;\n    int c, amount;\n    while (ss >> c) coins.push_back(c);\n    if (!(cin >> amount)) return 0;\n    \n    // Write your solution here: output fewest coins needed, or -1\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n    if (lines.length < 2) return;\n    const coins = lines[0].trim().split(/\\s+/).map(Number);\n    const amount = Number(lines[1].trim());\n    \n    // Write your solution here: console.log(fewestCoins or -1)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    h = list(map(int, sys.stdin.read().split()))\n    if not h:\n        return\n    \n    # Write your solution here: print trapped rain water units\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int val;\n    vector<int> h;\n    while (cin >> val) h.push_back(val);\n    \n    // Write your solution here: output trapped rain water units\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const h = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\n    \n    // Write your solution here: console.log(trappedWater)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    nums1 = list(map(int, lines[0].split())) if len(lines) > 0 and lines[0].strip() else []\n    nums2 = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []\n    \n    # Write your solution here: print median formatted with 1 decimal place (e.g. 2.0 or 2.5)\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string l1, l2;\n    vector<int> a, b;\n    if (getline(cin, l1)) {\n        stringstream ss(l1);\n        int v; while (ss >> v) a.push_back(v);\n    }\n    if (getline(cin, l2)) {\n        stringstream ss(l2);\n        int v; while (ss >> v) b.push_back(v);\n    }\n    \n    // Write your solution here: output median to 1 decimal place\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n    const a1 = lines[0] && lines[0].trim() ? lines[0].trim().split(/\\s+/).map(Number) : [];\n    const a2 = lines[1] && lines[1].trim() ? lines[1].trim().split(/\\s+/).map(Number) : [];\n    \n    // Write your solution here: console.log(median.toFixed(1))\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    s = sys.stdin.read().rstrip('\\r\\n')\n    \n    # Write your solution here: print reversed string\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s;\n    if (getline(cin, s)) {\n        // Write your solution here: output reversed string\n    }\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').replace(/\\r?\\n$/, '');\n    \n    // Write your solution here: console.log(reversedString)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    s = lines[0].strip()\n    t = lines[1].strip()\n    \n    # Write your solution here: print 'true' or 'false'\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s, t;\n    if (cin >> s >> t) {\n        // Write your solution here: output \"true\" or \"false\"\n    }\n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    if (lines.length < 2) return;\n    const s = lines[0].trim();\n    const t = lines[1].trim();\n    \n    // Write your solution here: console.log('true' or 'false')\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    nums = list(map(int, lines[0].split()))\n    target = int(lines[1].strip())\n    \n    # Write your solution here: print 0-based index or -1\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string line;\n    if (!getline(cin, line)) return 0;\n    stringstream ss(line);\n    vector<int> nums;\n    int v, target;\n    while (ss >> v) nums.push_back(v);\n    if (!(cin >> target)) return 0;\n    \n    // Write your solution here: output 0-based index or -1\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    if (lines.length < 2) return;\n    const nums = lines[0].trim().split(/\\s+/).map(Number);\n    const target = Number(lines[1].trim());\n    \n    // Write your solution here: console.log(index or -1)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw:\n        return\n    n = int(raw)\n    \n    # Write your solution here: print distinct ways to climb stairs\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\nusing namespace std;\n\nint main() {\n    long long n;\n    if (!(cin >> n)) return 0;\n    \n    // Write your solution here: output distinct ways to climb stairs\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const raw = fs.readFileSync(0, 'utf-8').trim();\n    if (!raw) return;\n    const n = Number(raw);\n    \n    // Write your solution here: console.log(distinctWays)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    a1 = list(map(int, lines[0].split())) if len(lines) > 0 and lines[0].strip() else []\n    a2 = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []\n    \n    # Write your solution here: print merged space-separated numbers\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string l1, l2;\n    vector<int> a, b;\n    if (getline(cin, l1)) {\n        stringstream ss(l1);\n        int x; while (ss >> x) a.push_back(x);\n    }\n    if (getline(cin, l2)) {\n        stringstream ss(l2);\n        int x; while (ss >> x) b.push_back(x);\n    }\n    \n    // Write your solution here: output space-separated merged integers\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    const a1 = lines[0] && lines[0].trim() ? lines[0].trim().split(/\\s+/).map(Number) : [];\n    const a2 = lines[1] && lines[1].trim() ? lines[1].trim().split(/\\s+/).map(Number) : [];\n    \n    // Write your solution here: console.log(merged.join(' '))\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    \n    # Write your solution here: print count of unique triplets summing to 0\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int v;\n    vector<int> nums;\n    while (cin >> v) nums.push_back(v);\n    \n    // Write your solution here: output count of unique triplets summing to 0\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const nums = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).map(Number);\n    \n    // Write your solution here: console.log(tripletsCount)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if not lines:\n        return\n    n = int(lines[0].strip())\n    matrix = [list(map(int, lines[i + 1].split())) for i in range(n)]\n    \n    # Write your solution here: print rotated matrix row by row (space-separated)\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    if (!(cin >> n)) return 0;\n    vector<vector<int>> m(n, vector<int>(n));\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            cin >> m[i][j];\n    \n    // Write your solution here: output rotated matrix row by row\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/).filter(l => l.trim().length > 0);\n    if (!lines.length) return;\n    const n = Number(lines[0].trim());\n    const m = [];\n    for (let i = 0; i < n; i++) {\n        m.push(lines[i + 1].trim().split(/\\s+/).map(Number));\n    }\n    \n    // Write your solution here: console.log rotated matrix row by row\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    if not s:\n        print(0)\n        return\n    \n    # Write your solution here: print length of longest palindromic substring\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s;\n    if (!(cin >> s)) { cout << 0 << endl; return 0; }\n    \n    // Write your solution here: output length of longest palindromic substring\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const s = fs.readFileSync(0, 'utf-8').trim();\n    if (!s) { console.log(0); return; }\n    \n    // Write your solution here: console.log(longestPalindromeLength)\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if len(lines) < 2:\n        return\n    s = lines[0].strip()\n    words = lines[1].split()\n    \n    # Write your solution here: print 'true' or 'false'\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\n#include <vector>\n#include <sstream>\nusing namespace std;\n\nint main() {\n    string s, dict_line;\n    if (!getline(cin, s)) return 0;\n    if (!getline(cin, dict_line)) return 0;\n    stringstream ss(dict_line);\n    vector<string> words;\n    string w;\n    while (ss >> w) words.push_back(w);\n    \n    // Write your solution here: output \"true\" or \"false\"\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').trim().split(/\\r?\\n/);\n    if (lines.length < 2) return;\n    const s = lines[0].trim();\n    const words = lines[1].trim().split(/\\s+/);\n    \n    // Write your solution here: console.log('true' or 'false')\n}\n\nsolve();\n"
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
            starter_code_python="import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    w1 = lines[0].strip() if len(lines) > 0 else \"\"\n    w2 = lines[1].strip() if len(lines) > 1 else \"\"\n    \n    # Write your solution here: print minimum operations\n    pass\n\nif __name__ == '__main__':\n    solve()\n",
            starter_code_cpp="#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string w1, w2;\n    getline(cin, w1);\n    getline(cin, w2);\n    \n    // Write your solution here: output minimum operations\n    \n    return 0;\n}\n",
            starter_code_javascript="const fs = require('fs');\n\nfunction solve() {\n    const lines = fs.readFileSync(0, 'utf-8').split(/\\r?\\n/);\n    const w1 = lines[0] ? lines[0].trim() : '';\n    const w2 = lines[1] ? lines[1].trim() : '';\n    \n    // Write your solution here: console.log(minOperations)\n}\n\nsolve();\n"
        )
        TestCase.objects.create(problem=edit_dist, input_data="horse\nros", expected_output="3", is_hidden=False, order=1)
        TestCase.objects.create(problem=edit_dist, input_data="intention\nexecution", expected_output="5", is_hidden=False, order=2)
        TestCase.objects.create(problem=edit_dist, input_data="abc\nabc", expected_output="0", is_hidden=True, order=3)
        TestCase.objects.create(problem=edit_dist, input_data="kitten\nsitting", expected_output="3", is_hidden=True, order=4)
        TestCase.objects.create(problem=edit_dist, input_data="\na", expected_output="1", is_hidden=True, order=5)

        self.stdout.write(self.style.SUCCESS("Successfully seeded 20 comprehensive DSA problems with starter templates (solutions removed)!"))

