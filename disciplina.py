class Disciplina :

    def __init__(self, nome, nome_professor, carga_horaria, codigo = None) :
        self.codigo = codigo
        self.nome = nome
        self.nome_professor = nome_professor
        self.carga_horaria = carga_horaria