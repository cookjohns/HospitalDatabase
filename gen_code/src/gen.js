var Node = require('./gnode');
var Dict = require('./dict');

var gen_objects = function(table)
{
   var num_entries = table.amount;
   var entries = [];
   var entry = {};
   var attr_name = '';
   for (var i = 0; i < num_entries; i++) {
      entry = {};
      for (var j = 0; j < table.options.length; j++) {
         attr_name = table.options[j].name;
         //constructs internal objects ref by attr_name
         entry[attr_name] = {};
         entry[attr_name].type = table.options[j].type;
         entry[attr_name].value = table.options[j].func();
      }
      entries.push(entry);
   }
   return entries;
}

var gen_def_from_words = function(n = 100)
{
   return () => {
      var words = new Dict.Dictionary('words', 'words');
      return words.rnd_def(n);
   };
}

var gen_fkey = function(tables, foreign_table, key_name)
{
   return () => {
      var opt = tables.filter((table) => {
         return (table.name == foreign_table);
      }); 
      return opt[0].
         elem[Math.floor(Math.random()*opt[0].elem.length)][key_name].value;
   };
}

//tables are described by this format
// + Name of relation: name
// + Depends on: depends[other_table_name, [...]]
// + Relation values: elem[]
//   -> elem is seperate obj described by options
// + Relation gen options and type: options

module.exports = {gen_objects, gen_def_from_words, gen_fkey};
