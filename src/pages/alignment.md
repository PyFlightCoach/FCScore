## Align Flown Data to Template

This stage takes quite a while and quite a few things happen:

1. Align the template to the flight based on the axis rates (roll, pitch and yaw) using dynamic time warping. The lateral (roll and yaw) axis rates are absolute as the roll, snap, spin and stallturn directions chosen by the pilot are not yet known.
2. Measure the optional parameters (speed, line length, loop diameter, roll direction etc.) for each element from the corresponding bit of flight log recoreded in the last stage.
3. Create a new template with the optional parameters measured in the last step.
4. Perform a second sequence alignment to the new template, this time without mirroring the lateral axis rates. 
5. Measure the elements again based on the new aligned data. 
6. Create a new template 
7. Check the element dimensions against each other within each manoeuvre and create the corrected template

