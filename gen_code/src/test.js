var collator = require('./collator');
var gen = require('./gen');
var jsontosql = require('./jts.js');
var fs = require('fs');

var run = function(err, data) {
   data.tables.forEach((table) => {
      gen.gen_objects(table);
   });
   data.tables.forEach((table) => {
      console.log(table.name, table.elem, '\n');
   });
   var sql = [];
   data.tables.forEach((table) => {
      sql.push(jsontosql.jsontosql(table));
   });

   fs.writeFile('test.sql', ''); //empty file

   sql.forEach((table) => {
      var output = '';
      table.forEach((tuple) => {
         //chunk and write
         output += tuple + '\n';
      });
      //write with append
      fs.writeFile('test.sql', output, {flag: 'a'});
   });
}

collator.collate_strip_nodes('./definitions', run);
