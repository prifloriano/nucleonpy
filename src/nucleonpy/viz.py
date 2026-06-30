# src/nucleonpy/viz.py
import numpy as np
import matplotlib.pyplot as plt
from .calculus import calculate_bateman_chain

def plot_decay_chain(initial_amount: float, half_lives_seconds: list[float], time_max_seconds: float, num_points: int = 500):
    """
    Gera um gráfico estilo artigo científico para uma cadeia de decaimento.
    """
    
    t_array = np.linspace(0, time_max_seconds, num_points)
    
    num_isotopes = len(half_lives_seconds)
    results_matrix = np.zeros((num_isotopes, num_points))
    
    for i, t in enumerate(t_array):
        results = calculate_bateman_chain(initial_amount, half_lives_seconds, t)
        for j in range(num_isotopes):
            results_matrix[j, i] = results[j]
            
    print("Gerando o gráfico de alta resolução...")
    
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = [f"Geração {i+1} (Instável)" for i in range(num_isotopes)]
    labels[-1] = "Produto Final (Estável)" 
    
    colors = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#F0E442']
    
    for j in range(num_isotopes):
        color = colors[j % len(colors)]
        ax.plot(t_array, results_matrix[j, :], linewidth=2.5, label=labels[j], color=color)
        
    ax.set_xlabel("Tempo (segundos)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Abundância / Atividade", fontsize=12, fontweight='bold')
    ax.set_title("Evolução da Cadeia de Decaimento Radioativo", fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=11)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.show()