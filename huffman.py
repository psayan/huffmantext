# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 19:58:44 2014

@author: sayan
"""

#! /usr/bin/python
# -*- coding: latin-1 -*-
from sys import argv, getsizeof
from math import ceil, floor
from subprocess import call
from random import randint, choice
from time import time
import pygraphviz
 
class Huffman:
 
    def get_frequency(self, text):
        frequency = dict()
        for i in text:
            if i in frequency:
                frequency[i] += 1
            else:
                frequency[i] = 1.0
        return frequency
 
    def sort(self, frequency):
        res = list()
        for i in range(len(frequency.keys())):
            values = frequency.keys()
            min_value = (values[0], frequency[values[0]], 0)
            for j in range(len(values)):
                if frequency[values[j]] < min_value[1]:
                    min_value = (values[j], frequency[values[j]], j)
            res.append( [min_value[0], frequency.pop(min_value[0]), -1, ''] )
        return res
 
    def calculate_nodes(self, n):
        res = 0
        res += n
        while n > 1:
            if n % 2 == 0:
                res += (n/2)
                n /= 2
            else:
                res += ((n-1)/2)
                n = ((n-1)/2) + 1
        return res
 
 
    def build_tree(self, frequency):
        # write graph
        Tree = pygraphviz.AGraph(directed=True, strict=True)
 
        number_nodes = self.calculate_nodes(len(frequency))        
        graph = [[0]*number_nodes for i in range(number_nodes)]
        graph_guide = dict()
        chars_positions = dict()
        used_positions = -1
        
        while len(frequency) > 1:
            suma = frequency[0][1] + frequency[1][1]
            nodo = [str(suma), suma, used_positions+1, '']
            graph_guide[used_positions+1] = nodo
            used_positions += 1
 
            #Hacer arbol aqui
            subnodo1 = frequency[0]
            subnodo2 = frequency[1]
            subnodo1[3] = '0'
            subnodo2[3] = '1'
 
            if subnodo1[2] == -1:
                subnodo1[2] = used_positions+1
                graph_guide[used_positions+1] = subnodo1
                used_positions += 1
                chars_positions[subnodo1[0]] = subnodo1[2]
 
            if subnodo2[2] == -1:
                subnodo2[2] = used_positions+1
                graph_guide[used_positions+1] = subnodo2
                used_positions += 1
                chars_positions[subnodo2[0]] = subnodo2[2]
 
            ################################
            nodo[0] += '('+str(nodo[2])+')'
            Tree.add_edge(subnodo1[0], nodo[0], color = 'blue', label = '0')
            Tree.add_edge(subnodo2[0], nodo[0], label = '1')
 
#            print subnodo1, "->", nodo
#            print subnodo2, "->", nodo
 
            graph[subnodo1[2]][nodo[2]] = 1
            graph[nodo[2]][subnodo1[2]] = -1
            graph[subnodo2[2]][nodo[2]] = 1
            graph[nodo[2]][subnodo2[2]] = -1
 
            frequency = frequency[2:]
            length = len(frequency)
            if length == 0:
                frequency.append(nodo)
            else:
                for i in range(length):
                    if frequency[i][1] > nodo[1]:
                        frequency.insert(i-1, nodo)
                        break
                    if i == length-1:
                        frequency.append(nodo)
 
        #To save the tree graph and create an ps file
        chars_positions["root"] = nodo[2]
        Tree.layout(prog='dot')
        Tree.write('output.dot')
        call(['dot', '-Tps', 'output.dot', '-o', 'output.ps'])
 
        return graph, chars_positions, graph_guide
 
    def get_connections(self, graph, pos, graph_guide, direction = 1):
        con = list()
        for j in range(len(graph[pos])):
            if graph[pos][j] == direction:
                con.append(j)
        return con
 
    def build_encoding_dictionary(self, graph, basic_chars, graph_guide):
        encoding_dictionary = dict()
        for i in basic_chars.keys():
            pos = basic_chars[i]
            char = graph_guide[pos][3]
            while False is not True:
                if pos == basic_chars["root"]:
                    break
                con = self.get_connections(graph, pos, graph_guide)                
                pos = con[0]
                char += graph_guide[con[0]][3]
 
            encoding_dictionary[i] = char[::-1]
        return encoding_dictionary
 
    def encode(self, text):
        frequency = self.get_frequency(text)
        frequency = self.sort(frequency)
        graph, chars_positions, graph_guide = self.build_tree(frequency)
        encoding = self.build_encoding_dictionary(graph, chars_positions, graph_guide)
        res = ''
        for i in text:
            res += encoding[i]
 
        return res, encoding, graph, chars_positions, graph_guide
 
    def decode(self, text, graph, chars_pos, graph_guide):
        length = len(text)
        text_pos = 0
        graph_pos = chars_pos['root']
        decoded = ''
        while text_pos < length:
            con = self.get_connections(graph, graph_pos, graph_guide, direction = -1)
            if len(con) > 0:
                for i in con:
                    if str(graph_guide[i][3]) == text[text_pos]:
                        graph_pos = i
                text_pos += 1
            else:
                decoded += graph_guide[graph_pos][0]
                graph_pos = chars_pos['root']
        decoded += graph_guide[graph_pos][0]
 
        return decoded
 
def generar_caso_normal(n):
    caracteres = (("A", 12.53), ("B", 1.42), ("C", 4.68), ("D", 5.86), ("E", 13.68), ("F", 0.69), ("G", 1.01), ("H", 0.70), ("I", 6.25), ("J", 0.44), ("K", 0.01), ("L", 4.97), ("M", 3.15), ("N", 6.71), ("O", 8.68), ("P", 2.51), ("Q", 0.88), ("R", 6.87), ("S", 7.98), ("T", 4.63), ("U", 3.93), ("V", 0.90), ("W", 0.02), ("X", 0.22), ("Y", 0.90), ("Z", 0.52))
    acumulada = list()
    suma = 0.0
    text = ''
    for i in caracteres:
        suma += i[1]
        acumulada.append(suma)
    length = len(acumulada)
 
    for i in range(n):
        eleccion = randint(0, int(floor(acumulada[length-1])))
        for j in range(length):
            if acumulada[j] > eleccion:
                text += caracteres[j-1][0]
                break
    return text
 
def generar_peor_caso(n):
    caracteres = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P" "Q", "R", "S", "T", "U", "V", "W", "X", "Y" "Z")
    text = ''
    for i in range(n):
        text += choice(caracteres)
    return text
 
def test(max_chars = 1000):
    h = Huffman()
    fl = open("output.dat", "w")
    for i in range(5, maxi_chars+1):
        print i
        texto_normal = generar_caso_normal(i)
        texto_peor = generar_peor_caso(i)
 
        before = time()
        encoded_normal, dictionary, graph, chars_pos, graph_guide = h.encode(texto_normal)
        normal_encode_time = time() - before
        
        before = time()
        decoded_normal =  h.decode(encoded_normal, graph, chars_pos, graph_guide)
        normal_decode_time = time() - before
 
        memoria_normal = getsizeof(graph) + getsizeof(chars_pos) + getsizeof(graph_guide)
        # bits del texto comprimido + peso del grafo / peso del texto original
        radio_compresion_normal = ( float(len(encoded_normal)+memoria_normal) / ( getsizeof(texto_normal[0])*len(texto_normal)*8) )
 
        before = time()
        encoded_peor, dictionary, graph, chars_pos, graph_guide = h.encode(texto_peor)
        peor_encode_time = time() - before
 
        before = time()
        decoded_peor =  h.decode(encoded_peor, graph, chars_pos, graph_guide)
        peor_decode_time = time() - before
 
        memoria_peor = getsizeof(graph) + getsizeof(chars_pos) + getsizeof(graph_guide)
        radio_compresion_peor = ( float(len(encoded_peor)+memoria_peor) / ( getsizeof(texto_peor[0])*len(texto_peor)*8) )
        fl.write(str(i)+' '+str(normal_encode_time)+' '+str(normal_decode_time)+' '+str(peor_encode_time)+' '+str(peor_decode_time)+' '+str(memoria_normal)+' '+str(memoria_peor)+' '+str(radio_compresion_normal)+' '+str(radio_compresion_peor)+'\n')
    fl.close()
 
def main():
    h = Huffman()
    text = 'Huffman'
 
    print 'Encoding...'
    encoded, dictionary, graph, chars_pos, graph_guide = h.encode(text)
    print 'Encoding dictionary:', dictionary
    print 'Original text:', text
    print 'Encoded text:', encoded
    print 'Compression ratio (compressed / original):', (float(len(encoded)) / (getsizeof(text[0])*len(text)*8) )
 
    print 'Decoding...'
    decoded_text =  h.decode(encoded, graph, chars_pos, graph_guide)
    print 'Original text:', encoded
    print 'Decoded text:', decoded_text
 
main()
#test()