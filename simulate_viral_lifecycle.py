#!/usr/bin/env python3
"""
Simulate viral lifecycle model using BioNetGen and libroadrunner

This script:
1. Uses bionetgen Python package to parse and run BNGL files
2. Exports to SBML format
3. Simulates using libroadrunner
4. Plots the results
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def simulate_with_bionetgen(bngl_file, t_end=2880, n_points=200):
    """
    Simulate the model using bionetgen Python package and libroadrunner

    Parameters:
    -----------
    bngl_file : str
        Path to BNGL file
    t_end : float
        End time for simulation (minutes)
    n_points : int
        Number of time points

    Returns:
    --------
    result : numpy array
        Simulation results
    rr : roadrunner.RoadRunner
        RoadRunner object
    """
    try:
        import bionetgen
        import roadrunner
    except ImportError as e:
        print(f"ERROR: Required package not installed: {e}")
        print("Install with: pip install bionetgen libroadrunner")
        sys.exit(1)

    print(f"Processing BNGL file: {bngl_file}")

    # Use bionetgen to run the model
    # The bionetgen package can generate SBML from BNGL
    try:
        # Run BioNetGen on the BNGL file to generate SBML
        result = bionetgen.run(bngl_file)
        print("BioNetGen execution successful!")

        # Find the generated SBML file
        base_name = os.path.splitext(os.path.basename(bngl_file))[0]
        output_dir = os.path.dirname(bngl_file) or '.'
        sbml_file = os.path.join(output_dir, base_name + '.xml')

        if not os.path.exists(sbml_file):
            print(f"Warning: SBML file not found at {sbml_file}")
            print("Attempting to generate SBML explicitly...")

            # Try alternative method: use bionetgen to explicitly generate SBML
            import bionetgen.core as core
            model = core.model(bngl_file)
            model.generate_xml()

            if not os.path.exists(sbml_file):
                print("ERROR: Failed to generate SBML file")
                sys.exit(1)

        print(f"Loading SBML model from: {sbml_file}")
        rr = roadrunner.RoadRunner(sbml_file)

        # Set simulation parameters
        print(f"Simulating from 0 to {t_end} minutes with {n_points} points...")
        result = rr.simulate(0, t_end, n_points)

        print("Simulation completed successfully!")
        return result, rr

    except Exception as e:
        print(f"ERROR during BioNetGen execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def plot_results(result, species_to_plot=None, log_scale=True, save_prefix='viral_lifecycle'):
    """
    Plot simulation results

    Parameters:
    -----------
    result : numpy array
        Simulation results from libroadrunner
    species_to_plot : list, optional
        List of species names to plot. If None, plots key species.
    log_scale : bool
        Use log scale for y-axis
    save_prefix : str
        Prefix for saved figure files
    """
    # Convert time from minutes to hours
    time_hours = result['time'] / 60.0

    # Default species to plot
    if species_to_plot is None:
        species_to_plot = [
            '[V_E]',    # Extracellular virus
            '[V_I]',    # Intracellular virus
            '[R_cyt]',  # Cytoplasmic RNA
            '[P_S]',    # Structural protein
            '[R_ds]',   # dsRNA
        ]

    # Create figure with subplots
    n_species = len(species_to_plot)
    fig, axes = plt.subplots(n_species, 1, figsize=(10, 3*n_species))

    if n_species == 1:
        axes = [axes]

    for i, species in enumerate(species_to_plot):
        try:
            # Try to get data for this species
            data = result[species]
            axes[i].plot(time_hours, data, linewidth=2, color='blue')
            axes[i].set_ylabel(species, fontsize=12)
            axes[i].set_xlabel('Time (hours)', fontsize=12)
            axes[i].grid(True, alpha=0.3)

            if log_scale and np.any(data > 0):
                axes[i].set_yscale('log')

            axes[i].set_xlim([0, time_hours[-1]])

        except KeyError:
            print(f"Warning: Species {species} not found in results")
            axes[i].text(0.5, 0.5, f'{species}\nNot Found',
                        ha='center', va='center', transform=axes[i].transAxes)

    plt.tight_layout()

    # Save figure
    fig_file = f'{save_prefix}_timecourse.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"Figure saved as: {fig_file}")

    plt.show()

    return fig


def main():
    """Main execution function"""

    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bngl_file = os.path.join(script_dir, 'viral_lifecycle.bngl')

    if not os.path.exists(bngl_file):
        print(f"ERROR: BNGL file not found: {bngl_file}")
        sys.exit(1)

    print("="*60)
    print("Viral Lifecycle Model Simulation")
    print("="*60)
    print(f"BNGL file: {bngl_file}\n")

    # Run BioNetGen and simulate
    try:
        # Simulate using bionetgen and libroadrunner
        result, rr = simulate_with_bionetgen(
            bngl_file,
            t_end=2880,  # 48 hours
            n_points=200
        )

        print("\n" + "="*60)
        print("Simulation Results Summary")
        print("="*60)
        print(f"Time range: {result['time'][0]:.1f} - {result['time'][-1]:.1f} minutes")
        print(f"           ({result['time'][0]/60:.1f} - {result['time'][-1]/60:.1f} hours)")

        # Print final values for key species
        print("\nFinal values:")
        key_species = ['[V_E]', '[V_I]', '[R_cyt]', '[P_S]', '[R_ds]']
        for species in key_species:
            try:
                final_val = result[species][-1]
                print(f"  {species:12s}: {final_val:.2e}")
            except KeyError:
                print(f"  {species:12s}: Not found")

        # Plot results
        print("\nGenerating plots...")
        plot_results(result, log_scale=True, save_prefix='viral_lifecycle')

        # Save data to CSV
        csv_file = os.path.join(script_dir, 'viral_lifecycle_results.csv')
        import pandas as pd
        df = pd.DataFrame(result)
        df['time_hours'] = df['time'] / 60.0
        df.to_csv(csv_file, index=False)
        print(f"\nResults saved to: {csv_file}")

        print("\n" + "="*60)
        print("Simulation completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\nERROR during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
