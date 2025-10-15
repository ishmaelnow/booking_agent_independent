// swagger.js
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Your API Title',
      version: '1.0.0',
      description: 'API documentation for your backend',
    },
    servers: [
      {
        url: 'https://your-app.onrender.com/api', // Replace with your actual base URL
      },
    ],
  },
  apis: ['./routes/*.js'], // Adjust this path to where your route files live
};

const specs = swaggerJsdoc(options);
module.exports = { swaggerUi, specs };