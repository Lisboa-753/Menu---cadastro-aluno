#criando uma classe
class Aluno :

    #ctor
    def __init__(self, nome, ra, email, disciplina = None, id = None) :
        self.id = id
        self.nome = nome
        self.ra = ra
        self.email = email
        self.disciplina = disciplina