const clientError = require("../exceptions/clientError.js");

class inputError extends clientError {
    constructor(message) {
        super(message);
        this.name = 'inputError';
    }
}

module.exports = inputError;