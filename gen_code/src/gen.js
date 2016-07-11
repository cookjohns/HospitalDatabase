var Node = require('./gnode');
var Dict = require('./dict');

//Given a table generates all
//the required tuples.
//Still needs to implement unique
//constrants (maybe). Or let db
//reject all infringing tuples.
var gen_objects = function(table)
{
   var num_entries = table.amount;
   var entries = [];
   var entry = {};
   var attr_name = '';
   for (var i = 0; i < num_entries; i++) {
      entry = {};
      //one less from options for the manditory
      //post function pass
      for (var j = 0; j < table.options.length - 1; j++) {
         attr_name = table.options[j].name;
         //constructs internal objects ref by attr_name
         entry[attr_name] = {};
         entry[attr_name].type = table.options[j].type;
         entry[attr_name].value = table.options[j].func();
      }
      entries.push(entry);
   }

   //post scripts may only be ran on finished tables
   var functions = table.options[table.options.length - 1];
   for (var i = 0; i < functions.length; i++) {
      functions[i](); 
   }

   table.elem = entries;
}

//Returns a function to be used for generation
//of random words from a word dictionary.
//The amount of data to randomly use
//can be selected with n. IE only first n words.
var gen_def_from_words = function(n = 100)
{
   return () => {
      var words = new Dict.Dictionary('words', 'words');
      return words.rnd_def(n);
   };
}

//Returns a function that can be used to get
//valide foreign keys in a table. Must have
//specified proper dependencies and topo-sorted
//for this function to work properly.
var gen_fkey = function(tables, foreign_table, key_name)
{
   return () => {
      //find foreign table
      //assume no duplicate tables
      var opt = tables.filter((table) => {
         return (table.name == foreign_table);
      }); 
      //return rnd f_key
      return opt[0].
         elem[Math.floor(Math.random()*opt[0].elem.length)][key_name].value;
   };
}

var post_unique = function(table, options)
{
   var temp = table.elem;
   //Filter for each constrant in options
   option.forEach((constrant) => {
      //create a new array of [key, value]
      //pairs where keys are the unique attr tuples
      temp = temp.map((tuple) => {
         //return [key, value] pairs where
         //key is an array of selected attributes
         return [tuple.filter((attr) => {
            return (attr in constrant);
         }), tuple];
      });

      //Use map to filter down to unique keys
      var unique_filter = new Map();
      temp.forEach((elem) => {
         unique_filter.set(elem[0].join(''), elem);
      });

      //get all unique [key, value] pairs
      temp = unique_filter.values();

      //get remaining tuples
      temp = temp[1]; //all non-infringing tuples
   });

   //no need for return since table passed by reference
}

//tables are described by this format
// + Name of relation: name
// + Depends on: depends[other_table_name, [...]]
// + Relation values: elem[]
//   -> elem is seperate obj described by options
// + Relation gen options and type: options

module.exports = {gen_objects, gen_def_from_words, gen_fkey};
