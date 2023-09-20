# FCScore Changelog

#### Outstanding Issues
AP - Centering criteria does not currently reflect a judges approach. Within a single manoeuvre a human judge will have a number of center checks at key points, rather than a single check of the overall geometry. Add optional additional center checks to the sequence definition.\
AU - Corrected template often does not look all that close to the flown data. perhaps an issue with averaging.\
TD - line before and after spin and stallturn is scored as a normal line, where in fact track criteria should be relaxed slightly\
TD - Roll angle visibility can be too easy, take highest visibility from anywhere between flown and template, rather than current visiblity of flown attitude. If the wings pass through the sight vector it is very obvious.\
TD - snaps and spins are not currently assessed\
TD - Proces for manual adjustment of sequence alignment is not logical\
AU - need an easy mode\
TD - track visibility is not always correct. change to scale based on angle between view vector and the velocity error, rather than the axis the error happens about.\
TD - Y and Z track visibility need to be considered together. For example getting closer can hide a reduction in height.\
AU - need to consider case of no visible line between manoeuvres. Also where there is a short line it can be hard to split inside the line with the flight coach plotter.

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
Initial Version

#### Closed Issues
fixed 20/09/2023 - AU - Display version number\
fixed 20/09/2023 - AU - error in P25 loop, sometimes gives negative downgrades and incorrect intended templates\
fixed 14/09/2023 - AU - P23 figure M exited in wrong direction, not zeroed and remaining sequence scored when it should be zero.