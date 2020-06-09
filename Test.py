from typing import List


class Solution:

    #48 最长不含重复字符的子字符串
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0
        d = {}
        length = len(s)
        tmp = 1
        for i in range(0, length):
            count = 0
            for k in range(i, length):
                if s[k] in d:
                    d = {}
                    tmp = max(tmp, count)
                    count = 0
                    break
                else:
                    d[s[k]] = True
                    count  += 1
            tmp = max(tmp, count)
        return tmp

    # 快速排序
    def quickSort(self, array, start, end):
        l, r = start, end
        key = array[l]
        while l<r:
            while l<r and array[r] >= key:
                r -= 1
            if l<r:
                array[l] = array[r]
                l += 1
            while l<r and array[l] <= key:
                l += 1
            if l<r:
                array[r] = array[l]
                r -= 1
        array[l] = key
        return l

    def qs(self, l, start, end):
        if start < end:
            i = self.quickSort(l, start, end)
            self.qs(l, start, i-1)
            self.qs(l, i+1, end)
        print(l)

    #59 滑窗最大值
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        length = len(nums)
        dum = [None] * len(nums)
        start = 0
        end = start + k
        while end <= length:
            val = 0
            for i in range(start, end):
                val = max(val, nums[i])
            res. append(val)
            start += 1
            end += 1
        return res

    def permutation(self, s: str) -> List[str]:
        s, res = list(s), set()
        def dfs(x):
            if x == len(s)-1:
                res.add(''.join(s))
                return
            for i in range(x, len(s)):
                print(res)
                s[x], s[i] = s[i], s[x]
                # res.add(''.join(s))
                dfs(x+1)
                s[x], s[i] = s[i], s[x]
        dfs(0)
        print(list(res))

    def dfs(self, x):
        if x == 6:
            print("stop")
            return
        print("开始递归")
        print("dfs(%d)" %x)
        self.dfs(x + 1)
        print("结束递归")
        print(x)
    def cont_break(self):
        for i in range(10):

            for j in range(10):
                if j == 3:
                    continue
                print(j)
            print("####%d" % i)
    #二叉搜索树判断
    def verifyPostorder(self, postorder) -> bool:
        if not postorder:
            return

        def isTree(l):
            root = l[-1]
            length = len(l)

            for i in range(length):
                if l[i] > root:
                    break
            for j in range(i, length - 1):
                if l[j] < root:
                    return False

            left = True
            if i > 0:
                left = isTree(l[:i])
            right = True
            if i < length - 1:
                right = isTree(l[i:-1])
            # isTree(l[:i])
            # isTree(l[i:-1])
            return left and right

        return isTree(postorder)


if __name__ == "__main__":
    tree = [4, 8, 6, 12, 16, 14, 10]
    s=Solution()
    res = s.verifyPostorder(tree)
    print(res)