var Node = require('./gnode');
var Dict = require('./dict');

var gen_objects = function(table, num_entries)
{
   var entries = [];
   var entry = {};
   for (var i = 0; i < num_entries; i++) {
      for (var i = 0; i < table.options.length; i++) {
         var attr_name = table.options[i].name;
         //constructs internal objects ref by attr_name
         entry[attr_name] = {};
         entry[attr_name].type = table.options[i].type;
         entry[attr_name].val = table.options[i].func();
      }
      entries.push(JSON.stringify(entry));
   }
}

//tables are described by this format
// + Name of relation: name
// + Depends on: depends[other_table_name, [...]]
// + Relation values: elem[]
//   -> elem is seperate obj described by options
// + Relation gen options and type: options
var tables =
   [
   {
      name: 'Worker',
      depends: 'prime',
      elem: [],
      options:
      [
         {
            name: 'id',
            type: 'varchar(10)',
            func: () => {
               var test = tables.reduce((prev, cur) => {if (cur.name == this.depends) return cur;});
               var dict = new Dict.Dictionary('word', '\n', 'words.txt', true);
               return dict.rnd_def(100); 
            }
         }
      ]
   },
   {
      name: 'prime',
      depends: null,
      elem: [],
      options:
      [
         {
            name: 'id',
            type: 'varchar(10)',
            func: () => {
               var regrex = new RegExp('$\n');
               var dict = new Dict.Dictionary('word', regrex, 'words.txt', true);
               return dict.rnd_def(100);
            }
         }
      ]
   }
   ];

//to node
var nodes = [];
for (var i = 0; i < tables.length; i++) {
   var node = new Node.G_Node();
   node.elem = tables[i];
   nodes.push(node);
}
//link dependences
for (var i = 0; i < tables.length; i++) {
   if (!(nodes[i].elem.depends === null)) {
      nodes[i].depends_on(nodes.reduce(
      (prev, cur) => {
         if (cur.elem.name == nodes[i].elem.depends)
            return cur;
      }));
   }
}

//gen order
var order = Node.topo_sort(nodes);

order.forEach(
   (node) => {
      //console.log(node);
      gen_objects(node.elem, 100);
   }
);
