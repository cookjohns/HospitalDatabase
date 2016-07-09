var collator = require('./collator');
var gen = require('./gen');

var run = function(err, data) {
   data.tables.forEach((table) => {
      table.elem = gen.gen_objects(table);
   });
   console.log(data.tables[0].elem);
   console.log(data.tables[1].elem);
}

var tables = collator.collate_strip_nodes('./definitions', run);
