#leetcode 125

class Solution:
    def isPalindrome(self, s: str) -> bool:
        arr = [char for char in s if char.isalnum()]
        left = 0
        print(arr)
        right = len(arr)-1
        while left < right:
            if arr[left].lower()!=arr[right].lower():
                return False
                break
            else:
                left+=1
                right-=1

        else:
            return True
                