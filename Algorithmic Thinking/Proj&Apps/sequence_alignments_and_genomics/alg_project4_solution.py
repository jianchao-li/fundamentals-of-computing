"""
Project 4 - Computing alignments of sequences
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Build the scoring matrix.
    """
    scoring_matrix = {}
    for alpha1 in alphabet:
        score = {}
        for alpha2 in alphabet:
            if alpha2 == alpha1:
                score[alpha2] = diag_score
            else:
                score[alpha2]= off_diag_score
        score['-'] = dash_score
        scoring_matrix[alpha1] = score
    score = {}
    for alpha in alphabet:
        score[alpha] = dash_score
    score['-'] = dash_score
    scoring_matrix['-'] = score
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Compute global/local alignment matrix.
    """
    rows, cols = len(seq_x), len(seq_y)
    alignment_matrix = [[0 for dummy_col in range(cols + 1)] for dummy_row in range(rows + 1)]
    for row in range(1, rows + 1):
        alignment_matrix[row][0] = alignment_matrix[row - 1][0] + scoring_matrix[seq_x[row - 1]]['-']
        if not global_flag and alignment_matrix[row][0] < 0:
            alignment_matrix[row][0] = 0
    for col in range(1, cols + 1):
        alignment_matrix[0][col] = alignment_matrix[0][col - 1] + scoring_matrix['-'][seq_y[col - 1]]
        if not global_flag and alignment_matrix[0][col] < 0:
            alignment_matrix[0][col] = 0
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            diag = alignment_matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]
            left = alignment_matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-']
            top = alignment_matrix[row][col - 1] + scoring_matrix['-'][seq_y[col - 1]]
            alignment_matrix[row][col] = max(diag, left, top)
            if not global_flag and alignment_matrix[row][col] < 0:
                alignment_matrix[row][col] = 0
    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Compute global pairwise sequence alignment.
    """
    row, col = len(seq_x), len(seq_y)
    score = alignment_matrix[row][col]
    align_x, align_y = "", ""
    while row > 0 and col > 0:
        if alignment_matrix[row][col] == alignment_matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]:
            align_x = seq_x[row - 1] + align_x
            align_y = seq_y[col - 1] + align_y
            row -= 1
            col -= 1
        elif alignment_matrix[row][col] == alignment_matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-']:
            align_x = seq_x[row - 1] + align_x
            align_y = '-' + align_y
            row -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[col - 1] + align_y
            col -= 1
    while row > 0:
        align_x = seq_x[row - 1] + align_x
        align_y = '-' + align_y
        row -= 1
    while col > 0:
        align_x = '-' + align_x
        align_y = seq_y[col - 1] + align_y
        col -= 1
    return (score, align_x, align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Compute local pairwise sequence alignment.
    """
    rows, cols = len(seq_x), len(seq_y)
    row, col, score = 0, 0, 0
    for ridx in range(1, rows + 1):
        for cidx in range(1, cols + 1):
            if alignment_matrix[ridx][cidx] > score:
                score = alignment_matrix[ridx][cidx]
                row, col = ridx, cidx
    align_x, align_y = "", ""
    while row > 0 and col > 0 and alignment_matrix[row][col] > 0:
        if alignment_matrix[row][col] == alignment_matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]:
            align_x = seq_x[row - 1] + align_x
            align_y = seq_y[col - 1] + align_y
            row -= 1
            col -= 1
        elif alignment_matrix[row][col] == alignment_matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-']:
            align_x = seq_x[row - 1] + align_x
            align_y = '-' + align_y
            row -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[col - 1] + align_y
            col -= 1
    return (score, align_x, align_y)


###############################################################
# Codes for Application 4 - Applications to genomics and beyond
###############################################################

import math
import random
import matplotlib.pyplot as plt
import alg_application4_provided as provided

# Paths for data files
PAM50_PATH = 'G:/Resources/Courses/Algorithmic Thinking/Proj&Apps/sequence_alignments_and_genomics/alg_PAM50.txt'
HUMAN_EYELESS_PATH = 'G:/Resources/Courses/Algorithmic Thinking/Proj&Apps/sequence_alignments_and_genomics/alg_HumanEyelessProtein.txt'
FRUITFLY_EYELESS_PATH = 'G:/Resources/Courses/Algorithmic Thinking/Proj&Apps/sequence_alignments_and_genomics/alg_FruitflyEyelessProtein.txt'
CONSENSUS_PAX_PATH = 'G:/Resources/Courses/Algorithmic Thinking/Proj&Apps/sequence_alignments_and_genomics/alg_ConsensusPAXDomain.txt'
WORD_LIST_PATH = 'G:/Resources/Courses/Algorithmic Thinking/Proj&Apps/sequence_alignments_and_genomics/assets_scrabble_words3.txt'

def remove_dash(seq_in):
    """
    Remove all dashes from the sequences.
    """
    seq_out = ""
    for idx in range(len(seq_in)):
        if seq_in[idx] == '-':
            continue
        seq_out += seq_in[idx]
    return seq_out

def count_match_percentage(seq_x, seq_y):
    count = 0
    for idx in range(len(seq_x)):
        if seq_x[idx] == seq_y[idx]:
            count += 1
    return 1.0 * count / len(seq_x)

def gen_random_seqs(length):
    """
    Generating random sequences with speficied length.
    """
    acids = list("ACBEDGFIHKMLNQPSRTWVYXZ")
    seq = ""
    for dummy in range(length):
        seq += random.choice(acids)
    return seq

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Generating distribution of scores.
    """
    scoring_distribution = {}
    lst_y = list(seq_y)
    for dummy in range(num_trials):
        print dummy
        random.shuffle(lst_y)
        rand_y = ''.join(lst_y)
        alignment_matrix = compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        (score, local_seq_x, local_rand_y) = compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)
        if score in scoring_distribution.keys():
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1
    return scoring_distribution

