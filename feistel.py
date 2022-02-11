from helpers import *

"""
    Implementation of a single round of a Feistel network
    
    This implementation will encrypt 64bit input with
    64bit key (key is created using a PRNG)
    
    ***Because of the short key length, this encryption method is
    unable to withstand brute-force attacks. This is why DES is
    no longer secure***
    
    Check https://en.wikipedia.org/wiki/Data_Encryption_Standard
    for more information about the algorithm
    
    """

def feistel(input, key):
    output = []
    """INPUT"""
    permuted_input = initPermute(input)
    left_half = splitInput(permuted_input)[0]
    left_half_output = splitInput(permuted_input)[1]


    """KEY SCHEDULE"""
    # 64bit key -> 48bit key
    key_48 = keySchedule(key)

    """ROUND FUNCTION"""
    # expand right half 32bit -> 48bit
    expanded_right_half = expand(left_half_output)

    # key xor input
    xor_key_input = xor(expanded_right_half, key_48)

    # S-boxes
    s_box_output = []

    # split into eight sections
    bit_blocks = list(split(xor_key_input, 8))

    # run s1-box for all eight sections
    for s in range(len(bit_blocks)):
        s_box_output += s_box_function(bit_blocks[s], s)

    # P-box permutation
    round_function_output = permute_round(s_box_output)

    final_rightHalf = xor(left_half, round_function_output)

    # first add left half
    output += left_half_output
    # then right half
    output += final_rightHalf

    # final permutatation
    final_output = finalPermute(output)
    return final_output

print(feistel(test, key_64))