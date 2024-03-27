from __future__ import annotations
from typing import List

from htmlparser.tokenizer.tokens import TokenType

mdTokens = {
        "#": TokenType.H1,
        "##": TokenType.H2,
        "###": TokenType.H3,
        "`": TokenType.CODE,
        }

class MdNode(object):
    type: TokenType
    children: List[MdNode | str]

    def __init__(self, type: TokenType, children: List[MdNode | str]):
        self.type = type
        self.children = children

    def __repr__(self) -> str:
        return "MdNode{ type={" + self.type.__repr__() + "}, children=" + self.children.__repr__() + " }"

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, MdNode):
            return False
        return self.type.__eq__(value.type) and self.children.__eq__(value.children)

def createMdNode(ttype: TokenType, text: str) -> MdNode:
    children = list()
    children.append(text)
    return MdNode(ttype, children)

class MdParser(object):
    source: str
    start: int
    current: int
    char: str
    tokens: List[MdNode]

    def __init__(self, source: str) -> None:
        self.source = source
        self.current = -1
        self.start = self.current
        self.advance()

    def readLines(self) -> List[MdNode]:
        tokens = []
        while self.char != '':
            token = self.readLine()
            if token:
                tokens.append(token)
        return tokens

    def readLine(self) -> MdNode | None:
        self.start = self.current
        nodeType = TokenType.P
        match self.char: 
            case '':
                return None
            case '#':
                while self.char == '#':
                    self.advance()
                nodeType = mdTokens.get(self.source[self.start:self.current], TokenType.P)
                if nodeType != TokenType.P:
                    self.advance()
                    self.start = self.current
            case '`':
                self.advance()
                node = self.readCode()
                self.advance()
                return node
            case '\n':
                self.eatWhitespace()
                return self.readLine()
        children = list()
        while self.char not in ('\n', ''):
            if self.char == '`':
                children.append(self.source[self.start:self.current])
                self.advance()
                children.append(self.readCode())
                self.advance()
                self.start = self.current
            self.advance()
        children.append(self.source[self.start:self.current])
        return MdNode(nodeType, children)

    def readCode(self) -> MdNode:
        self.start = self.current
        while self.char != '`' and self.char != '':
            self.advance()
        if self.char == '':
            return createMdNode(TokenType.P, self.source[self.start:self.current])
        return createMdNode(TokenType.CODE, self.source[self.start:self.current])

    def eatWhitespace(self):
        while self.char in ("\n", "\r", "\t", " "):
            self.source = self.source[:self.current] + self.source[self.current + 1:]
            if self.current < len(self.source):
                self.char = self.source[self.current]
            else:
                self.char = ''

    def advance(self) -> None:
        if self.current < len(self.source) - 1:
            self.current += 1
            self.char = self.source[self.current]
        else:
            self.current = len(self.source)
            self.char = ''

    def peek(self) -> str:
        if self.current < len(self.source) - 1:
            return self.source[self.current + 1]
        else:
            return ''
