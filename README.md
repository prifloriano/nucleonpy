# nucleonpy

O `nucleonpy` é uma biblioteca científica em Python projetada para facilitar a análise de decaimento radioativo. Ele automatiza o cálculo de cadeias de decaimento (equações de Bateman) e oferece visualização profissional para dados nucleares, baseada em informações da IAEA.

## Como instalar

Para utilizar o `nucleonpy` em seus projetos, você pode instalá-lo diretamente via terminal:

```bash
# Clone o repositório
git clone [https://github.com/prifloriano/nucleonpy.git](https://github.com/prifloriano/nucleonpy.git)
cd nucleonpy

# Instale o pacote no modo editável
pip install -e .

```
## Como usar
O nucleonpy foi desenhado para ser intuitivo. Esqueça cálculos manuais de meia-vida ou constantes de decaimento — o pacote cuida da física para você.

### 1. Orientação a Objetos (Recomendado)
A forma mais simples de interagir com o pacote é através da classe Isotope:


```bash
from nucleonpy import Isotope

# Instancie o isótopo pelo nome (ex: Co-60)
cobalto = Isotope("Co-60")

# Calcule a atividade após 5 anos (em segundos)
tempo = 5 * 365 * 24 * 3600
atividade = cobalto.get_remaining_activity(initial_amount=1000, time_elapsed=tempo)

print(f"Atividade restante: {atividade:.2f} Bq")

```

### 2. Simulação de Cadeia de Decaimento
Para problemas complexos (Pai → Filho → Estável), utilize o motor de Bateman:

```bash
from nucleonpy import calculate_bateman_chain

# Meias-vidas em segundos (Use float('inf') para isótopos estáveis)
meias_vidas = [5.0, 10.0, float('inf')]
resultados = calculate_bateman_chain(initial_amount=100.0, half_lives_seconds=meias_vidas, time_elapsed_seconds=20.0)

print(f"Abundância das gerações: {resultados}")
```
###  3. Visualização Científica
Gere gráficos prontos para publicação acadêmica com uma única chamada:

```bash
from nucleonpy import plot_decay_chain

plot_decay_chain(initial_amount=100.0, half_lives_seconds=[5.0, 10.0, float('inf')], time_max_seconds=50.0)
```

## Desenvolvimento & Testes

Para garantir a integridade dos cálculos, o pacote possui testes automatizados com pytest. Para rodar a bateria de testes e validar o ambiente:

```bash
poetry run pytest
```