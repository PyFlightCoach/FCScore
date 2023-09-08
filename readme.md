This project combines the api and client for FCScore. FCScore is a WIP tool for automatic judging at F3A competitions.


To run:\
git clone git@github.com:PyFlightCoach/FCScore.git\
cd FCScore/project\
docker compose pull\
docker compose start\
\
To build:\
git clone git@github.com:PyFlightCoach/FCScore.git\
cd FCScore\
git submodule update --init --recursive\
cd project\
docker compose up
