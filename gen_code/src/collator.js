var Node = require('./gnode');
var fs = require('fs');
var path = require('path');

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

      //link dependences
      //for (var i = 0; i < tables.length; i++) {
      //   if (!(nodes[i].elem.depends === null)) {
      //      nodes[i].depends_on(nodes.reduce(
      //      (prev, cur) => {
      //         if (cur.elem.name == nodes[i].elem.depends)
      //            return cur;
      //      }));
      //   }
      //}

      //link dependences
      nodes.forEach((node) => { 
         node.elem.depends.forEach((dependency) => {
            node.depends_on(nodes.filter((node) => {
               return (node.elem.name == dependency);
            })[0]);
         });
      }); 

      //gen order
      if (do_topo_sort)
         callback(null, {nodes: Node.topo_sort(nodes)});
      else
         callback(null, {nodes});
   }
}

var create_tables = function (options, callback) {
   var path_to_tables = options.path_to_tables;
   var do_topo_sort = options.do_topo_sort;
   var table_names = fs.readdirSync(path_to_tables); 
   
   table_names = table_names.filter((file_name) => {
      if (path.extname(path.join(path_to_tables,file_name)) == '.jst')
         return true;
      else
         return false;
   }); 
   
   var $tables = [];
   var working = table_names.length;
   table_names.forEach((file_name) => {
      fs.readFile(path.join(path_to_tables, file_name),
      (err, data) => {
         eval(data.toString());
         $tables.push($output);
         working--;
         if (!working) callback(null, {tables: $tables, do_topo_sort});
      }); 
   });
}

var collate = function (path_to_tables, callback, do_topo_sort = 'true') {
   create_tables({path_to_tables, do_topo_sort}, create_nodes(callback));
}

var collate_strip_nodes = function (path_to_tables, callback, do_topo_sort) {
   collate(path_to_tables, 
   (err, data) => {
      var tables = data.nodes.map((node) => {return node.elem});
      callback(null, {tables}); 
   },
   do_topo_sort);
}

module.exports = {collate_strip_nodes};
