# Utilitarios EDAT
Classes utilitarias utilizadas pelo EDAT.

## Passos para deploy em pyorg
Primeiro, é necessário alterar a versão do projeto no arquivo [setup.py](./setup.py), após, seguir os comandos abaixo para gerar o pacote.

Ativar o ambiente virtual
```sh
source venv/bin/activate
```

Instalar as dependências
```sh 
pip install wheel
```

```sh 
pip install twine
```

Gerar os pacotes necessários
```sh 
python setup.py sdist bdist_wheel
```

Verificar os pacotes
```sh
twine check dist/*
```

Realizar deploy dos pacotes
```sh
twine upload dist/*
```


### Credenciais
- Usuario: `edat`
- Senha: `#cgu@2023@`


# Possíveis erros

#### Erro de reuso de nome 
- Verificar se a versão já foi utilizada. 
- Apagar a pasta dist e gerar novamente os pacotes
