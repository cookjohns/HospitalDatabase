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
   var entry = [];
   var attr_name = '';
   for (var i = 0; i < num_entries; i++) {
      entry = [];
      //one less from options for the manditory
      //post function pass
      for (var j = 0; j < table.options.length - 1; j++) {
         attr_name = table.options[j].name;
         //constructs internal objects ref by attr_name
         entry[j] = {};
         entry[j].name = attr_name;
         entry[j].type = table.options[j].type;
         entry[j].value = table.options[j].func(entries, entry);
      }
      entries.push(entry);
   }

   table.elem = entries;

   //post scripts may only be ran on finished tables
   var functions = table.options[table.options.length - 1].func;
   for (var i = 0; i < functions.length; i++) {
      functions[i](table); 
   }
}

//Returns a function to be used for generation
//of random words from a word dictionary.
//The amount of data to randomly use
//can be selected with n. IE only first n words.
var gen_def_from_words = function(n = 100, word_length)
{
   return () => {
      var words = new Dict.Dictionary('words', 'words');
      //for no word_length restriction do not pass argument
      return words.rnd_def(n).substring(0, word_length);
   };
}

//Returns a random integer in the interval [start,end).
var gen_int = function(start = 0, end = 100)
{
   return () => {
      return Math.floor(Math.random()*(end-start) + start);
   };
}

//Returns a random real in the interval [start, end)
//singleprecision if set to true will round to singleprecision
//   by default double precision
var gen_real = function(start = 0, end = 100, singleprecision)
{
   return () => {
      if (singleprecision)
         return Math.fround(Math.random()*(end-start) + start);
      else
         return Math.random()*(end-start) + start;
   };
}

//generate from the ISO_8601 standard referenced from https://en.wikipedia.org/wiki/ISO_8601
//programmer should make sure that both date functions generate
//the same amount of data if using pair mode
//with exception that an end date may generate one less
//validly (ie started but never ended).
//unique is prepended to this function instead of a post function
//to prevent errors if the pairing functionality is used.
var gen_date = function(options)
{
   return ($table, $tuple) => {
      //define options
      var attr_name = options.attr_name;
      var id = (options.id
         + ($tuple.find((elem) => {return elem.name == attr_name;}) || {}).value
                || '');
      var pair = (options.pair || false);
      var start = (options.start || '');
      var end = (options.end || '');
      var receiver = (options.receiver || false);
      var retry_count = 1000;

      var input_start_date = new Date(start);
      var input_end_date = new Date(end);

      var rnd_date = function() {
         var date = new Date(start); 
         //sets year to current year or year thereafter
         date.setFullYear((Math.floor(Math.random()*
                     (input_end_date.getFullYear()
                      - input_start_date.getFullYear())
                      + input_start_date.getFullYear())
                      || date.getFullYear()));
         //sets month
         if (date.getFullYear() < input_end_date.getFullYear()
             && date.getFullYear() > input_start_date.getFullYear()) {
            //generate any month 0-11
            date.setMonth(Math.floor(Math.random() * 12));
         }
         else if (input_start_date.getFullYear() ==
                  input_end_date.getFullYear()) {
            date.setMonth(Math.floor(Math.random()*
                     (input_end_date.getMonth() - 
                      input_start_date.getMonth()) +
                      input_start_date.getMonth())); 
         }
         else if (input_start_date.getFullYear() ==
                  date.getFullYear()) {
            date.setMonth(Math.floor(Math.random()*
                     input_start_date.getMonth()));
         }
         else {
            date.setMonth(Math.floor(Math.random()*
                     input_end_date.getMonth()));
         }

         //not precise to days (possibly implement later)
         //also ignore different amounts of days by
         //only considering 0-27
         date.setDate(Math.floor(Math.random() * 28));

         //assign random timestamp
         date.setHours(Math.floor(Math.random() * 24));
         date.setMinutes(Math.floor(Math.random() * 60));
         date.setSeconds(Math.floor(Math.random() * 60));

         return date;
      }
      //construct singleton holder for pairs
      //this is used in sharing pairs across relations
      //and not allowing between
      gen_date.prototype.ids = (gen_date.prototype.ids || []);

      //uses a fifo queue to match pairings between runs
      if (receiver) {
         var index = gen_date.prototype.ids.findIndex((elem) => {
            return elem[0] ==  id;
         });

         var elem = gen_date.prototype.ids[index][2];
         // Thanks to http://stackoverflow.com/questions/5767325/remove-a-particular-element-from-an-array-in-javascript
         // for pointing the proper syntax out
         gen_date.prototype.ids.splice(index, 1);
         return elem.toISOString();
      }
      else {
         if (pair) {
            var i = 0;

            var prev_end_date = undefined;
            for (var j = gen_date.prototype.ids.length; j > -1; j--) {
                     if (gen_date.prototype.ids[j]
                         && gen_date.prototype.ids[j][0] == id)
                        prev_end_date = gen_date.prototype.ids[j][2];
            }

            if (prev_end_date) {
               while (i < retry_count) {
                  var start_date = rnd_date();
                  if (start_date > prev_end_date) {
                     break;
                  }
                  else i++;
               } 
               start_date = (i == retry_count) ? undefined : start_date;
            }
            else {
               var start_date = rnd_date();
            }

            i = 0
            while (i < retry_count) {
               var end_date = rnd_date();
               if (end_date > (start_date))
                  break;
               else i++;
            }
            end_date = (i == retry_count) ? start_date : end_date;

            gen_date.prototype.ids.push(
                  [id, start_date, end_date]);
            return start_date.toISOString();
         }
         else {
            return rnd_date().toISOString();
         }
      }
   }
}

var gen_date_fkey = function(id) {
   return () => {
      var index = gen_date.prototype.ids.findIndex((elem) => {
         return elem[0].startsWith(id);
      });

      return gen_date.prototype.ids[index][0].replace(id, '');
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
      //assume unique table names
      var opt = (tables || []).filter((table) => {
         return (table.name == foreign_table);
      }); 
      //return rnd f_key
      return (opt[0].elem[Math.floor(Math.random()*opt[0].elem.length)] || []).filter(
            (attr) => {
            //filters out all non-key attributes
            //assume unique attr names
            return (attr.name == key_name)
            })[0].value;
   };
}

var post_unique = function(options)
{
   return (table) => {
      var temp = table.elem;
      //Filter for each constrant in options
      options.forEach((constrant) => {
         //create a new array of [key, value]
         //pairs where keys are the unique attr tuples
         temp = temp.map((tuple) => {
            //return [key, value] pairs where
            //key is an array of selected attributes
            var f_tuple = tuple.filter((attr) => {
               return (constrant.includes(attr.name));
            });

            return [f_tuple, tuple];
         });

         //Use map to filter down to unique keys
         var unique_filter = {};
         temp.forEach((elem) => {
            unique_filter[elem[0].reduce((str, attr) => {return str += attr.value},'')] = elem;
         });

         //get all unique values from [key, value] pairs
         temp = [];
         for (var elem in unique_filter) {
            temp.push(unique_filter[elem][1]);
         };
      });

      //no need for return since table passed by reference
      table.elem = temp;
   }
}

//tables are described by this format
// + Name of relation: name
// + Depends on: depends[other_table_name, [...]]
// + Relation values: elem[]
//   -> elem is seperate obj described by options
// + Relation gen options and type: options

module.exports = {gen_objects, gen_def_from_words, gen_fkey,
                  gen_date, gen_date_fkey, gen_int, gen_real, post_unique};
