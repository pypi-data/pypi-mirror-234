### Common fast data processing methods

#### Smooth

- smooth_MIS(x,y,factor=300): 
  - smooth data
- smooth_SF(x,y,factors=[5,3]): 
  - smooth data

### files processing

- get_files(directory, suffix): 
  - Read files with the same suffix in the folder and save them as a list

### plot figs

- add_fig(figsize=(10,8)): 
  - add a canvas, return ax

- plot_fig(ax,x,y,label="PotEng",linewidth=1,
  	factors=[199,3],color="r",savefig="temp.png",
  	xlabel="X axis",ylabel="Y axis",fontweight="bold",
  	dpi=300,transparent=True): 
  - plot fig