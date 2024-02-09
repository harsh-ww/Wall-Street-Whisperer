FROM node:18-alpine as base


FROM base as dev
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD [ "npm", "run", "dev:docker"]
