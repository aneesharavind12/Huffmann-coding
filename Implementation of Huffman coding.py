import heapq
import os.path


class BinaryTreeNode :
    def __init__(self,value,frequency):
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        if self.frequency < other.frequency :
            return True
        else :
            return False

    def __eq__(self, other):
        if self.frequency == other.frequency :
            return True
        else :
            return False



class HuffmanCoding :
    def __init__(self,path):
        self.path = path
        self.__heap = []
        self.__Codes = {}
        self.__reverseCodes = {}

    def make_frequency_dict(self,text):
        char_dict = {}
        for char in text :
            if char not in char_dict :
                char_dict[char] = 0
            char_dict[char] += 1

        return char_dict

    def __Build_heap(self,freq_dict):
        for key in freq_dict :
            frequency = freq_dict[key]
            binary_tree_node = BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,binary_tree_node)

    def __Build_Tree(self):
        while(len(self.__heap) > 1) :
            binary_tree_node1 = heapq.heappop(self.__heap)
            binary_tree_node2 = heapq.heappop(self.__heap)
            freq_sum = binary_tree_node1.frequency + binary_tree_node2.frequency
            newNode = BinaryTreeNode(None,freq_sum)
            newNode.left = binary_tree_node1
            newNode.right = binary_tree_node2
            heapq.heappush(self.__heap,newNode)

    def __BuildCodesHelper(self,root,curr_bits):
        if root is None :
            return
        if root.value is not None :
            self.__Codes[root.value] = curr_bits
            self.__reverseCodes[curr_bits] = root.value
        self.__BuildCodesHelper(root.left,curr_bits + "0")
        self.__BuildCodesHelper(root.right,curr_bits + "1")


    def __BuildCodes(self):
        root = heapq.heappop(self.__heap)
        self.__BuildCodesHelper(root,"")

    def __getEncodedText(self,text):
        encoded_text = ""
        for char in text :
            encoded_text += self.__Codes[char]
        return encoded_text

    def getPaddedEncodedText(self,encoded_text):
        padded_amount = 8 - (len(encoded_text)%8)
        for i in range(padded_amount) :
            encoded_text += "0"
        padded_info = "{0:08b}".format(padded_amount)
        padded_encoded_text = encoded_text + padded_info
        return padded_encoded_text

    def __getBytesArray(self,padded_encoded_text):
        byte_array = []
        for i in range(0,len(padded_encoded_text),8) :
            byte = padded_encoded_text[i:i+8]
            byte_array.append(int(byte,2))

        return byte_array


    def Compress(self):
        #get file from path and read text from file
        file_name,file_extension = os.path.splitext(self.path)
        output_path = file_name + ".bin"

        with open(self.path,'r+') as file,open(output_path,'wb') as output :
            text = file.read()
            text = text.rstrip()

            # Construct a Frequency Dictionary using the text
            freq_dict = self.make_frequency_dict(text)

            # Construct a Heap using Frequency Dictionary
            self.__Build_heap(freq_dict)

            # Construct a Binary Tree using Heap
            self.__Build_Tree()

            # Building codes from the Binary Tree
            self.__BuildCodes()

            # Create the Encoded texts using the codes
            encoded_text = self.__getEncodedText(text)

            # pad the encoded text
            padded_encoded_text = self.getPaddedEncodedText(encoded_text)

            # Converting Bytes
            bytes_array = self.__getBytesArray(padded_encoded_text)
            final_byte = bytes(bytes_array)

            # Compressing file
            output.write(final_byte)

        print("Compressed")
        return output_path

    def __removePadding(self,text):
        padded_info = text[:8]
        extra_padding_amount = int(padded_info,2)
        text = text[8:]
        text_after_removing_padding = text[:-1*extra_padding_amount]
        return text_after_removing_padding

    def __Decoded_text(self,text):
        decoded_text = ""
        current_bits = ""
        for bits in text :
            current_bits += bits
            if current_bits in self.__reverseCodes :
                character = self.__reverseCodes[current_bits]
                decoded_text += character
                current_bits = ""
        return decoded_text

    def Decompress(self,input_path):
        file_name,file_extension = os.path.splitext(input_path)
        output_path = file_name + "_decompressed" + ".txt"
        with open(input_path,"rb") as file , open(output_path,"w") as output :
            bit_string = ""
            byte = file.read(1)
            while byte : #this will iterate till there is no byte
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,"0")
                bit_string += bits
                byte = file.read(1)

            actual_string = self.__removePadding(bit_string)
            decompressed_text = self.__Decoded_text(actual_string)
            output.write(decompressed_text)



path = "C:\Aneesh\sample1.txt"
h = HuffmanCoding(path)
output_path = h.Compress()
h.Decompress(output_path)

