import ast
import matplotlib.pyplot as plt
import numpy as np

files = {
    ('Plurality', 'Bullet Voting'): './data_files/BTVA/BTVA_plurality_bullet',
    ('Plurality', 'Burying'): './data_files/BTVA/BTVA_plurality_bury',
    ('Plurality', 'Compromise'): './data_files/BTVA/BTVA_plurality_compromise',
    ('Anti-Plurality', 'Bullet Voting'): './data_files/BTVA/BTVA_anti_plurality_bullet',
    ('Anti-Plurality', 'Burying'): './data_files/BTVA/BTVA_anti_plurality_bury',
    ('Anti-Plurality', 'Compromise'): './data_files/BTVA/BTVA_anti_plurality_compromise',
    ('Borda', 'Bullet Voting'): './data_files/BTVA/BTVA_borda_bullet',
    ('Borda', 'Burying'): './data_files/BTVA/BTVA_borda_bury',
    ('Borda', 'Compromise'): './data_files/BTVA/BTVA_borda_compromise',
    ('Voting for Two', 'Bullet Voting'): './data_files/BTVA/BTVA_voting_for_two_bullet',
    ('Voting for Two', 'Burying'): './data_files/BTVA/BTVA_voting_for_two_bury',
    ('Voting for Two', 'Compromise'): './data_files/BTVA/BTVA_voting_for_two_compromise',
}

def load_data(path):
    data = {}
    with open(path) as f:
        lines = f.readlines()[1:]
    for line in lines:
        idx = line.index('{')
        d = ast.literal_eval(line[idx:line.rindex('}')+1])
        c, v = d['num_candidates'], d['num_voters']
        data[(c, v)] = d['avg_risk']
    return data

all_data = {k: load_data(v) for k, v in files.items()}

schemes = ['Plurality', 'Anti-Plurality', 'Borda', 'Voting for Two']
strategies = ['Bullet Voting', 'Burying', 'Compromise']
colors = {'Bullet Voting': '#2196F3', 'Burying': '#FF9800', 'Compromise': '#4CAF50'}


fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(schemes))
width = 0.25
#Risk values are averaged across all (c, v) pairs for each scheme and strategy
for i, strategy in enumerate(strategies):
    means = []
    for scheme in schemes:
        d = all_data[(scheme, strategy)]
        means.append(np.mean(list(d.values())))
    ax.bar(x + i * width, means, width, label=strategy, color=colors[strategy])

ax.set_xticks(x + width)
ax.set_xticklabels(schemes)
ax.set_ylabel('Overall Avg. Risk')
ax.set_title('BTVA: Overall Average Risk per Scheme and Strategy', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('./graphs_figures/fig1_overall_bar.png', dpi=150, bbox_inches='tight')
plt.show()

#Risk vs Candidates for each scheme and strategy

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes = axes.flatten()

for ax, scheme in zip(axes, schemes):
    candidates_range = range(2, 11)
    for strategy in strategies:
        d = all_data[(scheme, strategy)]
        y = []
        for c in candidates_range:
            vals = [d[(c, v)] for v in range(2, 11) if (c, v) in d]
            y.append(np.mean(vals) if vals else 0)
        ax.plot(list(candidates_range), y, marker='o', label=strategy,
                color=colors[strategy], linewidth=2)
    ax.set_title(scheme, fontsize=13, fontweight='bold')
    ax.set_xlabel('Number of Candidates')
    ax.set_ylabel('Avg. Risk')
    ax.legend(fontsize=8)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)

