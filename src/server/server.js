require('dotenv').config();

const Hapi = require('@hapi/hapi');
const routes = require('../server/routes');
const loadModel = require('../services/loadModel');
const InputError = require('../exceptions/inputError');

//Start hapi server di 0.0.0.0
(async () => {
    const server = Hapi.server({
        port: 8000,
        host: '0.0.0.0',
        routes: {
            cors: {
              origin: ['*'],
            },
        },
    });

    //Model belum ada, bisa ditambahkan di .env nya.
    const model = await loadModel();
    server.app.model = model;

    server.route(routes);

    //ON-PRERESPONSE FUNCTION, FOR HANDLING THE ERROR BEFORE IT BEGINS.
    //THIS MACHINE WILL RUN THIS ALLL FIRST.
    server.ext('onPreResponse', function (request, h) {
        const response = request.response;

        // Error jika foto tidak di detekdi daun sama sekali.
        if (response instanceof InputError) {
            const newResponse = h.response({
                status: 'fail',
                message: `${response.message} Silakan gunakan foto lain.`
            })
            newResponse.code(response.statusCode)
            return newResponse;
        }

        //
        if (response.isBoom) {
            const newResponse = h.response({
                status: 'fail',
                message: response.message
            })
            newResponse.code(response.output.statusCode)
            return newResponse;
        }

        return h.continue;
    });

    await server.start();
    console.log(`Server start at: ${server.info.uri}`);
})();