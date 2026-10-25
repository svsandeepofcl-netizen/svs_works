class Solution:
    def canPlaceFlowers(self, nums: List[int], n: int) -> bool:

        for i in range(len(nums)):

            if nums[i] == 0:

                # check left side
                left = (i == 0 or nums[i-1] == 0)

                # check right side
                right = (i == len(nums)-1 or nums[i+1] == 0)

                # safe to plant
                if left and right:

                    nums[i] = 1
                    n -= 1

                    print(f"Inserted at index {i}")

                    if n == 0:
                        return True

        return n <= 0