plt.suptitle('BTVA: Average Tactical Voting Risk by Candidates & Strategy',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('./graphs_figures/fig2_risk_vs_candidates.png', dpi=150, bbox_inches='tight')
plt.show()


#HeatMaps
files = {
    'Bullet Voting': './data_files/BTVA/BTVA_anti_plurality_bullet',
    'Burying':       './data_files/BTVA/BTVA_anti_plurality_bury',
    'Compromise':    './data_files/BTVA/BTVA_anti_plurality_compromise',
}

def load_data(path):
    data = {}
    with open(path) as f:
        lines = f.readlines()[1:]
    for line in lines:
        idx = line.index('{')
        d = ast.literal_eval(line[idx:line.rindex('}')+1])
        c, v = d['num_candidates'], d['num_voters']
        data[(c, v)] = d['avg_risk']
    return data

all_data = {strategy: load_data(path) for strategy, path in files.items()}

strategies = ['Bullet Voting', 'Burying', 'Compromise']
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, strategy in zip(axes, strategies):
    d = all_data[strategy]

    # Build 9x9 matrix: rows = candidates 2-10, cols = voters 2-10
    matrix = np.zeros((9, 9))
    for ci, c in enumerate(range(2, 11)):
        for vi, v in enumerate(range(2, 11)):
            matrix[ci, vi] = d.get((c, v), 0)

    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1.0)

    ax.set_xticks(range(9))
    ax.set_xticklabels(range(2, 11))
    ax.set_yticks(range(9))
    ax.set_yticklabels(range(2, 11))
    ax.set_xlabel('Number of Voters')
    ax.set_ylabel('Number of Candidates')
    ax.set_title(strategy, fontweight='bold')

    plt.colorbar(im, ax=ax, label='Avg Risk')

plt.suptitle('Anti-Plurality: Risk Heatmap (candidates × voters)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('./graphs_figures/fig4_heatmap_antiplurality.png', dpi=150, bbox_inches='tight')
plt.show()

#Risk vs Voters for each scheme and strategy

files = {
    ('Plurality', 'Bullet Voting'): './data_files/BTVA/BTVA_plurality_bullet',
    ('Plurality', 'Burying'): './data_files/BTVA/BTVA_plurality_bury',
    ('Plurality', 'Compromise'): './data_files/BTVA/BTVA_plurality_compromise',
    ('Anti-Plurality', 'Bullet Voting'): './data_files/BTVA/BTVA_anti_plurality_bullet',
    ('Anti-Plurality', 'Burying'): './data_files/BTVA/BTVA_anti_plurality_bury',
    ('Anti-Plurality', 'Compromise'): './data_files/BTVA/BTVA_anti_plurality_compromise',
    ('Borda', 'Bullet Voting'): './data_files/BTVA/BTVA_borda_bullet',
    ('Borda', 'Burying'): './data_files/BTVA/BTVA_borda_bury',
    ('Borda', 'Compromise'): './data_files/BTVA/BTVA_borda_compromise',
    ('Voting for Two', 'Bullet Voting'): './data_files/BTVA/BTVA_voting_for_two_bullet',
    ('Voting for Two', 'Burying'): './data_files/BTVA/BTVA_voting_for_two_bury',
    ('Voting for Two', 'Compromise'): './data_files/BTVA/BTVA_voting_for_two_compromise',
}

def load_data(path):
    data = {}
    with open(path) as f:
        lines = f.readlines()[1:]
    for line in lines:
        idx = line.index('{')
        d = ast.literal_eval(line[idx:line.rindex('}')+1])
        c, v = d['num_candidates'], d['num_voters']
        data[(c, v)] = d['avg_risk']
    return data

all_data = {k: load_data(v) for k, v in files.items()}

schemes = ['Plurality', 'Anti-Plurality', 'Borda', 'Voting for Two']
strategies = ['Bullet Voting', 'Burying', 'Compromise']
colors = {'Bullet Voting': '#2196F3', 'Burying': '#FF9800', 'Compromise': '#4CAF50'}

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes = axes.flatten()

for ax, scheme in zip(axes, schemes):
    voters_range = range(2, 11)
    for strategy in strategies:
        d = all_data[(scheme, strategy)]
        y = []
        for v in voters_range:
            vals = [d[(c, v)] for c in range(2, 11) if (c, v) in d]
            y.append(np.mean(vals) if vals else 0)
        ax.plot(list(voters_range), y, marker='s', label=strategy,
                color=colors[strategy], linewidth=2)
    ax.set_title(scheme, fontsize=13, fontweight='bold')
    ax.set_xlabel('Number of Voters')
    ax.set_ylabel('Avg. Risk')
    ax.legend(fontsize=8)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)

plt.suptitle('BTVA: Average Tactical Voting Risk by Voters & Strategy',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('./graphs_figures/fig3_risk_vs_voters.png', dpi=150, bbox_inches='tight')
plt.show()
