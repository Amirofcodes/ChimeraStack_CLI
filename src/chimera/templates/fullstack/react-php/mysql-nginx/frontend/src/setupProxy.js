const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: process.env.REACT_APP_BACKEND_URL || `http://localhost:${process.env.BACKEND_PORT}`,
      pathRewrite: {
        "^/api": "/api",
      },
      changeOrigin: true,
    })
  );
};