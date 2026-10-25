#Leetcode 334
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        smallest=float("inf")
        second=float("inf")

        for i in nums:
            if i <=smallest:
                smallest=i
            elif i <=second:
                second=i
            elif i > smallest and i >second:
                return True
        
        return False