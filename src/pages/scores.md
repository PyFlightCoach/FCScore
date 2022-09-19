## Scores

Here we have a breakdown of the final score for each manoeuvre and all the downgrades (note snaps, spins and stallturns don't work yet). 

- Intra element downgrades consider each element independently.
- Inter element downgrades compare elements within a manoeuvre (matching loop diameters, line lengths and so on). These comparisons are automatically defined and named when the sequence defintion is instantiated based on sporting code. 

notes:
- The amount of downgrade for a given error is specified roughly based on the sporting code, but is only preliminary and needs more thought.
- For intra element downgrades only increases in the absolute error are considered. Reductions in absolute error are free. The sum of increase in absolute error for all increasing regions within an element are considered. This could produce large downgrades if there is noise in the data. Perhaps some smoothing should be included first.
- The downgrades are truncated. At the moment this means that if an element is completed with less than 0.5 marks of error then this is not carried onto the next element. This needs more thought as a manoeuvre can look very wrong if you keep accumulating 0.49 mark errors in the same direction through consecutive elements.
- No consideration is given to how hard a downgrade is to see. This needs to be included to make the scores more representative of the percieved quality of a flight.
