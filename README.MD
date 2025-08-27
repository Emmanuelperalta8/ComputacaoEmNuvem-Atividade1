# ComputacaoEmNuvem-Atividade1

Alunos: Emmanuel Peralta e Lucas Casagrande


Este projeto demonstra como criar uma aplicação Django conteinerizada, com upload de arquivos, Gunicorn, Nginx como proxy reverso e PostgreSQL como banco de dados. Os arquivos enviados são persistidos em um volume Docker para garantir durabilidade.

---

## Visão geral dos containers

- **Django + Gunicorn**: Serve a aplicação web.
- **Nginx**: Proxy reverso para Django e servidor dos arquivos enviados.
- **PostgreSQL**: Banco de dados relacional.

---

## Estrutura do Projeto

```
ComputacaoEmNuvem-Atividade1/
├── django/
│   └── src/
│       ├── core/                  # Configurações Django (settings.py, etc)
│       ├── uploads/               # App de upload
│       │   └── templates/
│       │       └── uploads/
│       │           ├── upload.html
│       │           └── success.html
│       ├── media/                 # Pasta dos arquivos enviados (persistida via volume)
│       ├── manage.py
│       └── requirements.txt
├── Dockerfile                     # Build da imagem Django + Gunicorn
├── docker-compose.yml             # Orquestração dos containers
├── nginx/
│   └── nginx.conf                 # Configuração do Nginx
```

---

## Explicação dos principais arquivos

### Dockerfile

Cria a imagem do serviço Django.  
Principais etapas:
- Usa imagem base Python.
- Instala dependências de sistema.
- Copia o projeto para o container.
- Instala as dependências Python (do `requirements.txt`).
- Expõe a porta 8000.
- Inicia o Gunicorn, rodando o Django.

**Exemplo de Dockerfile:**
```dockerfile
FROM python:3.11

WORKDIR /app

COPY django/src/ /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

### docker-compose.yml

Orquestra todos os containers necessários:
- `db`: PostgreSQL, com volume para persistência de dados.
- `web`: Django, exposto na porta 8000, com volume para persistência dos uploads.
- `nginx`: Proxy reverso, exposto na porta 80, também acessando os uploads via volume.

**Exemplo resumido:**
```yaml
services:
  db:
    image: postgres:15
    # configs...

  web:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./django/src:/app
      - ./django/src/media:/app/media
    ports:
      - "8000:8000"
    environment:
      # variáveis do Django e banco
    depends_on:
      - db

  nginx:
    image: nginx:1.25
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./django/src/media:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
```

---

### requirements.txt

Lista todas as dependências Python do projeto, por exemplo:
```
Django==4.2.4
gunicorn==21.2.0
psycopg2-binary==2.9.6
```
Essas dependências são instaladas no build da imagem Docker.

---

## Explicação dos arquivos do código

- **core/**: Configurações principais do Django.
  - `settings.py`: Configura variáveis do projeto, banco, media, apps, etc.
  - `urls.py`: Roteamento das URLs da aplicação.
  - `wsgi.py`: Ponto de entrada para servidores WSGI (como o Gunicorn).

- **manage.py**: Utilitário para comandos Django (migração, admin, shell, etc).

- **uploads/**: App Django responsável pelo upload de arquivos.
  - `views.py`: Lógica para renderizar o formulário e salvar o upload.
  - `forms.py`: Formulário de upload.
  - `models.py`: Modelos relacionados ao upload (se houver).
  - `templates/uploads/upload.html`: Formulário de upload.
  - `templates/uploads/success.html`: Página de sucesso após upload.

- **media/**: Pasta onde os arquivos enviados via upload são salvos.  
  **IMPORTANTE:** Esta pasta é persistida por volume Docker e compartilhada entre Django e Nginx, garantindo que os arquivos não se percam se algum container for removido.

- **nginx/nginx.conf**: Configuração do Nginx para proxy reverso e servir arquivos estáticos/media.

---

## Como rodar o projeto localmente

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/Emmanuelperalta8/ComputacaoEmNuvem-Atividade1.git
   cd ComputacaoEmNuvem-Atividade1
   ```

2. **Monte os containers:**
   ```sh
   docker-compose up --build
   ```

3. **Acesse a aplicação:**
   - Página inicial: [http://localhost/](http://localhost/)
   - Upload de arquivos: [http://localhost/upload/](http://localhost/upload/)

---

## Onde os arquivos ficam salvos?

Os arquivos enviados via upload são persistidos na pasta:
```
django/src/media/
```
no seu host local, pois o volume do Docker está configurado para essa pasta.  
Seus arquivos nunca se perdem, mesmo se os containers forem apagados ou reiniciados.

---

## Dicas de desenvolvimento

- Modifique o `requirements.txt` para adicionar bibliotecas Python e reconstrua o container web.
- Migrações do banco:
  ```sh
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
  ```
- Para acessar o shell do Django:
  ```sh
  docker-compose exec web python manage.py shell
  ```

---

## Segurança e produção

- Use variáveis de ambiente (ou arquivos `.env`) para senhas e dados sensíveis.
- Proteja a rota de upload conforme necessário.
- Nginx serve como camada extra de segurança e desempenho.

---

## Dúvidas?

Abra uma issue ou entre em contato!
