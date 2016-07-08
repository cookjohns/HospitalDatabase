var Node = require('./gnode');
var Dict = require('./dict');

var gen_objects = function(table, num_entries)
{
   var entries = [];
   var entry = {};
   for (var i = 0; i < num_entries; i++) {
      for (var j = 0; j < table.options.length; j++) {
         var attr_name = table.options[j].name;
         //constructs internal objects ref by attr_name
         entry[attr_name] = {};
         entry[attr_name].type = table.options[j].type;
         entry[attr_name].value = table.options[j].func();
      }
      entries.push(entry);
   }
   return entries;
}

//tables are described by this format
// + Name of relation: name
// + Depends on: depends[other_table_name, [...]]
// + Relation values: elem[]
//   -> elem is seperate obj described by options
// + Relation gen options and type: options
var tables =
   [
   worker = {
      name: 'Worker',
      depends: 'prime',
      elem: [],
      options:
      [
         {
            name: 'id',
            type: 'varchar(10)',
            func: () => {
               var opt = tables.reduce((prev, cur) => {
                  if (cur.name == worker.depends) return cur.elem;
               }); 
               return opt[Math.floor(Math.random()*opt.length)];
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
               var dict = new Dict.Dictionary('word', /\n/, 'words', true);
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
      node.elem.elem = gen_objects(node.elem, 10);
   }
);
console.log(JSON.stringify(order[1].elem.elem[0]));
console.log(JSON.stringify(order[1].elem.elem[1]));
console.log(JSON.stringify(order[0].elem.elem[1]));
console.log((order[0].elem.elem));
