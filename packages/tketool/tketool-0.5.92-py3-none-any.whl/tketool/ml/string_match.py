def lcs(s1, s2):
    # 创建一个二维数组来存储在每一步中计算出来的Levenshtein距离
    dp_table = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]

    # 初始化第一行和第一列，这对应于将一个空字符串转化为另一个字符串
    for i in range(len(s1) + 1):
        dp_table[i][0] = i

    for j in range(len(s2) + 1):
        dp_table[0][j] = j

    # 对s1和s2进行迭代
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1

            # 在三种可能的操作（删除、插入、替换）中选择最小的值
            dp_table[i][j] = min(dp_table[i - 1][j] + 1,  # 删除
                                 dp_table[i][j - 1] + 1,  # 插入
                                 dp_table[i - 1][j - 1] + cost)  # 替换

    return dp_table[-1][-1] / max(len(s1), len(s2))


def match_2_string_list(list1: [str], list2: [str], top_n=1) -> [[int]]:
    result = []

    for str1 in list1:
        lcs_values = [(lcs(str1, str2), index) for index, str2 in enumerate(list2)]
        lcs_values.sort(key=lambda x: x[0], reverse=True)
        best_match_indices = [index for _, index in lcs_values[:top_n]]

        result.append(best_match_indices)

    return result
