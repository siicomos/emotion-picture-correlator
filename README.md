# Emotion Picture Correlator

## Project Overview

This is a web application whose main purpose is to make a user's face image as input and based on the face's emotion to find the most relevant list of GIF files from GIFGIF.com.

The intermediate process of detecting emotion and find the GIF is done in Machine Learning methods which involve OpenFace feature extraction, PCA transformation, and SVM Model.

## Requirements

- Docker version > 19.03.12
- Docker-Compose version > 1.25
- NodeJS version > 12.16.1
- NPM version > 6.13.4
- You need a webcam to take a picture of yourself (or your dog)!

## How to Run

- Frontend: `cd web/ && npm install && npm start`
- Create a file `secret.env` at `services/emotion-picture-correlator` with [GIFGIF API Key](https://developers.giphy.com/docs/api/endpoint#search)
  - This file is required to let the backend has access to the GIFGIF API endpoint so that it can display GIFs to you.
- Backend: `cd services/emotion-picture-correlator/ && ./run_emotional_correlator.sh && docker logs -f emotional-correlator`

Then, the webpage is available at `localhost:3030`