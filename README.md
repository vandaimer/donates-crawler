### Para rodar o crawler

- Após clonar do projeto
- Rodar
```bash
 docker run -it --rm -v ${PWD}:/app python bash
```
- Dentro do container ir para o diretoróio */app*
- Instalar as dependências dentro do container
```bash
pip install -r requirements.txt
```
- Entrar diretoróio */app/src*
```bash
scrapy crawl vakinha
```

### Para editar o notebook

- Após clonar do projeto
- Rodar
```bash
 docker run -it --rm -p 8888:8888 -v ${PWD}:/home/jovyan/work jupyter/datascience-notebook
```
- Acessar via browser `http://127.0.0.1:8888/tree`
- Irá pedir um token, você o encontra no terminal que executou o docker
- Acessar o notebook `Vakinha.ipynb` e o editar


### Contribuir

- Fork
- Melhorias
- Submeter PR
