from ordered_list import *
from huffman_bit_writer import *
from huffman_bit_reader import *


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # stored as an integer - the ASCII character code value
        self.freq = freq  # the freqency associated with the node
        self.left = None  # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return type(self) == type(other) and self.freq == other.freq

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq < other.freq:
            return True
        elif self.freq > other.freq:
            return False
        else:
            if self.char < other.char:
                return True
            else:
                return False


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file'''
    c_freq = [0] * 256
    infile = open(filename, "r")
    list_lines = infile.readlines()
    for line in list_lines:
        for char in line:
            c_freq[ord(char)] += 1
    infile.close()
    return c_freq


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    lst_node = OrderedList()
    for i in range(len(char_freq)):
        if not char_freq[i] == 0:
            lst_node.add(HuffmanNode(i, char_freq[i]))
    if lst_node.size() == 0:
        return None
    if lst_node.size() == 1:
        return lst_node.pop(0)
    while lst_node.size() > 1:
        n1 = lst_node.pop(0)
        n2 = lst_node.pop(0)
        if n1.char < n2.char:
            temp = n1.char
        else:
            temp = n2.char
        new_n = HuffmanNode(temp, n1.freq + n2.freq)
        new_n.left = n1
        new_n.right = n2
        lst_node.add(new_n)
    return lst_node.pop(0)


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    lst_codes = [""] * 256
    current_code = ""
    if node is not None:
        return create_code_helper(node, lst_codes, current_code)
    else:
        return None


def create_code_helper(node, lst_codes, code):
    if node.right is None and node.left is None:
        lst_codes[node.char] = code
    else:
        create_code_helper(node.right, lst_codes, code + str("1"))
        create_code_helper(node.left, lst_codes, code + str("0"))
    return lst_codes


def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    return_str = ""
    for i in range(len(freqs)):
        if not freqs[i] == 0:
            if return_str == "":
                return_str = str(i) + " " + str(freqs[i])
            else:
                return_str = return_str + " " + str(i) + " " + str(freqs[i])
    return return_str


def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take note of special cases - empty file and file with only one unique character'''
    try:
        infile = open(in_file, "r")
    except FileNotFoundError as error:
        raise error
    else:
        outfile = open(out_file, "w")
        lst_cnt_freq = cnt_freq(in_file)
        header = create_header(lst_cnt_freq)
        code = create_code(create_huff_tree(lst_cnt_freq))
        list_lines = infile.readlines()
        if len(list_lines) == 0:
            outfile.write(header)
        else:
            outfile.write(header + "\n")
        for line in list_lines:
            for char in line:
                outfile.write(code[ord(char)])
        infile.close()
        outfile.close()

        outfile = open(out_file, "r")
        outfile.readline()
        code = outfile.readline()
        hbw = HuffmanBitWriter(out_file[:-4] + "_compressed.txt")
        if len(code) == 0 or len(code) == 1:
            hbw.write_str(header)
        else:
            hbw.write_str(header + "\n")
        hbw.write_code(code)
        hbw.close()
        outfile.close()


def huffman_decode(encoded_file, decoded_file):
    try:
        hbr = HuffmanBitReader(encoded_file)
    except FileNotFoundError as error:
        raise error
    else:
        d_file = open(decoded_file, "w")
        header_str = hbr.read_str()
        c_freq = parse_header(header_str)
        current_node = create_huff_tree(c_freq)
        # if current_node.right is None and current_node.left is None:
        #     pass
        root = create_huff_tree(c_freq)
        while True:
            try:
                bit = hbr.read_bit()
            except struct.error:
                break
            if current_node.left is None and current_node.right is None:
                ch = chr(current_node.char)
                d_file.write(ch)
                current_node = root
            if bit:
                current_node = current_node.right
            else:
                current_node = current_node.left
        hbr.close()
        d_file.close()


def parse_header(header_string):
    c_freq = [0] * 256
    lst_header = header_string.split()
    for i in range(0, len(lst_header)-1, 2):
        c_freq[int(lst_header[i])] = int(lst_header[i+1])
    return c_freq

