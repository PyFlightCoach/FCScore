# FCScore Changelog

#### Outstanding Issues / Features
AU - Corrected template often does not look all that close to the flown data. perhaps an issue with averaging.\
TD - Line before and after spin and stallturn is scored as a normal line, where track criteria should be relaxed\
TD - Snaps and spins are not currently assessed\
AU - Need to consider case of no visible line between manoeuvres. Also where there is a short line it can be hard to split inside the line with the flight coach plotter.\
TD - Allow picking up some of previous / next manoeuvre when splitting has been done poorly.\
TD - Can't handle cross box start / finish of manoeuvres for IMAC.
TD - pyodide server option\
TD - Make version numbering more logical.\
AU - error when POS / ATT data selected in the plotter rather than XKF1.\
AU - include some kind of weighting to make longer manoeuvres be judged less harshly.\
JT - error in P25 template when it is run through FCSCore./

#### Client: cbb786b5a3, Server: 272626d7
Fix bug in the P25 template loop where roll direction options were not picked up.\
Improve Intra single downgrade plots.\
Add smoothing to continuous absolute criteria and increase smoothing on continuous ratio criteria.\
Improve accounting for continuous criteria region not picked up by convolve.\
Handle optional manoevures where the number or order of elements changes.\
Round down the sum of each type of intra element downgrade within a manoeuvre before adding them up.\
Make easy the default mode and persiest between runs.\
Include pilot and center altitude in the fc json so top box criteria works at places above sea level.\
Refactor analysis api to standardise python and server interface and logic.\
Add nose drop angle criteria to constrain spin alignment optimisation.\
Add logic to count number of autorotations performed.\

#### Client: cec7e3c1fa, Server: 397ef11
Fix bug in continuous criteria where final points of sample were ignored.\
Add plots and colouring to Inter element results\
Add fun 3D visualisation in summary and intra pages.\
update docker compose file so it works in windows too.

#### Client: e8fded8, Server: d1310ef00
Update schedule definition to cope with new flight coach plotter naming convention.

#### Client: 00f641f0, Server: 771ea037
Use curvature rather than radius for intra element scoring to avoid divide by zero on straight lines.\
standardise export format between client and server.

#### Client: f536a35, Server: 9ca4322
run 16 instances of backend to speed things up a bit\
Include split point optimisation to give minimum intra downgrade.\
Correct roll angle visibility round loops and stallturns.\
Correct roll angle measurement to look at the angle between a body frame vector and the corresponding ref frame vector, rather than just comparing flown to template.\
Add new bounded criteria, to downgrade only when the measurement is above, below, inside or outside a bound. This is useful for assessing things like stallturn
width, snap angle of attack etc. Currently just used for snap break/recovery length and stallturn width.\
Fix bug that causes crashes when intra plot is clicked whilst a criteria is active.\
Generally refactor client side logic.\
Added option to export analysis and load from exported analysis.

#### Client: f70966, Server: 1f05393
Add an Easy mode\
Improve appearance and plots\
simplify alignment adjustment\
run a low pass filter over all log data before doing any processing\
only smooth data if its passing through a ratio criteria\
include example log\

#### Client: c65cff8, Server: 4d2db89
Add colouring to intra table and graphs to highlight more significant downgrades.\
Restructuring of base data structures.\
Remove outliers from measurements before smoothing to avoid bad data causing downgrades.\
Allow the definition of more than one centre per manoeuvre as centred points or elements in the template and populate the positioning information page in the client.\
Add position visibility to all visibility calculations.\
Apply smoothing before taking the magnitude of the measurement, so it goes to zero when.\
Calculate visibility factors for absolute errors and apply to the downgrade (as per ratio errors), rather than to the error. This means that a constant error cannot be downgraded twice.\
Colour items in tables and graphs to highlight the more critical downgrades.

#### Client: 708e39b, Server: 040d7a5, 10/10/2023
Update measuement data structure\
Improve visibility factoring to account for combined y and z track errors.\
Occasional errors with detecting sequence direction

