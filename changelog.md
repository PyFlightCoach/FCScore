# FCScore Changelog

#### Outstanding Issues / Features
AU - Corrected template often does not look all that close to the flown data. perhaps an issue with averaging.\
AU - Need to consider case of no visible line between manoeuvres.\
TD - Allow picking up some of previous / next manoeuvre when splitting has been done poorly.\
TD - Can't handle cross box start / finish of manoeuvres for IMAC.
AU - error when no velocity data is available in the fc json.\
AU - include some kind of weighting to make longer manoeuvres be judged less harshly.\
JT - error in P25 template when it is run through FCSCore.\
TD - add short element between opposing rolls to fix alignment issues when a pause is flown. Include length downgrade for it.\
AU - add option to manually edit scores for failed analyses.\

#### Client: next, Server: next
update measurements so the ratio calculation is performed on construction if necessary.\
Adjust ratio calculation so expected value is zero (ratio of 1), negative values are for 1/ratio if ratio <1, positive values when ratio > 1.\
new snap and spin elements to replace old break, autorotation and recovery elements.\
seperate smoothing into a seperate process, rather than including it in the criteria, make smoothing configurable per eldef.\
Add concept of selectors, to downselect the data within an element that is passed to the criteria.\
apply continuous criteria visibility factoring before smoothing the sample and getting downgrades.\
Add downgrades for snap and spin.\
update stallturn scoring.\
add Peak criteria to downgrade the biggest absolute value in a sample.\
replace ContRat and ContAbs with single continuous criteria.\
replace intra element convolve smoothing with low pass filter.\

#### Client: v0.1.4, Server: v0.1.4
Add run button to client score table to re-run individual manoeuvres.\
Fix bug in loop intra roll angle which was always showing 0.\
reduce averaging width for intra track errors.

#### Client: v0.1.4, Server: v0.1.3
Move Intra criteria from element to element definition to allow other disciplines and more refined tailoring of criteria selection.\
Allow speed and track errors on lines before and after stallturns and spins.\
Fix intra speed criteria where it was giving incorrect values in some cases.\
Better version handling in client.\
Add fa_version to score message in case server is changed mid analysis.\
Refactor alignment optimisation, minor bug fixes.

#### Client: v0.1.3, Server: v0.1.2
Label browser tab with schedule and fcj name.

#### Client: v0.1.2, Server: v0.1.2
Add example flight.\
Add instructions to main page.\
reduce visibility factor weigting from 0.2 to 0.1 for errors parallel to view vector.\
add variable convolve width for different kinds of intra criteria.

#### Client: v0.1.1, Server: v0.1.1
Enable output to FCJSON.\
Move difficulty and truncate settings to server.\
Label shift bugfix.\
change client dockerfile so it deploys static app.\
refactor client.

#### Client: 0.1.0, Server: 0.1.0
Adjust inter visibility as its too harsh in many cases.\
refactor messages to minimise data transferred.\
Add analysis server selection option to client.\
build client as a static site and deploy on github pages.\
fix bug on sequence alignment where lable could be reduced to 1 data point.\

#### Client: v0.0.14, Server: v0.0.14
Adjust splitting logic to include first datapoint of the next label as the last value in the extracted item. \
Fix the inter radius and inter line length criteria which had an exponent < 1.
Adjust inter visibility factoring to account for the size of the element. 1 if >= 0.5 of box height, scaling to 0 for zero height. Adjust visibility factor
selection logic to suit (take max of previous and current).\
Change intra element track visiblity round loops so it considers the loop axial vector at each point rather than interpolating between the visibility values at the start and end.\
Make box scoring a little more harsh.

#### Client: v0.0.13, Server: v0.0.13
reduce sample std deviation when convolve width is less than max.\
take min visibility of current and previous element for inter element downgrades.\
Fix the schedule positioning so that it matches the plotter.

#### Client: v0.0.12, Server: v0.0.12
Reduce convolve width for short element continuous criteriea rather than assuming linear interpolation between start and end.\
pick up wind direction from first manoeuvre rather than takeoff.\
Add button to recalculate scores and to rerun aligment optimisation to the alignment page.\
display intra, inter and position downgrades on top bar whem manoeuvre is active.\
Change roll angle visibility so it considers worst case of anywhere between flown and template.\
Fix bug on handling alignment failures to allow manual editing and re-running.\
Fix version numbering to use git tag rather than commit id. 

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
fixed 20/08/2024 - AM - stallturn track critetia should be removed in y as well as z.\
fixed 20/08/2024 - AM - snap roll angle error is measured at end of autorotation and recovery, this is double accounting.\
fixed 20/08/2024 - TD - Snaps and spins are not currently assessed\
fixed 11/07/2024 - TD - Line before and after spin and stallturn is scored as a normal line, where track criteria should be relaxed\
fixed 11/07/2024 - TD - remove speed criteria around stallturns and spins.
fixed 11/07/2024 - TD - error in speed criteria, goes to zero in some cases. 
fixed 01/07/2024 - TD - reduce or remove smoothing on intra track criteria as downgrades are missed in short elements and this data is less noisy than curvature or roll angle.
fixed 16/05/2024 - TD - Box downgrades are too kind. Perhaps change to 10 points for the whole manoeuvre 7.5 degrees outside the box, rather than 15 degrees.\
fixed 16/05/2024 - TD - Intra track visiblity round loops doesn't make much sense.\
fixed 15/05/2024 - TD - inter visilibility, consider size of the element, smaller elements are harder to see and have larger ratio errors so are disproportionately harsh.\
fixed 14/05/2024 - TD - one datapoint lost when splitting.\
fixed 07/05/2024 - TD - Position of flown data does not always match the plotter.\ 
fixed 07/05/2024 - TD - inter visibility, take min value of current and previous element.\
fixed 07/05/2024 - TD - Intra smoothing. Factor errors down to account for reduced convolve width when sample has less than 40 datapoints.\
fixed 03/05/2024 - TD - Make version numbering more logical.\
fixed 27/04/2024 - TD - roll angle visiblity should consider worst case of anywhwere between flown and template roll angle, rather than just flown.\
fixed 22/04/2024 - MH - error in direction selection when takeoff is perormed downwind.\
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
