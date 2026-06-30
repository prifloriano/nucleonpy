# nucleonpy

`nucleonpy` é uma biblioteca científica em Python para cálculo e visualização de decaimento radioativo.

O pacote foi criado para facilitar análises envolvendo meia-vida, atividade remanescente e cadeias lineares de decaimento usando as equações de Bateman. A proposta é oferecer uma API simples para estudos, prototipação científica e aplicações educacionais em física nuclear.

## Recursos

* Cálculo de atividade ou quantidade remanescente após determinado tempo
* Simulação de cadeias lineares de decaimento radioativo
* Implementação das equações de Bateman
* Base interna de isótopos
* Interface orientada a objetos com a classe `Isotope`
* Visualização de cadeias de decaimento com Matplotlib

## Instalação

Clone o repositório:

```bash
git clone https://github.com/prifloriano/nucleonpy.git
cd nucleonpy
```

Instale o pacote em modo editável:

```bash
poetry install
```

Ou, caso esteja usando `pip`:

```bash
pip install -e .
```

## Uso rápido

### Decaimento simples com orientação a objetos

```python
from nucleonpy import Isotope

cobalto = Isotope("Co-60")

tempo = 5 * 365 * 24 * 3600
atividade = cobalto.get_remaining_activity(
    initial_amount=1000,
    time_elapsed=tempo,
)

print(f"Atividade restante: {atividade:.2f} Bq")
```

### Decaimento simples com função direta

```python
from nucleonpy import calculate_remaining_activity

atividade = calculate_remaining_activity(
    initial_amount=1000,
    half_life_seconds=5.27 * 365 * 24 * 3600,
    time_elapsed_seconds=5 * 365 * 24 * 3600,
)

print(atividade)
```

### Cadeia de decaimento

Para simular uma cadeia linear do tipo pai, filho e produto final:

```python
from nucleonpy import calculate_bateman_chain

half_lives = [5.0, 10.0, float("inf")]

resultados = calculate_bateman_chain(
    initial_amount=100.0,
    half_lives_seconds=half_lives,
    time_elapsed_seconds=20.0,
)

print(resultados)
```

Use `float("inf")` para representar um produto final estável.

### Visualização

```python
from nucleonpy import plot_decay_chain

plot_decay_chain(
    initial_amount=100.0,
    half_lives_seconds=[5.0, 10.0, float("inf")],
    time_max_seconds=50.0,
)
```

## Desenvolvimento

Instale as dependências do projeto:

```bash
poetry install
```

Execute os testes:

```bash
poetry run pytest
```

Execute o linter:

```bash
poetry run ruff check .
```

## Status do projeto

Este projeto está em fase inicial de desenvolvimento.

O objetivo da versão `0.1.0` é validar a estrutura principal da biblioteca, incluindo:

* API básica para isótopos
* Cálculo de decaimento simples
* Cálculo de cadeias lineares
* Visualização inicial
* Base interna de dados nucleares

## Roadmap

* [x] Estrutura inicial do pacote
* [x] Cálculo de decaimento simples
* [x] Cadeias de Bateman
* [x] Base interna de isótopos
* [x] Visualização com Matplotlib
* [ ] Testes automatizados
* [ ] CI com GitHub Actions
* [ ] Normalização de nomes de isótopos
* [ ] Melhor tratamento para isótopos estáveis
* [ ] Exportação de resultados
* [ ] Documentação expandida
* [ ] Publicação no PyPI

## Aviso

O `nucleonpy` ainda está em fase alpha. Os resultados devem ser validados antes de qualquer uso acadêmico, técnico, médico, industrial ou regulatório.

## Licença

Licença a definir.
