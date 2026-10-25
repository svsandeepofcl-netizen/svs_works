#leetcode 345
class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels=['a', 'e', 'i','o','u', 'A','E','I','O','U']
        found=[]
        new_String=''

        for i in s:
            if i in vowels:
                found.append(i)

        for i in range(len(s)):
            if s[i] in vowels:
                new_String=new_String+found.pop()
            else:
                new_String=new_String+s[i]
        
        return new_String