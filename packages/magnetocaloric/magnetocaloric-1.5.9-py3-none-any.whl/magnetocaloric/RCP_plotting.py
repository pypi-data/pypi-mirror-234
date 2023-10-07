import numpy as np
import matplotlib.pyplot as plt

def RCP_plotting(g_name, M_unit, H_unit, T_unit, T_FWHM_con, T_FWHM_con_final, Label_one, RCP_con, RCP_final, H_for_RCP, samp_name):
    """
    Plot Relative Cooling Power (RCP) and Full Width at Half Maximum (T_FWHM) against magnetic field (H).

    Args:
        T_FWHM_con (list): List of calculated FWHM values.
        Label_one (list): List of temperature values.
        RCP_con (list): List of calculated RCP values for all temperatures.
        RCP_final (list): List of RCP values with sufficient data.
        H_for_RCP (list): List of magnetic field values corresponding to RCP.
        samp_name (str): Name of the sample.

    Returns:
        None: The function only plots the RCP/T_FWHM vs H graphs.
    """
    if (g_name== 'RCP_plot' or g_name== 'all_plots'):
        samp_name_plus_RCP = "RCP (" + samp_name + ") :: max val : " + str(np.max(RCP_con)) + "(" + str(M_unit) + ")." + str(H_unit)
        samp_name_plus_T_FWHM = "T_FWHM (" + samp_name + ") :: max width : " + str(np.max(T_FWHM_con)) + str(T_unit)

        if len(RCP_final) >= 2:
            fig, ax1 = plt.subplots()
            ax1.set_xlabel(f"Magnetic Field(H) {H_unit}")
            ax1.set_ylabel(f"RCP ({M_unit}).{H_unit}")
            ax1.plot(H_for_RCP, RCP_final, linestyle='solid', marker='o', label=samp_name_plus_RCP, color='r', markersize=5, linewidth=0.5)
            ax1.legend(loc='upper left', frameon=False, ncol=2)
            ax1.tick_params(axis='y')

            ax2 = ax1.twinx()
            ax2.set_ylabel(f"T_FWHM ({T_unit})")
            ax2.plot(H_for_RCP, T_FWHM_con_final, linestyle='-', marker='+', label=samp_name_plus_T_FWHM, color='black', markersize=7, linewidth=0.0)
            ax2.legend(loc='lower right', frameon=False, ncol=2)
            ax2.tick_params(axis='y')

            plt.title("Field depedence of RCP/T_FWHM")
            plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
            plt.show()
            print ("</> request for RCP_plot ----> accepted & generated ")
        else:
            print ("</> request for RCP_plot ----> denied for insufficient data ")

    return
