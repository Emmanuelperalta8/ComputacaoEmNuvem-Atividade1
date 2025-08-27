# DepressaoEmNuvem-Atividade1

Projeto Django containerizado com Docker, PostgreSQL e Nginx, para upload de arquivos e armazenamento persistente.

## Estrutura do Projeto

```
DepressaoEmNuvem-Atividade1/
├── django
│   └── src
│       ├── core
│       ├── media (arquivos enviados)
│       ├── uploads
│       │   └── templates
│       │       └── uploads
│       │           ├── upload.html
│       │           └── success.html
│       ├── manage.py
│       └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── nginx
    ├── nginx.conf
    └── nginx.conf_OLD
```

## Como rodar o projeto

1. **Clone o repositório**

   ```sh
   git clone https://github.com/seu-usuario/seu-repo.git
   cd DepressaoEmNuvem-Atividade1
   ```

2. **Monte os containers**

   ```sh
   docker-compose up --build
   ```

   Isso irá subir:
   - Django (porta 8000)
   - PostgreSQL
   - Nginx (porta 80)

3. **Acesse o sistema**

   - Página inicial:
     ```
     http://localhost/
     ```
   - Para realizar upload de arquivos:
     ```
     http://localhost/upload/
     ```
     Preencha o formulário e envie seu arquivo.

   - Após o envio, a mensagem de sucesso exibirá o nome do arquivo.

## Onde o arquivo fica salvo?

- Todo arquivo enviado via upload é salvo na pasta:
  ```
  django/src/media
  ```
  (Se estiver usando o volume padrão do docker-compose deste projeto.)

- Você pode acessar localmente os arquivos enviados diretamente nesta pasta.

## Pastas importantes

- **media/**: arquivos enviados via upload são salvos aqui.
- **uploads/templates/uploads/**: templates HTML para upload e sucesso.

## Observações

- Se quiser que os arquivos enviados apareçam diretamente na pasta `media` do projeto, certifique-se que o volume do Docker está configurado para mapear `./django/src/media:/app/media`.

---

**Contato:**  
Dúvidas ou sugestões? Abra uma issue ou entre em contato!