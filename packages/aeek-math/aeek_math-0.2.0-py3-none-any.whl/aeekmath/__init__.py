from typing import Tuple


def egcd(a: int, b: int) -> Tuple[int, int, int]:
	"""
	Возвращает числа g, x, y такие, что ax + by = gcd(a,b).
	"""
	if a*b == 0:
		return max(a, b), 1, 1
	else:
		g, x, y = egcd(b, a % b)
		n = a // b
		x, y = y, x - n * y
		return g, x, y


def bin_pow(a: int, p: int, mod: int) -> int:
	"""
	Возводит число a в степень p по модулю mod.
	"""
	if p == 0:
		return 1
	elif p % 2 == 1:
		return a * bin_pow(a, p - 1, mod) % mod
	else:
		return bin_pow(a, p // 2, mod) ** 2 % mod

# def bin_pow(a: int, p: int, mod: int) -> int:
#     cur = a
#     ans = 1
#     while p > 0:
#         if p & 1:
#             ans *= cur
#             ans %= mod
#         p //= 2
#         cur *= cur
#
#     return ans
