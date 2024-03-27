from typing import List
import unittest as test

from htmlparser.tokenizer.tokens import TokenType
from mdparser.classes.mdparser import MdNode, MdParser, createMdNode

class MdTests(test.TestCase):
    def test_h1(self):
        input = '''# teste'''
        parser = MdParser(input)
        nodes = parser.readLines()
        shouldBe: List[MdNode] = list()
        shouldBe.append(createMdNode(TokenType.H1, "teste"))
        self.assertEqual(nodes, shouldBe)

    def test_h2(self):
        input = '''## teste'''
        parser = MdParser(input)
        nodes = parser.readLines()
        shouldBe: List[MdNode] = list()
        shouldBe.append(createMdNode(TokenType.H2, "teste"))
        self.assertEqual(nodes, shouldBe)

    def test_h3(self):
        input = '''### teste'''
        parser = MdParser(input)
        nodes = parser.readLines()
        shouldBe: List[MdNode] = list()
        shouldBe.append(createMdNode(TokenType.H3, "teste"))
        self.assertEqual(nodes, shouldBe)

    def test_p(self):
        input = '''teste'''
        parser = MdParser(input)
        nodes = parser.readLines()
        shouldBe: List[MdNode] = list()
        shouldBe.append(createMdNode(TokenType.P, "teste"))
        self.assertEqual(nodes, shouldBe)

    def test_code(self):
        input = '''`
teste
hello
`'''
        parser = MdParser(input)
        nodes = parser.readLines()
        shouldBe: List[MdNode] = list()
        shouldBe.append(createMdNode(TokenType.CODE, "\nteste\nhello\n"))
        self.assertEqual(nodes, shouldBe)

    def test_whitespace(self):
        input = '''
        ### teste
            # hello
            '''
        parser = MdParser(input)
        nodes = parser.readLines()
        shouldBe: List[MdNode] = list()
        shouldBe.append(createMdNode(TokenType.H3, "teste"))
        shouldBe.append(createMdNode(TokenType.H1, "hello"))
        self.assertEqual(nodes, shouldBe)

    def test_inline_code(self):
        input = '''
teste `codigo` teste
'''
        parser = MdParser(input)
        nodes = parser.readLines()
        shouldBe: List[MdNode] = list()
        shouldBe.append(MdNode(TokenType.P, ["teste ", createMdNode(TokenType.CODE, "codigo"), " teste"]))
        self.assertEqual(nodes, shouldBe)
