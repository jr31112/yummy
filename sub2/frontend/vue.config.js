module.exports = {
  chainWebpack: config => {
    config.module.rules.delete('eslint');
},

  publicPath: "/",
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000/"
      }
    }
  },
  transpileDependencies: ["vuetify"]
};
