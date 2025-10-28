"""
You and your friends are all fans of the hit TV show ThroneWorld and like to discuss it on social media. 
Unfortunately, some of your friends don't watch every new episode the minute it comes out. Out of consideration 
for them you would like to obfuscate your status updates so as to keep them spoiler-free.

You settle on a route cipher, which is a type of transposition cipher. 
Given a message and a number of rows and number of columns, to compute the route encryption of the message:

    - Write out the message row-wise in a grid of size rows by cols
    - then read the message column-wise.

You are guaranteed that rows * cols == len(message).

Your task is to write a function that, given a message, rows, and cols, returns the route encryption of the message.


Example:

message1 = "One does not simply walk into Mordor"
rows1 = 6
cols1 = 6

Grid:
O n e   d o
e s   n o t
  s i m p l
y   w a l k
  i n t o  
M o r d o r

transpose(message1, rows1, cols1) -> "Oe y Mnss ioe iwnr nmatddoploootlk r"


Other examples:

message2 = "1.21 gigawatts!"
rows2_1 = 5
cols2_1 = 3

Grid:
1 . 2
1   g
i g a
w a t
t s !

transpose(message2, rows2_1, cols2_1) -> "11iwt. gas2gat!"


message2 = "1.21 gigawatts!"
rows2_2 = 3
cols2_2 = 5
transpose(message2, rows2_2, cols2_2) -> "1ga.it2gt1as w!"


"""

def transpose(message, rows, cols):
    matrix = [[''] * cols for _ in range(rows)]
    for i in range(len(message)):
        r = i // cols 
        c = i % cols
        print(r,rows,c, cols)
        matrix[r][c] = message[i]
    transposed_message = []
    for c in range(cols):
        for r in range(rows):
            transposed_message.append(matrix[r][c])
    return ''.join(c for c in transposed_message)


message1 = "One does not simply walk into Mordor"
rows1 = 6
cols1 = 6
assert transpose(message1, rows1, cols1) == "Oe y Mnss ioe iwnr nmatddoploootlk r"
print()

message2 = "1.21 gigawatts!"
rows2_2 = 3
cols2_2 = 5
assert transpose(message2, rows2_2, cols2_2) == "1ga.it2gt1as w!"