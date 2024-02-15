
# APIRestful Pepets
Pepets: Plataforma para Anúncios de Animais Perdidos e Encontrados

Esta aplicação web tem como objetivo facilitar a conexão entre pessoas que perderam seus animais de estimação e aqueles que encontraram animais perdidos, promovendo uma comunidade unida para ajudar a reunir esses animais com seus tutores.


## Funcionalidades

- Uso de Token JWT para autenticação com Django Simple JWT
- Validação de email
- Rotas para change/reset password
- Rotas para autenticados ou não, assim como administrativas
- Inserção de imagem para criação de um post
- Documentação da API usando Swagger
- APIRestful utilizando Django Rest Framework


## Observações

- O projeto ainda esta em desenvolvimento e ainda será implementado novas funcionalidades!
- Para criação de um usuário é enviado um link de verificação de email para o email do registro, por via de desenvolvimento este email aparece no console da aplicação, contendo o link para validação, basta abrir o link, que o usuário será validado.


## Rodando localmente

### Clone o projeto

```bash
  git clone https://github.com/joaoleau/api-pepets.git
```

### Entre no diretório do projeto

```bash
  cd api-pepets
```

### Ambiente Virtual Python

```bash
  python -m venv venv
```

### Ative o ambiente virtual
- No Windows:
```bash
  venv\Scripts\activate
```

- No Unix ou MacOS:
```bash
  source venv/bin/activate
```

### Instale as dependências

```bash
  pip install -r requirements.txt
```

### Faça as migrações

```bash
  python .manage.py migrate
```

### Inicie o projeto

```bash
  python .manage.py runserver
```


## Documentação da API
 
Para acessar a documentação basta acessar a rota 'doc/'

```http
  GET /doc/
```


## Aprendizados

Este projeto me proporcionou muito conhecimento, foi e é o meu primeiro projeto desenvolvido sem nenhum acompanhamento, por tanto, foi desafiador porém ótimo para aplicação do meu aprendizado e dos conceitos vistos.


## Autores

- [@joaoleau](https://www.github.com/joaoleau)