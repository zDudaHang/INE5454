
from typing import List


class PortalSCCrawlerState():
    def __init__(
            self,
            actual_processing_situacao_page: int = -1,
            total_of_pages_processing_situacao: int = -1,
            actual_processing_situacao: str = '',
            full_extracted_situacoes: List[str] = []):
        self.actual_processing_situacao_page = actual_processing_situacao_page
        self.total_of_pages_processing_situacao = total_of_pages_processing_situacao
        self.actual_processing_situacao = actual_processing_situacao
        self.full_extracted_situacoes = full_extracted_situacoes

    def __str__(self):
        return f"""
        Situação que estava sendo processada: {self.actual_processing_situacao}
        Página atual / Total de páginas: {self.actual_processing_situacao_page}/{self.total_of_pages_processing_situacao}
        Situações completamente processadas: {self.full_extracted_situacoes}
        """
