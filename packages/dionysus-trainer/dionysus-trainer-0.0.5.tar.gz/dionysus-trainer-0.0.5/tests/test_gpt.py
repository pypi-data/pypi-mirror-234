
import unittest
import torch
import torch.nn as nn

from src.dionysus.models import Config, GPT1


class TestGPT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
      self.config =  Config(vocab_size = 26,
                            dim_embeddings = 3,
                            dim_context = 5,
                            num_heads = 3,
                            n_layer = 2,
                            dropout = 0.2)
      
    def test_get_block_size(self):
        idx = torch.tensor([[1]])
        T_actual = idx.shape[-1]
        _, T_expected = idx.shape
        self.assertTrue(T_actual == T_expected)
    
        idx = torch.tensor([[1, 2, 3]])
        T_actual = idx.shape[-1]
        _, T_expected = idx.shape
        self.assertTrue(T_actual == T_expected)

    def test_get_block_size_no_batch(self):
        idx = torch.tensor([1])
        T_actual = idx.shape[-1]
        T_expected = 1
        self.assertTrue(T_actual == T_expected)

        idx = torch.tensor([1, 2, 3])
        T_actual = idx.shape[-1]
        T_expected = 3
        self.assertTrue(T_actual == T_expected)

    def test_output_dim_embedding(self):
        """
        Embedding layer adds dimension: idx -> dim_embedding
        """
        dim_embedding = 3
        token_embedding_table = nn.Embedding(num_embeddings=5, embedding_dim=dim_embedding)

        idx = torch.tensor([1])
        dim_context = 1
        embedding = token_embedding_table(idx)
        self.assertTrue(embedding.shape == (dim_context, dim_embedding))

        idx = torch.tensor([1,
                            3,
                            4])
        dim_context = 3
        embedding = token_embedding_table(idx)
        self.assertTrue(embedding.shape == (dim_context, dim_embedding))


        idx = torch.tensor([[1,
                            3,
                            4]])
        dim_context = 3
        batch_size = 1
        embedding = token_embedding_table(idx)
        self.assertTrue(embedding.shape == (batch_size, dim_context, dim_embedding))


        idx = torch.tensor([[1,
                            3,
                            4], 
                            
                            [3,
                             4,
                             0]])
        dim_context = 3
        batch_size = 2
        embedding = token_embedding_table(idx)
        self.assertTrue(embedding.shape == (batch_size, dim_context, dim_embedding))

    def test_single_token_input_bigram(self):
        x = torch.tensor([[1]])
        model = GPT1(self.config)

        logits = model(x)
        self.assertTrue(logits.shape == (1, 1, self.config.vocab_size))

    def test_single_token_input_bigram1(self):
        x = torch.tensor([1])
        model = GPT1(self.config)

        logits = model(x)
        self.assertTrue(logits.shape == (1, self.config.vocab_size))


if __name__ == "__main__":
    unittest.main() 
    