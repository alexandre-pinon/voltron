def plot_time_series(ax,
                     timesteps,
                     values,
                     title=None,
                     format='.',
                     start=0,
                     end=None,
                     label=None,
                     c='b'):
    """
  Plots a timesteps (a series of points in time) against values (a series of values across timesteps).
  
  Parameters
  ---------
  ax : matplotlib.Axes to plot
  timesteps : array of timesteps
  values : array of values across time
  title : title of plot
  format : style of plot, default "."
  start : where to start the plot (setting a value will index from start of timesteps & values)
  end : where to end the plot (setting a value will index from end of timesteps & values)
  label : label to show on plot of values
  c : color, default 'blue'
  """
    ax.plot(timesteps[start:end], values[start:end], format, c=c, label=label)
    ax.set_xlabel("Time")
    ax.tick_params('x', labelrotation=45)
    ax.grid(True)

    if title:
        ax.set_title(title, fontsize=16)
    if label:
        ax.legend(fontsize=14, loc='upper left')
