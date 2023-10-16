from abc import ABC, abstractmethod
from Bio.SeqRecord import SeqRecord
from Bio.PDB.Structure import Structure
import torch.nn as nn


class HuggingFacePredictor(ABC):

    def __init__(self, model: nn.Module):
        self.model = model

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def predict(self, job_id: str, record: SeqRecord) -> Structure:
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        import torch
        torch.cuda.empty_cache()
