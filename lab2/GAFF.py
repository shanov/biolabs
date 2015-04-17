__author__ = 'Big'
from FASTA import ReadFASTA
import os

def getScore(file,pair):
    with open(os.path.join(os.path.dirname(__file__),file )) as input_data:
        items = [line.strip().split() for line in input_data.readlines()]
        #print(items)
    j = 1

    for el in items[0]:

        if el == pair[1]:
            break
        j+=1

    i = 0
    for line in items:

        if line[0]==pair[0]:
            break
        i +=1

    res =items[j][i]
    return items[j][i]

#def global_alignment_affine_gap_penalty(v, w, scoring_matrix, sigma, epsilon):
def global_alignment_affine_gap_penalty(v, w, scoring_matrix, sigma, epsilon):
    '''Returns the global alignment score of v and w with constant gap peantaly sigma subject to the scoring_matrix.'''
    S = [[[0 for j in xrange(len(w)+1)] for i in xrange(len(v)+1)] for k in xrange(3)]
    backtrack = [[[0 for j in xrange(len(w)+1)] for i in xrange(len(v)+1)] for k in xrange(3)]

    for i in xrange(1, len(v)+1):
        S[0][i][0] = -sigma - (i-1)*epsilon
        S[1][i][0] = -sigma - (i-1)*epsilon
        S[2][i][0] = -10*sigma
    for j in xrange(1, len(w)+1):
        S[2][0][j] = -sigma - (j-1)*epsilon
        S[1][0][j] = -sigma - (j-1)*epsilon
        S[0][0][j] = -10*sigma

    for i in xrange(1, len(v)+1):
        for j in xrange(1, len(w)+1):
            lower_scores = [S[0][i-1][j] - epsilon, S[1][i-1][j] - sigma]
            S[0][i][j] = max(lower_scores)
            backtrack[0][i][j] = lower_scores.index(S[0][i][j])

            upper_scores = [S[2][i][j-1] - epsilon, S[1][i][j-1] - sigma]
            S[2][i][j] = max(upper_scores)
            backtrack[2][i][j] = upper_scores.index(S[2][i][j])

            pair=v[i-1]+w[j-1]
            #print(pair, getScore(scoring_matrix,pair ))
            middle_scores = [S[0][i][j], S[1][i-1][j-1] + int(getScore(scoring_matrix,pair ) ) , S[2][i][j]]
            S[1][i][j] = max(middle_scores)
            backtrack[1][i][j] = middle_scores.index(S[1][i][j])

    i,j = len(v), len(w)
    v_aligned, w_aligned = v, w

    matrix_scores = [S[0][i][j], S[1][i][j], S[2][i][j]]
    max_score = max(matrix_scores)
    backtrack_matrix = matrix_scores.index(max_score)

    insert_indel = lambda word, i: word[:i] + '-' + word[i:]

    while i*j != 0:
        if backtrack_matrix == 0:
            if backtrack[0][i][j] == 1:
                backtrack_matrix = 1
            i -= 1
            w_aligned = insert_indel(w_aligned, j)

        elif backtrack_matrix == 1:
            if backtrack[1][i][j] == 0:
                backtrack_matrix = 0
            elif backtrack[1][i][j] == 2:
                backtrack_matrix = 2
            else:
                i -= 1
                j -= 1

        else:
            if backtrack[2][i][j] == 1:
                backtrack_matrix = 1
            j -= 1
            v_aligned = insert_indel(v_aligned, i)

    for _ in xrange(i):
        w_aligned = insert_indel(w_aligned, 0)
    for _ in xrange(j):
        v_aligned = insert_indel(v_aligned, 0)

    return str(max_score), v_aligned, w_aligned


def main():
    # Parse the two input protein strings.
    s, t = [fasta[1] for fasta in ReadFASTA('gaff.txt')]

    # Get the alignment score.
    score = global_alignment_affine_gap_penalty(s, t, "BLOSUM62.txt", 11, 1)

    # Print and save the answer.
    with open('out_GAFF.txt', 'w') as output_data:
        output_data.write('\n'.join(score))

if __name__ == '__main__':
    main()
