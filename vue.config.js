const path = require('path');
const webpack = require('webpack');

module.exports = {
  chainWebpack: (config) => {
    config
      .entry('app')
      .clear()
      .add('./frontend/main.ts')
      .end();

    config.resolve.alias
      .set('@', path.join(__dirname, './frontend'));
  },
  configureWebpack: {
    plugins: [
      new webpack.EnvironmentPlugin(['API']),
    ],
  },
};
