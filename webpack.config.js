const path = require('path');

module.exports = {
  mode: 'development',
  entry: ['./static/js/cal.mjs', './node_modules/@fullcalendar/core/index.global.min.js'],
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static', 'dist'),
    clean: true
  },
};
