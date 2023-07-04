const path = require('path');

module.exports = {
  mode: 'development',
  entry: ['./static/js/cal.js'],
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static', 'dist'),
    clean: true
  },
};
