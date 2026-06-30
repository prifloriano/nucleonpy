# nucleonpy

[![PyPI version](https://img.shields.io/pypi/v/nucleonpy.svg)](https://pypi.org/project/nucleonpy/)
[![Python versions](https://img.shields.io/pypi/pyversions/nucleonpy.svg)](https://pypi.org/project/nucleonpy/)
[![CI](https://github.com/prifloriano/nucleonpy/actions/workflows/ci.yml/badge.svg)](https://github.com/prifloriano/nucleonpy/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/prifloriano/nucleonpy)](https://github.com/prifloriano/nucleonpy/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`nucleonpy` é uma biblioteca científica em Python para cálculo, consulta, simulação e visualização de decaimento radioativo.

O pacote foi criado para facilitar análises envolvendo meia-vida, atividade remanescente, cadeias lineares de decaimento, equações de Bateman e dados nucleares obtidos a partir da IAEA.

> Status: projeto em fase alpha.

## Recursos

* Cálculo de quantidade ou atividade remanescente
* Simulação de cadeias lineares de decaimento radioativo
* Implementação das equações de Bateman
* Base interna de isótopos
* Metadados sobre a fonte dos dados nucleares
* Normalização automática de nomes de isótopos
* Busca de isótopos por símbolo químico
* Filtros por estabilidade e modo de decaimento
* Interface orientada a objetos com `Isotope`
* Visualização com Matplotlib
* Exportação de resultados para CSV e JSON
* Testes automatizados com `pytest`
* Análise de qualidade com `ruff`
* CI com GitHub Actions

## Requisitos

* Python 3.11 ou superior
* Poetry

## Instalação

Clone o repositório:

```bash
git clone https://github.com/prifloriano/nucleonpy.git
cd nucleonpy
```

Instale as dependências com Poetry:

```bash
poetry install
```

Também é possível instalar em modo editável com `pip`:

```bash
pip install -e .
```

Ou

```bash
pip install nucleonpy
```

## Uso rápido

### Consultar um isótopo

```python
from nucleonpy import Isotope

tritio = Isotope("H-3")

print(tritio.name)
print(tritio.atomic_number)
print(tritio.half_life)
print(tritio.decay_mode)
print(tritio.is_stable)
print(tritio.decay_constant)
```

### Normalização de nomes de isótopos

O `nucleonpy` aceita diferentes formas de escrever o nome de um isótopo. A entrada é normalizada automaticamente para o formato usado na base interna.

Exemplos equivalentes para trítio:

```python
from nucleonpy import Isotope

tritio_1 = Isotope("H-3")
tritio_2 = Isotope("h-3")
tritio_3 = Isotope("h3")
tritio_4 = Isotope(" H-3 ")

print(tritio_1.name)
print(tritio_2.name)
print(tritio_3.name)
print(tritio_4.name)
```

Todas as chamadas acima são interpretadas como:

```text
H-3
```

Exemplos equivalentes para cobalto-60:

```python
from nucleonpy import Isotope

cobalto_1 = Isotope("Co-60")
cobalto_2 = Isotope("co-60")
cobalto_3 = Isotope("CO60")
cobalto_4 = Isotope("co60")

print(cobalto_1.name)
print(cobalto_2.name)
print(cobalto_3.name)
print(cobalto_4.name)
```

Todas as chamadas acima são normalizadas para:

```text
Co-60
```

### Calcular decaimento simples

```python
from nucleonpy import calculate_remaining_activity

atividade = calculate_remaining_activity(
    initial_amount=1000.0,
    half_life_seconds=10.0,
    time_elapsed_seconds=10.0,
)

print(atividade)
```

Após uma meia-vida, a quantidade restante será aproximadamente metade da quantidade inicial.

### Calcular decaimento usando a classe `Isotope`

```python
from nucleonpy import Isotope

tritio = Isotope("H-3")

atividade = tritio.get_remaining_activity(
    initial_amount=1000.0,
    time_elapsed=5 * 365 * 24 * 3600,
)

print(atividade)
```

### Simular uma cadeia de decaimento

```python
from nucleonpy import calculate_bateman_chain

resultados = calculate_bateman_chain(
    initial_amount=100.0,
    half_lives_seconds=[5.0, 10.0, float("inf")],
    time_elapsed_seconds=20.0,
)

print(resultados)
```

Use `float("inf")` para representar um produto final estável.

### Gerar gráfico da cadeia de decaimento

```python
from nucleonpy import plot_decay_chain

fig, ax = plot_decay_chain(
    initial_amount=100.0,
    half_lives_seconds=[5.0, 10.0, float("inf")],
    time_max_seconds=50.0,
)

fig.savefig("decay-chain.png", dpi=300)
```

Para exibir o gráfico imediatamente:

```python
from nucleonpy import plot_decay_chain

plot_decay_chain(
    initial_amount=100.0,
    half_lives_seconds=[5.0, 10.0, float("inf")],
    time_max_seconds=50.0,
    show=True,
)
```

## Busca e filtros

### Listar todos os isótopos disponíveis

```python
from nucleonpy import list_isotopes

isotopos = list_isotopes()

print(len(isotopos))
print(isotopos[:10])
```

### Buscar isótopos por símbolo químico

```python
from nucleonpy import get_isotopes_by_symbol

cobaltos = get_isotopes_by_symbol("Co")

print(cobaltos.keys())
```

### Filtrar isótopos estáveis e radioativos

```python
from nucleonpy import get_radioactive_isotopes, get_stable_isotopes

estaveis = get_stable_isotopes()
radioativos = get_radioactive_isotopes()

print(len(estaveis))
print(len(radioativos))
```

### Filtrar por modo de decaimento

```python
from nucleonpy import get_isotopes_by_decay_mode

beta_menos = get_isotopes_by_decay_mode("B-")

print(beta_menos.keys())
```

## Exportação de resultados

### Gerar série temporal

```python
from nucleonpy import generate_decay_chain_series

serie = generate_decay_chain_series(
    initial_amount=100.0,
    half_lives_seconds=[5.0, 10.0, float("inf")],
    time_max_seconds=50.0,
    num_points=100,
)

print(serie[0])
```

### Exportar para CSV

```python
from nucleonpy import export_decay_chain_to_csv

export_decay_chain_to_csv(
    path="decay-chain.csv",
    initial_amount=100.0,
    half_lives_seconds=[5.0, 10.0, float("inf")],
    time_max_seconds=50.0,
    num_points=100,
)
```

### Exportar para JSON

```python
from nucleonpy import export_decay_chain_to_json

export_decay_chain_to_json(
    path="decay-chain.json",
    initial_amount=100.0,
    half_lives_seconds=[5.0, 10.0, float("inf")],
    time_max_seconds=50.0,
    num_points=100,
)
```

## Fonte dos dados

A base interna de isótopos é gerada a partir da IAEA LiveChart of Nuclides.

Fonte usada pelo script de atualização:

```text
https://www-nds.iaea.org/relnsd/v0/data?fields=ground_states&nuclides=all
```

O script responsável pela atualização da base está em:

```text
scripts/fetch_iaea.py
```

Ele gera os arquivos:

```text
src/nucleonpy/isotopes.json
src/nucleonpy/isotopes_metadata.json
```

No arquivo `isotopes.json`, valores `null` em `half_life_seconds` representam isótopos estáveis ou registros sem meia-vida numérica disponível na fonte.

Durante o carregamento da biblioteca, esses valores são convertidos para `math.inf`.

## Atualizar a base de isótopos

Execute:

```bash
poetry run python scripts/fetch_iaea.py
```

Depois valide os arquivos JSON:

```bash
python -m json.tool src/nucleonpy/isotopes.json > /dev/null
python -m json.tool src/nucleonpy/isotopes_metadata.json > /dev/null
```

## Desenvolvimento

### Instalar dependências

```bash
poetry install
```

### Rodar testes

```bash
poetry run pytest
```

A suíte de testes cobre:

* Cálculo de decaimento simples
* Validações de entrada
* Cadeias de Bateman
* Carregamento da base de isótopos
* Normalização de nomes de isótopos
* Busca e filtros
* Classe `Isotope`
* API pública do pacote
* Visualização com Matplotlib
* Exportação para CSV e JSON

### Rodar lint com Ruff

```bash
poetry run ruff check .
```

Para corrigir automaticamente o que for possível:

```bash
poetry run ruff check . --fix
```

### Rodar formatação com Ruff

```bash
poetry run ruff format .
```

Para apenas verificar se a formatação está correta:

```bash
poetry run ruff format --check .
```

### Rodar validação completa

```bash
poetry run ruff format .
poetry run ruff check .
poetry run pytest
```

## Build do pacote

Para gerar os artefatos de distribuição:

```bash
poetry build
```

Os arquivos serão gerados na pasta:

```text
dist/
```

Para conferir se os arquivos de dados entraram no pacote:

```bash
tar -tzf dist/nucleonpy-0.1.0.tar.gz | grep isotopes
```

O resultado deve incluir:

```text
src/nucleonpy/isotopes.json
src/nucleonpy/isotopes_metadata.json
```

## Estrutura do projeto

```text
nucleonpy/
├── .github/
│   └── workflows/
│       └── ci.yml
├── scripts/
│   └── fetch_iaea.py
├── src/
│   └── nucleonpy/
│       ├── __init__.py
│       ├── calculus.py
│       ├── core.py
│       ├── data.py
│       ├── export.py
│       ├── isotopes.json
│       ├── isotopes_metadata.json
│       └── viz.py
├── tests/
├── README.md
├── pyproject.toml
└── LICENSE
```

## Comandos úteis

```bash
poetry install
poetry run pytest
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format .
poetry run ruff format --check .
poetry build
```

## Aviso

O `nucleonpy` ainda está em desenvolvimento.

Os resultados devem ser validados antes de qualquer uso acadêmico, técnico, médico, industrial, regulatório ou profissional.

## Licença

MIT
