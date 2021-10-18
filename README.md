# roofline-model-multiple-kernels

![alt text](https://github.com/Techercise/roofline-model-multiple-kernels/blob/main/Example_Roofline_Plot/LBM_C_Kernel.png)

## Repository Overview

The Python files in this repository come from the [NERSC Roofline-on-NVIDIA-GPUs GitLab repo](https://gitlab.com/NERSC/roofline-on-nvidia-gpus). The code from each Python script was modified in order to allow the code to plot multiple kernels (multiple points) from multiple CSV files.

## Suggested Use of this Repository
1. Format the data into the format the two examples csvs are in. Feel free to use them as a template and just change the FLOPS, and AI in each. **NOTE:** Even though Ranks and API are specified, you don’t necessarily need to change those in the csv because instead, you could have the programming model (OMP or OACC) and the number of ranks listed in the plot's legend.
2. Determine the precision the FLOPS are in. Are you using Double Precision for each app? Single Precision? Or both? If you only use Double Precision, in `nvidia_plot_roofline_multiple_kernels.py` on line 42, change `cmp_roofs = [('SP', 19.5), ('DP', 9.7)]` to just `cmp_roofs = [('DP', 9.7)]` and vice versa for only single precision.
3. If creating plots for multiple applications, make sure to change the file prefix in line 6 of `nvidia_postprocess_multiple_kernels.py` so that the Python scripts will read from the different spreadsheets.
4. On line 169 of `nvidia_plot_roofline_multiple_kernels.py`, you’ll see the statement:
`ax.text(xlim[0] * 1.1, ylim[1] / 1.1, 'LBM C Kernel', horizontalalignment='left'`
In that statement, the section that controls the text on the plot is where _LBM C Kernel_ is. When you change applications/kernels make sure to update the kernel name and/or application name to fit your use case.
5. On line 172 of `nvidia_plot_roofline_multiple_kernels.py`, you’ll save the roofline plot as an image. Name it something descriptive so you know what it represents such as _LBM_C_Kernel.png_ or _LBM_C_Kernel_OpenMP_Only.png_ etc.

## Related Repositories
* Again, feel free to check out the [NERSC Roofline-on-NVIDIA-GPUs GitLab repo](https://gitlab.com/NERSC/roofline-on-nvidia-gpus). The code from this repo allows a user to easily take date from NVIDIA's Nsight Compute and create an easy-to-read roofline model.
* Looking to create instruction roofline models for the AMD MI50, MI60, or MI100 GPUs? Check out my other repo here: [AMD-Instruction-Roofline-using-rocProf-Metrics](https://github.com/Techercise/AMD-Instruction-Roofline-using-rocProf-Metrics).
