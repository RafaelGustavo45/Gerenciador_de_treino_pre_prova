# Gerenciador_de_treino_pre_prova


# Pré-projeto — Definição do Entregável

- **Prazo:** Previsto 14/07/2026  
- **Formato:** Documento Markdown no repositório do projeto (`docs/pre_projeto.md`) ou PDF de 2–4 páginas  
  - Alunos devem portanto escolher um mantenedor que enviará o link do repositório do projeto nesta etapa.
  - O professor deverá ter acesso ao repositório durante o desenvolvimento.
 - **Objetivo:** Convencer o professor de que a ideia é viável, útil e do tamanho certo.

---

## Estrutura Obrigatória

### 1. Identificação da Equipe
- Gerenciador de Treino pré prova
- Rafael Gustavo Reinert (mantenedor), Gustavo Pimentel Borga, Gabriel
- githubs: RafaelGustavo45, (falta colocar)
- Rafael: banco de dados
- Gustavo: Front-end e lógica de tratamento dos dados recebidos e envio
- Gabriel: API (back-end)
### 2. Elevator Pitch (máx. 3 frases)
> *"Para Estudantes que realizam a tecnica de elaborar uma prova do proprio conteudo como técnica de estudo, Gerenciador de treino pré prova é uma aplicação web que permite a criação de tais treinos. Diferente de usar o word, nosso diferencial é ser uma aplicação estruturada para isso que permite tampar a resposta."*

### 3. Público-Alvo e Contexto
- Quem vai usar?: Estudantes
- Em que situação?: No computador
- Por que isso é melhor que planilha/papel/WhatsApp?: Por ser direcionado a isso com um formulário próprio e ocultação das respostas

### 4. Funcionalidades principais (máximo 5)
Liste o que a aplicação **deve fazer** para ser considerada terminada.  
Use o formato: *"Como [usuário], quero [ação] para [resultado]"*.

Exemplo:

Como estudante

1. Como estudante, quero registrar provas para futuro treino
2. Como estudante, quero editar provas para caso algo errado tenha sido cadastrado
3. Como estudante, quero excluir uma prova caso já tenha dominado
4. Como estudante, quero treinar em simulado uma prova registrada


Requisitos:
1. Cadastrar provas com titulo, série e matéria
2. Buscar provas por titulo
3. Elaborar questões:
3.1. Com limite de questões de no maximo 20
3.2. Escrevendo a questão
3.3. Escrevendo cada alternativa
3.3.1 Definindo uma alternativa como a correta
4. Salvar a prova
5. Treinar a prova
5.1. Assinalando as alternativas de cada questão
5.2. Obtendo resultado final com questões acertadas e erradas

### 5. Escopo Negativo — O que NÃO faremos
Liste explicitamente o que parece esperado em uma aplicação com a sua finalidade, mas está **fora** do projeto.  

- Não usaremos cartões respostas
- Não colocaremos pesos por questão (valor igual)

### 6. Modelo de Dados Preliminar
Liste as **entidades** (tabelas) e seus **relacionamentos** em português simples.  
Não precisa ser diagrama formal.

```
tabela provas
campos: id int autoincremento, titulo varchar(60), série int, matéria varchar(40)

tabela questoes
campos: id int autoincremento, fk_id_prova (relacionamento com provas), texto varchar(1000)

tabela alternativas
campos: id int autoincremento, fk_id_questao (relacionamento com questoes), texto varchar(100)

tabela gabarito
campos: id int autoincremento, fk_id_alternativa (relacionamento com alternativas)
```

### 8. Wireframes (obrigatório)
Anexe **fotos de rabiscos no papel** ou screenshots de ferramentas simples (Excalidraw, draw.io, Figma, Paint).  
Deve haver:

- Ao menos uma tela para **computador**
- Ao menos uma tela para **celular**

está em telas_prototipo

### 9. Stack Confirmado
Confirme que usarão:
- [X] Flask + Jinja2
- [X] SQLite/PostgreSQL/MariaDB
- [X] HTML + CSS Grid + JS Vanilla
- [X] GitHub com PRs

Justifique em uma frase cada biblioteca adicional (não built-in) que planejam utilizar.

### 10. Autoavaliação de Riscos
Responda honestamente:

1. Qual é a parte que vocês **mais temem** implementar?
R: A lógica da criação do formulário e de responder a questão
3. O que acontece se um membro da equipe sumir 1 semana antes da entrega?
R: Pelo planejamento oficial terminaremos 1 semana antes da entrega, então será só para aperfeiçoar
4. Qual é o "caminho feliz" mínimo que entrega valor mesmo se tudo mais falhar?
R: Conseguir criar uma prova de treino e responder recebendo o que errou
