https://towardsdatascience.com/deploy-containerized-plotly-dash-app-to-heroku-with-ci-cd-f82ca833375c


docker build -t fcscore project/.

docker run --rm -p 8050:8050 --name=fcscore fcscore