def kmp_search(pattern, text):
    if pattern == "":
        return 0


    lsp = [0]
    for c in pattern[1 : ]:
        j = lsp[-1]
        while j > 0 and c != pattern[j]:
            j = lsp[j - 1]
        if c == pattern[j]:
            j += 1
        lsp.append(j)


    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = lsp[j - 1]
        if text[i] == pattern[j]:
            j += 1
            if j == len(pattern):
                return i - (j - 1)
    return None

def main():
	hay = "aaabaa"
	needle = "ab"
	print(kmp_search(needle,hay))
#
main()