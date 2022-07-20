import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


class WindowGenerator():

    def __init__(self,
                 input_width,
                 label_width,
                 shift,
                 train_df,
                 val_df,
                 test_df,
                 label_columns=None):
        # Store the raw data.
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

        # Work out the label column indices.
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {
                name: i
                for i, name in enumerate(label_columns)
            }
        self.column_indices = {
            name: i
            for i, name in enumerate(train_df.columns)
        }

        # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(
            self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(
            self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'
        ])

    @property
    def train(self):
        return self.make_dataset(self.train_df)

    @property
    def val(self):
        return self.make_dataset(self.val_df)

    @property
    def test(self):
        return self.make_dataset(self.test_df, shuffle=False)

    @property
    def example(self):
        """Get and cache an example batch of `inputs, labels` for plotting."""
        result = getattr(self, '_example', None)
        if result is None:
            # No example batch was found, so get one from the `.train` dataset
            result = next(iter(self.train))
            # And cache it for next time
            self._example = result
        return result

    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tf.stack([
                labels[:, :, self.column_indices[name]]
                for name in self.label_columns
            ],
                              axis=-1)

        # Slicing doesn't preserve static shape information, so set the shapes
        # manually. This way the `tf.data.Datasets` are easier to inspect.
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    def plot_ts(self, model, title="Model forecast"):
        predictions = tf.squeeze(model.predict(self.test))
        predictions_size = len(predictions)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(
            4,
            1,
            figsize=(20, 40),
        )

        plot_time_series(ax1,
                         self.test_df.index[-predictions_size:],
                         self.test_df["meantemp"][-predictions_size:],
                         format="-",
                         label="Test data",
                         c='darkred')
        plot_time_series(ax1,
                         self.test_df.index[-predictions_size:],
                         predictions[:, self.column_indices["meantemp"]],
                         "Mean temperature (°C)",
                         format="o--",
                         label=title,
                         c='orange')
        plot_time_series(ax2,
                         self.test_df.index[-predictions_size:],
                         self.test_df["humidity"][-predictions_size:],
                         "Humidity (%)",
                         format="-",
                         label='Train data',
                         c='darkblue')
        plot_time_series(ax2,
                         self.test_df.index[-predictions_size:],
                         predictions[:, self.column_indices["humidity"]],
                         "Humidity (%)",
                         format="o--",
                         label=title,
                         c='lightblue')
        plot_time_series(ax3,
                         self.test_df.index[-predictions_size:],
                         self.test_df["wind_speed"][-predictions_size:],
                         "Wind speed (mph)",
                         format="-",
                         label='Train data',
                         c='darkgreen')
        plot_time_series(ax3,
                         self.test_df.index[-predictions_size:],
                         predictions[:, self.column_indices["wind_speed"]],
                         "Wind speed (mph)",
                         format="o--",
                         label=title,
                         c='lightgreen')
        plot_time_series(ax4,
                         self.test_df.index[-predictions_size:],
                         self.test_df["meanpressure"][-predictions_size:],
                         "Mean pressure (mbar)",
                         format="-",
                         label='Train data',
                         c='darkviolet')
        plot_time_series(ax4,
                         self.test_df.index[-predictions_size:],
                         predictions[:, self.column_indices["meanpressure"]],
                         "Mean pressure (mbar)",
                         format="o--",
                         label=title,
                         c='pink')

    def plot(self, model=None, plot_col='meantemp', max_subplots=3):
        inputs, labels = self.example
        plt.figure(figsize=(16, 8))
        plot_col_index = self.column_indices[plot_col]
        max_n = min(max_subplots, len(inputs))

        for n in range(max_n):
            plt.subplot(max_n, 1, n + 1)
            plt.ylabel(f'{plot_col} [normed]')
            plt.plot(self.input_indices,
                     inputs[n, :, plot_col_index],
                     label='Inputs',
                     marker='.',
                     zorder=-10)

            if self.label_columns:
                label_col_index = self.label_columns_indices.get(
                    plot_col, None)
            else:
                label_col_index = plot_col_index

            if label_col_index is None:
                continue

            plt.scatter(self.label_indices,
                        labels[n, :, label_col_index],
                        edgecolors='k',
                        label='Labels',
                        c='#2ca02c',
                        s=64)
            if model is not None:
                predictions = model(inputs)
                plt.scatter(self.label_indices,
                            predictions[n, :, label_col_index],
                            marker='X',
                            edgecolors='k',
                            label='Predictions',
                            c='#ff7f0e',
                            s=64)

            if n == 0:
                plt.legend()

        plt.xlabel('Time (day)')

    def make_dataset(self, data, shuffle=True):
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.utils.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=shuffle,
            batch_size=32,
        )

        ds = ds.map(self.split_window)

        return ds


class Baseline(tf.keras.Model):

    def call(self, inputs):
        return tf.expand_dims(inputs[:, -1, :], axis=1)


class CustomResidualWrapper(tf.keras.Model):

    def __init__(self, model):
        super().__init__()
        self.model = model

    def call(self, inputs, *args, **kwargs):
        delta = self.model(inputs, *args, **kwargs)

        # The prediction for each time step is the input
        # from the previous time step plus the delta
        # calculated by the model.
        res = inputs[:, -1, :] + delta
        return tf.expand_dims(res, axis=1)


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


def compile_and_fit(model, window, patience=10, epochs=100):
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=patience,
        mode='min',
        restore_best_weights=True)

    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=[tf.keras.metrics.MeanAbsoluteError()])

    history = model.fit(window.train,
                        epochs=epochs,
                        validation_data=window.val,
                        callbacks=[early_stopping])
    return history
