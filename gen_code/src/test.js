var collator = require('./collator');
var gen = require('./gen');

var run = function(err, data) {
   data.tables.forEach((table) => {
      gen.gen_objects(table);
   });
   data.tables.forEach((table) => {
      console.log(table.name, table.elem, '\n');
   });
   return tables;
}

var tables = collator.collate_strip_nodes('./definitions', run);
