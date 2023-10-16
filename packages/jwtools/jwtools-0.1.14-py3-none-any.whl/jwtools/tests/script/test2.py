from jwtools.func import *


# 示例列表
my_list = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]

# 获取列表的最大维度
max_dimension = get_max_dimension(my_list)
print(max_dimension)  # 输出 2

print_line('不使用 NumPy 平铺列表')

# 示例列表
my_list = [[1, 2, 3], [4, [5, 6]], [7, 8, [9, 10]]]

# 不使用 NumPy 平铺列表
flattened_list = flatten_list(my_list)
print(flattened_list)  # 输出 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print_line('不使用 NumPy 平铺列表2')

# 示例列表
my_list = [[1, 2, 3], [4, [5, 6]], [7, 8, [9, 10]], [11, [12, [13, 14, [15, 16]]]]]

# 不使用 NumPy 平铺列表
flattened_list = flatten_list(my_list)
print(flattened_list)  # 输出 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]