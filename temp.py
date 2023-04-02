class Solution:
    def buddyStrings(self, s: str, goal: str) -> bool:
        if len(s) != len(goal):
            return False
        else:
            (diff_a, diff_b, same) = ([], [], [])
            w = 0
            for (a, b) in list(zip(s, goal)):
                if a != b:
                    diff_a.append(a)
                    diff_b.append(b)
                else:
                    same.append(a)
                w += 1
            if len(diff_a) != 2 or len(diff_b) != 0:
                return False
            elif diff_a != diff_b.reverse():
                return False
            elif len(set(same)) == len(same):
                return False
            return True


k = Solution()
print(k.buddyStrings('ab', 'ba'))
