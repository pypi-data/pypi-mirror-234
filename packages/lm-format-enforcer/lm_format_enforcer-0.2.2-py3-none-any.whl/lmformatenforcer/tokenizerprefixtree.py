from typing import Dict, List
from transformers.tokenization_utils import PreTrainedTokenizerBase

class TokenizerPrefixTreeNode:
    def __init__(self):
        self.tokens: List[int] = []
        self.children: Dict[str, TokenizerPrefixTreeNode] = {}

class TokenizerPrefixTree:
    def __init__(self, tokenizer: PreTrainedTokenizerBase):
        self.tokenizer = tokenizer
        self.token_0 = tokenizer.encode("0")[-1]
        self.root = TokenizerPrefixTreeNode()
        self.json_freetext_tokens: List[int] = []
        for token_idx in range(self.tokenizer.vocab_size):
            if token_idx in self.tokenizer.all_special_ids:
                continue
            decoded = self._decode_single_token(token_idx)
            self._add_token_to_tree(decoded, token_idx, self.root)
            # Performance optimization - cache the tokens of all the strings that don't contain a quote in the middle.
            # When we are in a JSON freetext string field, they will all be permitted and this will save a lot of tree iterations.
            if '"' not in decoded or decoded.index('"') == len(decoded) - 1:
                self.json_freetext_tokens.append(token_idx)

    def _add_token_to_tree(self, token_str: str, token_idx: int, node: TokenizerPrefixTreeNode):
        for character in token_str:
            if character not in node.children:
                node.children[character] = TokenizerPrefixTreeNode()
            node = node.children[character]
        node.tokens.append(token_idx)

    def _decode_single_token(self, token: int) -> str:
        # We prepend token 0 and skip the first letter of the result to get a space if the token is a start word.
        decoded = self.tokenizer.decode([self.token_0, token])[1:]
        return decoded