def edit_distance(seq_x, seq_y):
    """
    Simple edit distance.
    """
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    diag_score, off_diag_score, dash_score = 2, 1, 0
    scoring_matrix = build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    alignment_matrix = compute_alignment_matrix(seq_x, seq_y, scoring_matrix, True)
    (score, align_x, align_y) = compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    return len(seq_x) + len(seq_y) - score

def check_spelling(checked_word, dist, word_list):
    """ 
    Check spelling by edist distances.
    """
    words = set([])
    for word in word_list:
        if edit_distance(checked_word, word) <= dist:
            words.add(word)
    return words

def run_app_q1():
    """
    Question 1 of application.
    """
    scoring_matrix = provided.read_scoring_matrix(PAM50_PATH)
    human_eyeless_protein = provided.read_protein(HUMAN_EYELESS_PATH)
    fruitfly_eyeless_protein = provided.read_protein(FRUITFLY_EYELESS_PATH)
    alignment_matrix = compute_alignment_matrix(human_eyeless_protein, fruitfly_eyeless_protein, scoring_matrix, False)
    (score, local_human, local_fruitfly) = compute_local_alignment(human_eyeless_protein, fruitfly_eyeless_protein, scoring_matrix, alignment_matrix)
    return (score, local_human, local_fruitfly)

def run_app_q2():
    """
    Question 2 of application.
    """
    scoring_matrix = provided.read_scoring_matrix(PAM50_PATH)
    (score, local_human, local_fruitfly) = run_app_q1()
    consensus_pax_domain = provided.read_protein(CONSENSUS_PAX_PATH)
    # local_human = remove_dash(local_human)
    local_fruitfly = remove_dash(local_fruitfly)
    # alignment_matrix = compute_alignment_matrix(local_human, consensus_pax_domain, scoring_matrix, True)
    # (score, global_human, global_consensus) = compute_global_alignment(local_human, consensus_pax_domain, scoring_matrix, alignment_matrix)
    # human_match = count_match_percentage(global_human, global_consensus)
    alignment_matrix = compute_alignment_matrix(local_fruitfly, consensus_pax_domain, scoring_matrix, True)
    (score, global_fruitfly, global_consensus) = compute_global_alignment(local_fruitfly, consensus_pax_domain, scoring_matrix, alignment_matrix)
    fruitfly_match = count_match_percentage(global_fruitfly, global_consensus)
    print fruitfly_match

