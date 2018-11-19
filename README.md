# cenipa
Projeto para extrair texto dos laudos do CENIPA

## Objetivo:

  Esse projeto tem como objetivo extrair dados não estruturados dos fatores contribuintes de acidentes aeronáuticos registrados pelo CENIPA (centro de investigação e prevenção de acidentes aeronáuticos).
  Para isso, foi utilizado a leitura dos fatores contribuíntes no banco de dados PostgreSQL, e extraído as classes gramaticais das frases para aplicação das regras definidas.

## Dependencias:

* Python >= 3.5
* spacy >= 2.0.12
* psycopg2 >= 2.7.5
* PostgreSQL >= 10

## Executar:

Para executar o projeto terá que restaurar a ultima base que está dentro da pasta bkp, dentro do PostgreSQL e rodar o script main.py.<br/>
Caso houver algum problema no restore da base, poderá baixar os arquivos do site http://dados.gov.br/dataset/ocorrencias-aeronauticas-da-aviacao-civil-brasileira e importar os dados para dentro do banco manualmente.

### Restaurar base de dados (Encoding utilizado pt_BR.UTF8):<br/>
`postgres@seupc:~$ psql`<br/>
`postgres=# create database cenipa;`<br/>
`CREATE DATABASE`<br/>
`postgres=# \l` <br/>
`                               Lista dos bancos de dados`<br/>
`   Nome    |   Dono   | Codificação |   Collate   |    Ctype    | Privilégios de acesso `<br/>
`-----------+----------+-------------+-------------+-------------+-----------------------`<br/>
`cenipa    | postgres | UTF8        | pt_BR.UTF-8 | pt_BR.UTF-8 | `<br/>
`postgres=# \q`<br/>
`postgres@seupc:~$ pg_restore -d cenipa bkp/20181022214717_cenipa.gz >> restore.log 2>&1`<br/>

### Executar script
`python3 main.py`
