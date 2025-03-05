class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0
    
    def adicionar(self, dado):
        novo_no = No(dado)
        
        if not self.cabeca:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no
        
        self.tamanho += 1
    
    def remover(self, dado):
        if not self.cabeca:
            raise ValueError("Lista vazia")
        
        if self.cabeca.dado == dado:
            self.cabeca = self.cabeca.proximo
            self.tamanho -= 1
            return
        
        atual = self.cabeca
        while atual.proximo:
            if atual.proximo.dado == dado:
                atual.proximo = atual.proximo.proximo
                self.tamanho -= 1
                return
            atual = atual.proximo
        
        raise ValueError("Dado não encontrado")
    
    def __iter__(self):
        atual = self.cabeca
        while atual:
            yield atual.dado
            atual = atual.proximo
    
    def __len__(self):
        return self.tamanho