def run_app_q3():
    """
    Question 3 of application.
    """
    scoring_matrix = provided.read_scoring_matrix(PAM50_PATH)
    human_eyeless_protein = provided.read_protein(HUMAN_EYELESS_PATH)
    fruitfly_eyeless_protein = provided.read_protein(FRUITFLY_EYELESS_PATH)
    human_rand = gen_random_seqs(len(human_eyeless_protein))
    fruitfly_rand = gen_random_seqs(len(fruitfly_eyeless_protein))
    alignment_matrix = compute_alignment_matrix(human_rand, fruitfly_rand, scoring_matrix, False)
    (score, local_human_rand, local_fruitfly_rand) = compute_local_alignment(human_rand, fruitfly_rand, scoring_matrix, alignment_matrix)
    print score
    print local_human_rand
    print local_fruitfly_rand
    consensus_pax_domain = provided.read_protein(CONSENSUS_PAX_PATH)
    local_human_rand = remove_dash(local_human_rand)
    alignment_matrix = compute_alignment_matrix(local_human_rand, consensus_pax_domain, scoring_matrix, True)
    (score, global_human_rand, global_consensus) = compute_global_alignment(local_human_rand, consensus_pax_domain, scoring_matrix, alignment_matrix)
    human_match = count_match_percentage(global_human_rand, global_consensus)
    print human_match
    local_fruitfly_rand = remove_dash(local_fruitfly_rand)
    alignment_matrix = compute_alignment_matrix(local_fruitfly_rand, consensus_pax_domain, scoring_matrix, True)
    (score, global_fruitfly_rand, global_consensus) = compute_global_alignment(local_fruitfly_rand, consensus_pax_domain, scoring_matrix, alignment_matrix)
    fruitfly_match = count_match_percentage(global_fruitfly_rand, global_consensus)
    print fruitfly_match

def run_app_q4():
    """
    Question 4 of application.
    """
    scoring_matrix = provided.read_scoring_matrix(PAM50_PATH)
    human_eyeless_protein = provided.read_protein(HUMAN_EYELESS_PATH)
    fruitfly_eyeless_protein = provided.read_protein(FRUITFLY_EYELESS_PATH)
    num_trials = 1000
    scoring_distribution = generate_null_distribution(human_eyeless_protein, fruitfly_eyeless_protein, scoring_matrix, num_trials)
    for score in scoring_distribution.keys():
        scoring_distribution[score] /= (1.0 * num_trials)
    plt.bar(scoring_distribution.keys(), scoring_distribution.values(), color = 'g')
    plt.grid(True)
    plt.xlabel('Scores')
    plt.ylabel('Fraction of Total Trials')
    plt.title('Normalized Scoring Distribution')
    plt.show()
    return scoring_distribution

def run_app_q5():
    """
    Question 5 of application.
    """
    scoring_distribution = run_app_q4()
    mean = 0
    for score in scoring_distribution.keys():
        mean += score * scoring_distribution[score]
    std_dev = 0
    for score in scoring_distribution.keys():
        std_dev += (score - mean) ** 2 * scoring_distribution[score]
    std_dev = math.sqrt(std_dev)
    z_score = (875 - mean) / std_dev
    print mean
    print std_dev
    print z_score

def run_app_q8(checked_word, dist):
    """
    Question 8 of application.
    """
    word_list = provided.read_words(WORD_LIST_PATH)
    words = check_spelling(checked_word, dist, word_list)
    return words

if __name__ == "__main__":
    words1 = run_app_q8('humble', 1)
    words2 = run_app_q8('firefly', 2)
    for word in words1:
        print word
    print
    for word in words2:
        print word
