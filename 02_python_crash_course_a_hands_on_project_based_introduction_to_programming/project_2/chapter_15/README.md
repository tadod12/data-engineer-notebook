# Data Visualization
## Generating Data
### Matplotlib
#### Method
1. scatter()
    ```
   ax.scatter(2, 4)  # plot 1 point at (2; 4)
   ax.scatter(2, 4, c=(0, 0.8, 0))  # color
   
   x_values = [1, 2, 3, 4, 5]
   y_values = [1, 4, 8, 16, 25]
   ax.scatter(x_values, y_values, c='red', s=100)  # plot 5 points
   
   # colormap
   ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)
   ```
   
2. plot()
    ```
   ax.plot(x_values, y_values, linewidth=3)  # plot line
   ```
   
3. axis()
    ```
   # Set range for each axis
   ax.axis([0, 1100, 0, 1100000])
   # x_values: from 0 to 1100
   # y_values: from 0 to 1100000
   ```
   
4. savefig()
    ```
   plt.savefig('squares_plot.png', bbox_inches='tight')
   # First argument: filename
   # Second argument: trims extra whitespace from the plot
   ```

5. subplots
   ```
   fig, ax = plt.subplots(figsize=(15, 9))
   # fig - entire figure
   # ax - a single plot, used to plot
   ```

#### Syntax
1. Plotting
    ```
   import matplotlib.pyplot as plt
   plt.style.use('seaborn')
   
   input_values = [1, 2, 3, 4, 5]
   squares = [1, 4, 9, 16, 25]
   
   fig, ax = plt.subplots()  # fig - entire figure, ax - a single plot
   ax.plot(input_values, squares, linewidth=3)
   
   # Set chart title and label axes
   ax.set_title('Square Numbers', fontsize=24)
   ax.set_xlabel('value', fontsize=14)
   ax.set_ylabel('square of value', fontsize=14)
   
   # Set size of tick labels
   ax.tick_params(axis='both', labelsize=14)
   
   plt.show()
   plt.savefig('quares_plot.png', bbox_inches='tight')
   ```
   
   More of Plotly
   https://plotly.com/python/creating-and-updating-figures/

2. Remove the axes
   ```
   ax.get_xaxis().set_visible(False)
   ax.get_yaxis().set_visible(False)
   ```
   
### Plotly
#### Example
`two_d8s.py` file