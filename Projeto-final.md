# Projeto Integrador — Definições do Trabalho Final

## 1. Objetivo
Desenvolver uma aplicação web completa, do banco de dados à interface, utilizando Python/Flask como backend. O projeto deve ser funcional, bem documentado e publicado no GitHub. A equipe deve demonstrar que domina os conceitos fundamentais do curso e consegue entregar software que funciona na prática.

Uma aplicação simples que roda e entrega valor é melhor que uma arquitetura sofisticada que não funciona. Note que os requisitos a seguir devem ser suficientes para evitar uma aplicação simples *demais*.

---

## 2. Requisitos Obrigatórios (Base)

### 2.1 Frontend
- **HTML semântico** e estruturado.
- **CSS Grid** para organização do layout, com design **responsivo**.
  - Ao menos um endpoint otimizado para uso em **computador**.
  - Ao menos um endpoint otimizado para uso em **celular**.
  - Podem ser na mesma página responsiva ou páginas separadas com finalidades distintas (ex: painel administrativo no PC, interface do usuário no celular).
- **JS Vanilla** (sem frameworks como React, Vue ou Angular).
  - **API REST JSON**: Endpoint(s) consumidos pelo frontend via `fetch()` assíncrono, sem recarregar a página.
- **Acessibilidade:** aprovação em auditoria W3C e WCAG básica (contraste de cores, hierarquia de títulos, textos alternativos em imagens, semântica, foco visível em elementos interativos).

### 2.2 Banco de Dados
- **Ao menos um banco de dados relacional:** SQLite, PostgreSQL ou MariaDB.
- **Chaves estrangeiras** utilizadas para modelar relacionamentos entre entidades.
- Operações básicas de **CRUD** (Criar, Ler, Atualizar, Excluir).
- **Segurança:** proteção contra SQL Injection.
- **Script dedicado para criação do schema** (`schema.sql` ou equivalente).
- **Script dedicado para preenchimento com dados de exemplo** (`seed.py` ou equivalente), permitindo que o avaliador execute a aplicação imediatamente.

### 2.3 Backend (Python/Flask)
- Ambiente configurado com `venv`, `pip install` e `requirements.txt` (incluir outras bibliotecas úteis ao projeto além do Flask e suas dependências).
- **Templates Jinja2** para geração de páginas HTML.
- **Tratamento de erros HTTP:** páginas de erro personalizadas (ex: `@app.errorhandler(404)`, `@app.errorhandler(500)`).
- **Programação Orientada a Objetos:** ao menos uma classe Python utilizada de forma significativa (ex: modelos de dados, serviços, repositórios).
- **Exportação standalone:** ao menos um endpoint que gere um arquivo **HTML contendo dados e JS embutido**, capaz de funcionar offline no navegador do cliente (ex: relatório filtrável/pesquisável localmente, sem necessidade de servidor).
- **Autenticação:** implementação de login/logout. **Mínimo obrigatório:** sessão com senhas armazenadas como hash (nunca em texto plano). OAuth, JWT ou 2FA são bônus, não substituem o requisito mínimo.
- **Integração externa**: Consumo de API de terceiros (clima, geolocalização, etc.).

### 2.4 Versionamento e Colaboração (Git/GitHub)
- Repositório público no GitHub.
- **Pull requests de todos os membros da equipe** (histórico de contribuição individual visível).
- **Reviews com aprovação manual** do dono do repositório (ou mantenedor designado) antes do merge.
- **Credenciais:** se houver dados de acesso no repositório, devem ser documentados no README para execução imediata pelo avaliador.

### 2.5 Arquitetura e Qualidade
- **Padrão de desenvolvimento:** escolher e aplicar um padrão arquitetural - refatorar se necessário.
- **Testes unitários:** mínimo de **3 testes úteis e relevantes**, cobrindo lógica de negócio (ex: regras de validação, cálculos, permissões de acesso).
- **Diagrama(s) didático(s) da arquitetura:** formato livre, desde que represente claramente o **fluxo de dados** da aplicação.

### 2.6 Documentação
- **README.md** contendo pelo menos:
  - Descrição do projeto e funcionalidades.
  - Tecnologias/bibliotecas/aplicações utilizadas.
  - Passo a passo de instalação e execução (deve ser possível clonar e rodar sem configurações manuais complexas).
  - Membros da equipe e divisão de tarefas.
- **GitHub Pages:** página estática sobre o projeto (bonita, informativa, ilustrada, com link para o repositório e instruções).
  - Também para inclusão no portfólio pessoal do aluno.

### 2.7 Entrega Final
- **Apresentação de slides** + **pitch** ao vivo.
- **Link do repositório** final disponibilizado ao professor.

### 2.8 Relatório de Processo
Documento simples (pode ser `RELATORIO.md` ou PDF) contendo:
- **Fontes e ferramentas extra-aula** utilizadas: vídeos, documentações, tutoriais, serviços de IA (quais e como foram usados?).
- **Dificuldades encontradas** e como foram superadas.
- **Autoavaliação** do que cada membro acredita ter compreendido bem e do que ainda precisa melhorar.
- **Sugestões e avaliação do curso** que queira compartilhar com o professor.

---

## 3. Requisitos de Bônus (Diferenciais)

- **PWA instalável**  A versão mobile pode ser instalada como app (manifesto, service worker básico). 
- **Múltiplos bancos de dados**  Uso de dois bancos de modalidades diferentes em tarefas distintas (ex: PostgreSQL para dados transacionais + MongoDB para logs). 
- **Docker** para execução containerizada e mais facilmente replicável.
- **Autenticação avançada**  Implementação de OAuth, JWT, 2FA ou controle de permissões por perfil (admin vs. usuário). 
- **Design pattern adicional** Aplicação de um segundo padrão de projeto bem justificado. 
- **Logs aprimorados** Substituição de `print()` pelo módulo `logging` do Python. 

## 5. Observações Importantes

- **Uso de IA e recursos externos é permitido e incentivado.** O que importa é que a equipe entenda o que entregou e consiga explicar.
- **Não deixe o projeto para a última semana.** O requisito de Git colaborativo exige tempo para revisões e iterações.
- **Se algo não estiver claro, pergunte antes.** É melhor alinhar expectativas do que supor errado.

---

**Boa sorte. Construam algo que vocês mesmos gostariam de usar.**