In general a .jst file is a javascript file. It has a different name to
seperate it from .js files that may be used for maintanence or other tasks
in the definitions folder. To start the table to be outputed is an object
with the distinct name $output. This is for collating the tables. Each table
has access to a special variable called $tables that contains an array
of all the tables. All post functions have access to their own table
as an argument. Below is the definition of a table.

~~~~
//possible dependencies
//practice is to name them with a _
var _gen = require('./gen');
var $output = {
   name: 'Some Name',
   depends: [(some dependences or none)], // Ex. [], ['test'], etc.
   elem: [], //element that contains the tuples of values
   amount: X // X = some amount of tuples to generate
   options:
   [
      {
         name: 'some attribute name',
         type: 'SQL type',
         func: X() // some generator function to call to create values
      },
      //more attributes below
      {
         name: 'post',
         type: 'n/a',
         func: [/*list of post script functions*/]
      }
   ]
}
~~~~

~~~~
//Generator functions

//n: is the size of dictionary
//word_length: is the max length of the word (default full length)
gen_def_from_words(n = 100, word_length)

//tables: array of tables in jst reference as $tables
//foreign_table: string of foreign table name
//key_name: foreign key name
gen_fkey(tables, foreign_table, key_name)

//Post run functions

//options: array of attribute names for uniqueness
//   ex - options = [['id']] => id is unique
//   ex - options = [['id', 'name']] => (id,name) is unique
//   ex - options = [['id'],['id','name']] => both of the above
post_unique(options)
~~~~
