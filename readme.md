This project combines the api and client for FCScore. FCScore is a WIP tool for automatic judging at F3A competitions. The easiest way to use FCScore is with Docker\
\
To run:\
git clone git@github.com:PyFlightCoach/FCScore.git\
cd FCScore/project\
docker compose up\
\
Once it is running, open a web browser to: localhost/5173\
to stop the server: docker compose -p project kill
\
\
To Deploy:\
https://www.docker.com/blog/how-to-deploy-containers-to-azure-aci-using-docker-cli-and-compose/
