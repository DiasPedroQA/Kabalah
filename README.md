# Flask Formulário e API

Este é um projeto simples com Flask que contém um formulário para processar um valor informado pelo usuário e também uma API para processamento via requisição POST.

## Como rodar

1. Instale as dependências:

   pip install -r requirements.txt

2. Execute a aplicação:

   python main.py

3. Acesse o site:

   <http://127.0.0.1:5500/>

4. Teste a API usando o formulário na interface ou ferramentas como Postman.

## Testes

Para rodar os testes:

python -m unittest tests/test_app.py

### Melhorias Futuras

- Adicionar validação do lado do backend para os valores do formulário.
- Utilizar um banco de dados para armazenar os dados se necessário.
- Implementar autenticação para proteger a API.

Agora, você tem uma estrutura básica funcionando com Flask, um formulário, e uma API que processa dados e retorna resultados.
