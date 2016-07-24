var Node = require('./gnode');
var fs = require('fs');
var path = require('path');

//Creates a callback function to be used
//with table generator in creating a DAG
//representation of the table dependencies.
//in: callback that follows (err, data)
//out: callback that follows (err, data)
var create_nodes = function (callback) {
   return (err, data) => { 
      var tables = data.tables;
      var do_topo_sort = data.do_topo_sort;
      //to node 
      var nodes = [];
      for (var i = 0; i < tables.length; i++) {
         var node = new Node.G_Node();
         node.elem = tables[i];
         nodes.push(node);
      } 

      //link dependencies
      nodes.forEach((node) => { 
         //link each dependency
         node.elem.depends.forEach((dependency) => {
            //find and return table of dependency
            node.depends_on(nodes.filter((node) => {
               return (node.elem.name == dependency);
            })[0]);
         });
      }); 

      //generate a dependency preserving
      //sorted array of nodes
      if (do_topo_sort)
         callback(null, {nodes: Node.topo_sort(nodes)});
      else
         callback(null, {nodes});
   }
}

//Function for creating tables from .jst files
//in: options (obj)
//     - path_to_tables - directory to .jst files
//     - do_topo_sort - boolean to topo sort 
//    callback - function following (err, data)
//callback out: data (obj)
//               - tables - array of tables
//               - do_topo_sort - boolean to topo sort
//
//Also creates a side variable of the tables array
//available to the individual tables. Useful for
//certain functions.
var create_tables = function (options, callback) {
   var path_to_tables = options.path_to_tables;
   var do_topo_sort = options.do_topo_sort;
   var table_names = fs.readdirSync(path_to_tables); 
   
   //filter out all none .jst files
   table_names = table_names.filter((file_name) => {
      if (path.extname(path.join(path_to_tables,file_name)) == '.jst')
         return true;
      else
         return false;
   }); 
   
   var $tables = [];
   //variable that is cast to true
   //only when work has yet completed
   var working = table_names.length;
   //reads in all tables and pushes them
   //into the tables array
   table_names.forEach((file_name) => {
      fs.readFile(path.join(path_to_tables, file_name),
      (err, data) => {
         //construct table object
         eval(data.toString());
         //push table object
         $tables.push($output);
         working--;
         //done reading all tables
         if (!working) callback(null, {tables: $tables, do_topo_sort});
      }); 
   });
}

//Collates all the individual table files together and optionally sorts them.
//Refactoring can be done in the sorting method to get rid of this function.
//In: obvious
var collate = function (path_to_tables, callback, do_topo_sort = 'true') {
   if (do_topo_sort == undefined) do_topo_sort = true;
   create_tables({path_to_tables, do_topo_sort}, create_nodes(callback));
}

//Same as collate except strips nodes.
//In: obvious
var collate_strip_nodes = function (path_to_tables, callback, do_topo_sort) {
   collate(path_to_tables, 
   (err, data) => {
      var tables = data.nodes.map((node) => {return node.elem});
      callback(null, {tables}); 
   },
   do_topo_sort);
}

module.exports = {collate_strip_nodes};
