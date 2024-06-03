class clientError extends Error {
  constructor(message, statusCode = 400) {
      super(message);
      this.statusCode = statusCode;
      this.name = 'clientError';
  }
}

module.exports = clientError;