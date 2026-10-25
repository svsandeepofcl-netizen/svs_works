#brute force approach
class Solution(object):
    def mergeAlternately(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: str
        """
        loop_length=min(len(word1), len(word2))
        
        output=''

        for i in range(loop_length):
            output=output+word1[i]+word2[i]

        output=output+word1[loop_length:]
        output=output+word2[loop_length:]

        return output

obj=Solution()
word1 = "abcdfgh"
word2 = "pq"

print(obj.mergeAlternately(word1,word2))
