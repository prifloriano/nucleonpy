# src/nucleonpy/calculus.py

import math


def _validate_initial_amount(initial_amount: float) -> None:
    if math.isnan(initial_amount) or initial_amount < 0:
        raise ValueError("A quantidade inicial deve ser maior ou igual a zero.")


def _validate_elapsed_time(time_elapsed_seconds: float) -> None:
    if math.isnan(time_elapsed_seconds) or time_elapsed_seconds < 0:
        raise ValueError("O tempo decorrido deve ser maior ou igual a zero.")


def _validate_half_life(half_life_seconds: float) -> None:
    if math.isnan(half_life_seconds) or half_life_seconds <= 0:
        raise ValueError("A meia-vida deve ser maior que zero.")


def calculate_remaining_activity(
    initial_amount: float,
    half_life_seconds: float,
    time_elapsed_seconds: float,
) -> float:
    """
    Calcula a quantidade ou atividade restante de um isótopo radioativo.

    Args:
        initial_amount: Quantidade inicial, atividade inicial ou número inicial de átomos.
        half_life_seconds: Meia-vida do isótopo em segundos.
            Use math.inf ou float("inf") para isótopos estáveis.
        time_elapsed_seconds: Tempo decorrido em segundos.

    Returns:
        Quantidade ou atividade restante após o tempo informado.

    Raises:
        ValueError: Se a quantidade inicial, meia-vida ou tempo forem inválidos.
    """
    _validate_initial_amount(initial_amount)
    _validate_half_life(half_life_seconds)
    _validate_elapsed_time(time_elapsed_seconds)

    decay_constant = math.log(2) / half_life_seconds
    return initial_amount * math.exp(-decay_constant * time_elapsed_seconds)


def _validate_decay_chain(
    initial_amount: float,
    half_lives_seconds: list[float],
    time_elapsed_seconds: float,
) -> None:
    _validate_initial_amount(initial_amount)
    _validate_elapsed_time(time_elapsed_seconds)

    if not half_lives_seconds:
        raise ValueError("Informe pelo menos uma meia-vida.")

    for half_life in half_lives_seconds:
        _validate_half_life(half_life)

    for index, half_life in enumerate(half_lives_seconds[:-1]):
        if math.isinf(half_life):
            raise ValueError(
                "Apenas o último isótopo da cadeia pode ser estável."
            )

    finite_half_lives = [
        half_life for half_life in half_lives_seconds if not math.isinf(half_life)
    ]

    for i, half_life in enumerate(finite_half_lives):
        for other_half_life in finite_half_lives[i + 1:]:
            if math.isclose(half_life, other_half_life, rel_tol=1e-12):
                raise ValueError(
                    "Cadeias com meias-vidas iguais ou muito próximas ainda "
                    "não são suportadas pela implementação atual."
                )


def calculate_bateman_chain(
    initial_amount: float,
    half_lives_seconds: list[float],
    time_elapsed_seconds: float,
) -> list[float]:
    """
    Resolve as equações de Bateman para uma cadeia linear de decaimento.

    A cadeia segue o formato A -> B -> C -> ... .

    Args:
        initial_amount: Quantidade inicial do isótopo pai.
        half_lives_seconds: Lista de meias-vidas em segundos para cada isótopo.
            Use math.inf ou float("inf") para o produto final estável.
        time_elapsed_seconds: Tempo decorrido em segundos.

    Returns:
        Lista com a quantidade de cada isótopo no tempo informado.

    Raises:
        ValueError: Se os parâmetros forem inválidos ou se a cadeia ainda não
            for suportada pela implementação atual.
    """
    _validate_decay_chain(
        initial_amount=initial_amount,
        half_lives_seconds=half_lives_seconds,
        time_elapsed_seconds=time_elapsed_seconds,
    )

    lambdas = [
        0.0 if math.isinf(half_life) else math.log(2) / half_life
        for half_life in half_lives_seconds
    ]

    n_elements = len(lambdas)
    results = [0.0] * n_elements

    for n in range(n_elements):
        if n == 0:
            results[n] = initial_amount * math.exp(
                -lambdas[0] * time_elapsed_seconds
            )
            continue

        amount_n = 0.0

        for i in range(n + 1):
            denominator = 1.0

            for j in range(n + 1):
                if i != j:
                    denominator *= lambdas[j] - lambdas[i]

            amount_n += math.exp(-lambdas[i] * time_elapsed_seconds) / denominator

        prod_lambdas = 1.0

        for i in range(n):
            prod_lambdas *= lambdas[i]

        results[n] = initial_amount * prod_lambdas * amount_n

    return results