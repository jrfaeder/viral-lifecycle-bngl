#!/usr/bin/env python3
"""
Validation script for viral lifecycle model

This script compares the BNGL simulation results with MATLAB simulation results
to validate that the BioNetGen implementation matches the original ODE model.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def load_matlab_results(matlab_csv):
    """Load MATLAB simulation results from CSV file"""
    if not os.path.exists(matlab_csv):
        print(f"ERROR: MATLAB results file not found: {matlab_csv}")
        print("Please run run_viral_lifecycle_matlab.m first to generate the MATLAB results.")
        sys.exit(1)

    df = pd.read_csv(matlab_csv)
    print(f"Loaded MATLAB results: {matlab_csv}")
    print(f"  Time range: {df['time_hours'].min():.1f} - {df['time_hours'].max():.1f} hours")
    return df


def load_bngl_results(bngl_csv):
    """Load BNGL simulation results from CSV file"""
    if not os.path.exists(bngl_csv):
        print(f"ERROR: BNGL results file not found: {bngl_csv}")
        print("Please run simulate_viral_lifecycle.py first to generate the BNGL results.")
        sys.exit(1)

    df = pd.read_csv(bngl_csv)
    print(f"Loaded BNGL results: {bngl_csv}")
    print(f"  Time range: {df['time_hours'].min():.1f} - {df['time_hours'].max():.1f} hours")
    return df


def interpolate_to_common_timepoints(df1, df2, time_col='time_hours'):
    """Interpolate both dataframes to a common set of time points"""
    # Use the finer grid of the two
    if len(df1) >= len(df2):
        common_time = df1[time_col].values
        df1_interp = df1.copy()
        df2_interp = pd.DataFrame({time_col: common_time})
        for col in df2.columns:
            if col != time_col:
                df2_interp[col] = np.interp(common_time, df2[time_col].values, df2[col].values)
    else:
        common_time = df2[time_col].values
        df2_interp = df2.copy()
        df1_interp = pd.DataFrame({time_col: common_time})
        for col in df1.columns:
            if col != time_col:
                df1_interp[col] = np.interp(common_time, df1[time_col].values, df1[col].values)

    return df1_interp, df2_interp


def calculate_error_metrics(matlab_data, bngl_data, species_name):
    """Calculate error metrics between MATLAB and BNGL results"""
    # Filter out zero/near-zero values to avoid division by zero
    nonzero_mask = (np.abs(matlab_data) > 1e-10) | (np.abs(bngl_data) > 1e-10)

    if not np.any(nonzero_mask):
        return {'max_abs_error': 0, 'mean_abs_error': 0, 'max_rel_error': 0, 'mean_rel_error': 0}

    matlab_nz = matlab_data[nonzero_mask]
    bngl_nz = bngl_data[nonzero_mask]

    # Absolute error
    abs_error = np.abs(matlab_nz - bngl_nz)
    max_abs_error = np.max(abs_error)
    mean_abs_error = np.mean(abs_error)

    # Relative error (avoid division by very small numbers)
    rel_error = abs_error / (np.abs(matlab_nz) + 1e-10)
    max_rel_error = np.max(rel_error)
    mean_rel_error = np.mean(rel_error)

    return {
        'max_abs_error': max_abs_error,
        'mean_abs_error': mean_abs_error,
        'max_rel_error': max_rel_error,
        'mean_rel_error': mean_rel_error
    }


def compare_results(matlab_df, bngl_df, species_mapping):
    """
    Compare MATLAB and BNGL results for all species

    Parameters:
    -----------
    matlab_df : DataFrame
        MATLAB results
    bngl_df : DataFrame
        BNGL results
    species_mapping : dict
        Mapping from MATLAB column names to BNGL column names
    """
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)

    # Interpolate to common time points
    matlab_interp, bngl_interp = interpolate_to_common_timepoints(matlab_df, bngl_df)

    # Compare each species
    results = {}
    for matlab_col, bngl_col in species_mapping.items():
        if matlab_col not in matlab_interp.columns:
            print(f"Warning: {matlab_col} not found in MATLAB results")
            continue
        if bngl_col not in bngl_interp.columns:
            print(f"Warning: {bngl_col} not found in BNGL results")
            continue

        matlab_data = matlab_interp[matlab_col].values
        bngl_data = bngl_interp[bngl_col].values

        metrics = calculate_error_metrics(matlab_data, bngl_data, matlab_col)
        results[matlab_col] = metrics

        print(f"\n{matlab_col}:")
        print(f"  Max absolute error: {metrics['max_abs_error']:.4e}")
        print(f"  Mean absolute error: {metrics['mean_abs_error']:.4e}")
        print(f"  Max relative error: {metrics['max_rel_error']:.4f}")
        print(f"  Mean relative error: {metrics['mean_rel_error']:.4f}")

    return results, matlab_interp, bngl_interp


def plot_comparison(matlab_df, bngl_df, species_mapping, save_prefix='validation'):
    """
    Create comparison plots

    Parameters:
    -----------
    matlab_df : DataFrame
        MATLAB results (interpolated)
    bngl_df : DataFrame
        BNGL results (interpolated)
    species_mapping : dict
        Mapping from MATLAB column names to BNGL column names
    save_prefix : str
        Prefix for saved figure files
    """
    n_species = len(species_mapping)
    n_cols = 3
    n_rows = int(np.ceil(n_species / n_cols))

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
    axes = axes.flatten()

    for idx, (matlab_col, bngl_col) in enumerate(species_mapping.items()):
        ax = axes[idx]

        if matlab_col in matlab_df.columns and bngl_col in bngl_df.columns:
            # Plot MATLAB results
            ax.plot(matlab_df['time_hours'], matlab_df[matlab_col],
                   'b-', linewidth=2, label='MATLAB', alpha=0.7)

            # Plot BNGL results
            ax.plot(bngl_df['time_hours'], bngl_df[bngl_col],
                   'r--', linewidth=2, label='BNGL', alpha=0.7)

            ax.set_xlabel('Time (hours)', fontsize=10)
            ax.set_ylabel(f'{matlab_col}', fontsize=10)
            ax.set_yscale('log')
            ax.set_ylim(bottom=1e-2)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=9)
        else:
            ax.text(0.5, 0.5, f'{matlab_col}\nNot Found',
                   ha='center', va='center', transform=ax.transAxes)

    # Hide extra subplots
    for idx in range(n_species, len(axes)):
        axes[idx].axis('off')

    plt.suptitle('Viral Lifecycle Model: MATLAB vs BNGL Comparison',
                fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Save figure
    fig_file = f'{save_prefix}_comparison.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"\nComparison plot saved as: {fig_file}")

    plt.show()


def plot_error_heatmap(results, save_prefix='validation'):
    """
    Create a heatmap of error metrics

    Parameters:
    -----------
    results : dict
        Dictionary of error metrics for each species
    save_prefix : str
        Prefix for saved figure files
    """
    species = list(results.keys())
    metrics = ['max_abs_error', 'mean_abs_error', 'max_rel_error', 'mean_rel_error']
    metric_labels = ['Max Abs Error', 'Mean Abs Error', 'Max Rel Error', 'Mean Rel Error']

    # Create matrix of values
    data = np.zeros((len(species), len(metrics)))
    for i, sp in enumerate(species):
        for j, metric in enumerate(metrics):
            data[i, j] = results[sp][metric]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, len(species)*0.5 + 2))

    # Log scale for absolute errors, linear for relative
    data_display = data.copy()
    data_display[:, :2] = np.log10(data[:, :2] + 1e-20)  # Log scale for abs errors

    im = ax.imshow(data_display, aspect='auto', cmap='RdYlGn_r')

    # Set ticks and labels
    ax.set_xticks(np.arange(len(metrics)))
    ax.set_yticks(np.arange(len(species)))
    ax.set_xticklabels(metric_labels)
    ax.set_yticklabels(species)

    # Rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Error (log10 for abs, linear for rel)', rotation=270, labelpad=20)

    # Add text annotations
    for i in range(len(species)):
        for j in range(len(metrics)):
            if j < 2:  # Absolute errors
                text = f'{data[i, j]:.1e}'
            else:  # Relative errors
                text = f'{data[i, j]:.3f}'
            ax.text(j, i, text, ha="center", va="center", color="black", fontsize=8)

    ax.set_title('Error Metrics: MATLAB vs BNGL', fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Save figure
    fig_file = f'{save_prefix}_error_heatmap.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"Error heatmap saved as: {fig_file}")

    plt.show()


def main():
    """Main validation function"""

    print("="*80)
    print("Viral Lifecycle Model Validation")
    print("="*80)

    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    matlab_csv = os.path.join(script_dir, 'viral_lifecycle_matlab_results.csv')
    bngl_csv = os.path.join(script_dir, 'viral_lifecycle_results.csv')

    # Load results
    try:
        matlab_df = load_matlab_results(matlab_csv)
        bngl_df = load_bngl_results(bngl_csv)
    except Exception as e:
        print(f"\nERROR loading results: {e}")
        sys.exit(1)

    # Define species mapping (MATLAB column -> BNGL column)
    species_mapping = {
        'V_E': '[V_E]',
        'V_0': '[V_0]',
        'V_I': '[V_I]',
        'R_cyt': '[R_cyt]',
        'R_CM': '[R_CM]',
        'P_S': '[P_S]',
        'P_NS': '[P_NS]',
        'RC_CM': '[RC_CM]',
        'R_ds': '[R_ds]',
    }

    # Compare results
    results, matlab_interp, bngl_interp = compare_results(matlab_df, bngl_df, species_mapping)

    # Create comparison plots
    print("\nGenerating comparison plots...")
    plot_comparison(matlab_interp, bngl_interp, species_mapping)

    # Create error heatmap
    print("Generating error heatmap...")
    plot_error_heatmap(results)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    max_rel_errors = [v['max_rel_error'] for v in results.values()]
    mean_rel_errors = [v['mean_rel_error'] for v in results.values()]

    print(f"Overall max relative error: {np.max(max_rel_errors):.4f}")
    print(f"Overall mean relative error: {np.mean(mean_rel_errors):.4f}")

    if np.max(max_rel_errors) < 0.01:
        print("\n✓ VALIDATION PASSED: BNGL model matches MATLAB model (< 1% error)")
    elif np.max(max_rel_errors) < 0.1:
        print("\n⚠ VALIDATION WARNING: BNGL model has small differences (< 10% error)")
    else:
        print("\n✗ VALIDATION FAILED: BNGL model has significant differences (> 10% error)")

    print("\n" + "="*80)


if __name__ == '__main__':
    main()