#### Client: 4373dd3, Server: e986601, 20/09/2023
Improve measurement smoothing in intra element criteria\
Calculate average radius based on average weighted with incremental angle\
Sequence alignment label squashing Bug Fix\
Correction to radius calculation for rolling loops

#### Client: f3e32af, Server: 68a4a79, 14/09/2023
Prevent sequence alignemnt squashing labells to zero length\
Adjust visibility factoring application logic for Intra Criteria\
First pass at visibility factoring for Inter Element Criteria\
Force direction of template generation to be correct wrt first manoeuvre in sequence, not driven by flight direction of current manoeuvre.

#### Client: f592d7f, Server: 92acc4b, 13/09/2023
Start of changelog

#### Closed Issues
fixed 16/04/2024 - AU - round down downgrade for each criteria before adding up.\
fixed 16/04/2024 - JT,AU - difficult to see errors are still too harsh.\
fixed 16/04/2024 - MH - Roll angle criteria is too harsh round loops.\
fixed 09/04/2024 - AU - adjust distance visibility factors so downgrades are less harsh in the center.\
fixed 09/04/2024 - TD - consider distance from ground reference in visibility easements.\
fixed 08/04/2024 - JT - make easy the default mode and persist choice between runs.\
fixed 07/04/2024 - AU - Issue with manoeuvre positionoing, sometimes does not match position shown in the plotter.\
fixed 07/04/2024 - TD - Options on Maneouvres do not work then the number or order of the elements change, only roll directions. This is a problem for the top hat in P25. It will need manual intervention to specify which option was flown, or more advanced element recognition.\
fixed 25/03/2024 - TD - amount of rolls / autorotations need to be counted, just the end angle, allows unbounded optimisation in some cases and misses hard zeros.\
fixed 25/03/2024 - TD - breaks, nose drops and recoveries are occasionally not fully constrained during split optimisation.\
fixed 20/03/2024 - TD - add plots to inter\
fixed 11/08/2023 - TD - Continuous criteria peaks / troughs are not picking up the first / last points of a sample (should always be a peak or trough). This is causing the split optimisation to give funny results in some cases, for example at the end of loops where the curvature reduces before a line. \
fixed 07/01/2023 - TD -Visibility can be too easy (or hard), take highest (or some average) visibility from anywhere between flown and template, rather than current visiblity of flown attitude. For example, with roll angle if the wings pass through the sight vector it is very obvious.\
fixed 07/01/2023 - TD - Stallturn roll angle is not correct as velocity is small.\
fixed 07/01/2023 - TD - Stallturn width and speed are not considered\
fixed 02/01/2023 - TD - DTW does not necessarily provide an optimimum split. In some cases score can be improved.\
fixed 02/01/2023 - TD - Roll angle visibility in stallturns doesn't work correctly. Better to compare angle between wing vector and vector rejection of wing vector on the template xy plane, rather than just use the normal line / loop roll angle method\
fixed 26/12/2023 - TD - Need a means of exporting the splitting and score information to facilitate competitions, comparisons to previous versions etc.\
fixed 19/12/2023 - TD - Proces for manual adjustment of sequence alignment is not logical\
fixed 19/12/2023 - AU - need an easy mode\
fixed 30/10/2023 - AP - Centering criteria does not currently reflect a judges approach. Within a single manoeuvre a human judge will have a number of center checks at key points, rather than a single check of the overall geometry. Add optional additional center checks to the sequence definition.\
fixed 10/10/2023 - TD - track visibility is not always correct. change to scale based on angle between view vector and the velocity error, rather than the axis the error happens about.\
fixed 10/10/2023 - TD - Y and Z track visibility need to be considered together. For example getting closer can hide a reduction in height.\
fixed 20/09/2023 - AU - Display version number\
fixed 20/09/2023 - AU - error in P25 loop, sometimes gives negative downgrades and incorrect intended templates\
fixed 14/09/2023 - AU - P23 figure M exited in wrong direction, not zeroed and remaining sequence scored when it should be zero.
